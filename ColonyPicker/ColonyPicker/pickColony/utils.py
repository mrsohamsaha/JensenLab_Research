import math
import pandas as pd
import cv2
import numpy as np

class Blob(cv2.KeyPoint):
    def __init__(self, whitePix, darkPix, keyPoint):
        self.whitePix = whitePix
        self.darkPix = darkPix
        cv2.KeyPoint.__init__(self, x = keyPoint.pt[0], y = keyPoint.pt[1], _size = keyPoint.size)

def dist(p1, p2):
    return math.sqrt((p2[0] -  p1[0])**2 + (p2[1] - p1[1])**2)

def binaryMask(imagePath, blockSize, constant):
    plateImage = cv2.imread(imagePath,0)
    image = cv2.fastNlMeansDenoising(plateImage,None,10,7,21)
    adapGauss = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, blockSize, constant)
    return adapGauss

def detectColonies(orginalImagePath, binaryImagePath):

    binaryImage = cv2.imread(binaryImagePath,0)
    originalImage = cv2.imread(orginalImagePath)

    params2 = cv2.SimpleBlobDetector_Params()
    params2.filterByColor = True
    params2.blobColor = 255
    params2.filterByInertia = True
    params2.minInertiaRatio = 0.01
    params2.filterByConvexity = True
    params2.minConvexity = 0.9
    detector = cv2.SimpleBlobDetector_create(params2)

    keypoints = detector.detect(binaryImage)
    return keypoints

def analyzeColonies(keyPoints, binaryImagePath):
    binaryImage = cv2.imread(binaryImagePath,0)
    R = 32
    phi = 0.1
    width = len(binaryImage)
    height = len(binaryImage[0])
    blobList = []
    for keyPoint in keyPoints:
        # Obtaining the x,y pixel coordinates of the blob
        x = (int) (keyPoint.pt[0])
        y = (int) (keyPoint.pt[1])
        coord = [x, y]
        # Starting x and y coordinates for the segmented box
        lowX = x - R
        lowY = y - R

        # discarding blobs too close to window boundaries
        if lowX < 0 or lowY < 0 or lowX + 2*R > width or lowY + 2*R > height:
            continue
        r = (int) (keyPoint.size * (1+phi))/2
        # dark percentage inside = darkCount/insideCount
        # white percentage outside = whiteCOunt/outsideCount
        insideCount = 0
        outsideCount = 0
        whiteCount = 0
        darkCount = 0
        for i in range(lowX, lowX + 2*R):
            for j in range (lowY, lowY + 2*R):
                # Do not count pixels that are outside larger circle
                if dist([x,y], [i,j]) >= R:
                    continue
                # Check for dark pixels inside blob
                elif dist([x,y], [i,j]) <= r:
                    insideCount += 1
                    if binaryImage[j, i] == 0:
                        darkCount += 1
                # Check for white pixels outside blob
                else:
                    outsideCount += 1
                    if binaryImage[j, i] == 255:
                        whiteCount += 1
        whitePix = whiteCount*100/outsideCount
        darkPix = darkCount*100/insideCount
        blobList.append(Blob(whitePix, darkPix, keyPoint))
    print("%d Viable Colonies Analyzed" % len(blobList))
    return blobList

def convert(blobList):
    return [cv2.KeyPoint(x = blob.pt[0], y = blob.pt[1], _size = blob.size) for blob in blobList]

def highlightKeyPoints(originalImagePath, binaryImagePath, blobList, amount):
    keypointList = convert(blobList)
    binaryImage = cv2.imread(binaryImagePath,0)
    originalImage = cv2.imread(originalImagePath)
    binaryKeypoints = cv2.drawKeypoints(binaryImage, keypointList[:amount], np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    originalKeypoints = cv2.drawKeypoints(originalImage, keypointList[:amount], np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    return (binaryKeypoints, originalKeypoints)
