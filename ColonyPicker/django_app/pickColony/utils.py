import math
import cv2
import numpy as np


# Helper Classes and Functions
class Blob(cv2.KeyPoint):
    def __init__(self, whitePix, darkPix, keyPoint):
        self.whitePix = whitePix
        self.darkPix = darkPix
        cv2.KeyPoint.__init__(self, x=keyPoint.pt[0], y=keyPoint.pt[1], _size=keyPoint.size)


def dist(p1, p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def convert(blobList):
    return [cv2.KeyPoint(x=blob.pt[0], y=blob.pt[1], _size=blob.size) for blob in blobList]


# Main Functions
def binary_mask(image_path, block_size, constant):
    """
    :param image_path: path to the image to apply the binary mask
    :type image_path: str
    :param block_size: the block size to apply to the binary mask
    :type block_size: int
    :param constant: the constant to apply to the binary mask
    :type constant: int
    :return: the input image with a binary mask applied
    :rtype : numpy.ndarray
    """
    plate_image = cv2.imread(image_path, 0)
    image = cv2.fastNlMeansDenoising(plate_image, None, 10, 7, 21)
    adap_gauss = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, block_size,
                                       constant)
    return adap_gauss


def detect_colonies(binary_image):
    """
    :param binary_image: binary image to detect colonies from
    :type binary_image: numpy.ndarray
    :return: keypoints for each colony detected
    :rtype: list(cv2.KeyPoint)
    """
    params = cv2.SimpleBlobDetector_Params()
    params.filterByColor = True
    params.blobColor = 255
    params.filterByInertia = True
    params.minInertiaRatio = 0.01
    params.filterByConvexity = True
    params.minConvexity = 0.9

    detector = cv2.SimpleBlobDetector_create(params)

    keypoints = detector.detect(binary_image)
    return keypoints


def analyze_colonies(keypoints, binary_image):
    """
    :param keypoints: list of keypoints for each detected colony
    :type keypoints: list(cv2.KeyPoint)
    :param binary_image: binary image to detect colonies from
    :type binary_image: numpy.ndarray
    :return: metadata about each colony detected
    :rtype: list(tuple)
    """
    R = 32
    phi = 0.1
    width = len(binary_image)
    height = len(binary_image[0])
    blob_list = []
    for keypoint in keypoints:
        # Obtaining the x,y pixel coordinates of the blob
        center_x = int(keypoint.pt[0])
        center_y = int(keypoint.pt[1])

        # Starting x and y coordinates for the segmented box
        lower_x = center_x - R
        low_y = center_y - R

        # discarding blobs too close to window boundaries
        if lower_x < 0 or low_y < 0 or lower_x + 2 * R > width or low_y + 2 * R > height:
            continue
        r = int(keypoint.size * (1 + phi)) / 2

        # dark percentage inside = darkCount/insideCount
        # white percentage outside = whiteCount/outsideCount
        inside_count = 0
        outside_count = 0
        white_count = 0
        dark_count = 0
        for i in range(lower_x, lower_x + 2 * R):
            for j in range(low_y, low_y + 2 * R):
                # Do not count pixels that are outside larger circle
                if dist([center_x, center_y], [i, j]) >= R:
                    continue
                # Check for dark pixels inside blob
                elif dist([center_x, center_y], [i, j]) <= r:
                    inside_count += 1
                    if binary_image[j, i] == 0:
                        dark_count += 1
                # Check for white pixels outside blob
                else:
                    outside_count += 1
                    if binary_image[j, i] == 255:
                        white_count += 1
        white_pix = white_count * 100 / outside_count
        dark_pix = dark_count * 100 / inside_count
        blob_list.append((white_pix, dark_pix, keypoint))
        # blob_list.append(keyPoint)
    print("%d Viable Colonies Analyzed" % len(blob_list))
    print(type(blob_list[0]))
    return blob_list


def rank_colonies(blob_list):
    """
    :param blob_list: metadata about each colony detected
    :type blob_list: list(tuple)
    :return: keypoint of each viable colony
    :rtype: list(cv2.KeyPoint)
    """
    dark_cutoff = np.percentile(np.array([blob[1] for blob in blob_list]), 95)
    white_cutoff = np.percentile(np.array([blob[0] for blob in blob_list]), 50)
    for i, blob in enumerate(blob_list):
        if blob[1] > dark_cutoff or blob[0] > white_cutoff:
            blob_list.remove(blob)
    blob_list.sort(key=lambda x: x[0])
    print("%d Viable Colonies Extracted" % len(blob_list))
    keypoint_list = [blob[2] for blob in blob_list]
    return keypoint_list


def highlight_key_points(original_image, binary_image, keypoint_list, count):
    """
    :param original_image: original image of the petri dish
    :type original_image: numpy.ndarray
    :param binary_image: binary mask image of the petri dish
    :type binary_image: numpy.ndarray
    :param keypoint_list: list of keypoints for each viable colony
    :type keypoint_list: list(cv2.KeyPoint)
    :param count: number of colonies to select
    :type count: int
    :return: pair containing the binary and original image with keypoints highlighted
    :rtype: tuple
    """
    binary_keypoints = cv2.drawKeypoints(binary_image, keypoint_list[:count], np.array([]), (0, 0, 255),
                                        cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    original_keypoints = cv2.drawKeypoints(original_image, keypoint_list[:count], np.array([]), (0, 0, 255),
                                          cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    return binary_keypoints, original_keypoints


def format_key_points(keypoints, count):
    """
    :param keypoints: list of keypoints
    :type keypoints: list(cv2.KeyPoint)
    :param count: number of keypoints to select
    :type count: int
    :return: array containing the x and y coordinate for each keypoint
    :rtype: numpy.
    """
    type(np.asarray([[keyPoint.pt[0], keyPoint.pt[1]] for keyPoint in keypoints[:count]]))
    return np.asarray([[keyPoint.pt[0], keyPoint.pt[1]] for keyPoint in keypoints[:count]])
