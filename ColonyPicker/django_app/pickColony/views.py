"""
Contains all views for web application.
"""

# Django
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import Http404

# standard libraries
import os
import cv2
import numpy as np

# utility functions
from .utils import binaryMask, detectColonies, analyzeColonies, highlightKeyPoints, rankColonies, formatKeyPoints

# global variables
url = ""
thresholdUrl = ""
original_blob_list = None
DEFAULT_BLOCK_SIZE = 21
DEFAULT_CONSTANT = 2


def home(request):
    """
    Home page where user can upload an image.
    """
    if request.method == 'POST':
        if request.POST.get("from_pick", "") == "1":
            os.remove(request.POST.get("original", "")[1:])
            os.remove(request.POST.get("edit", "")[1:])
            os.remove(request.POST.get("original_blob", "")[1:])
            os.remove(request.POST.get("edit_blob", "")[1:])
            os.remove(request.POST.get("coordinates", "")[1:])
            return render(request, 'home.html')
        elif request.POST.get("from_threshold", "") == "1":
            os.remove(request.POST.get("original", "")[1:])
            os.remove(request.POST.get("edit", "")[1:])
            return render(request, 'home.html')
        else:
            # Post request is to upload an image
            if not request.FILES:
                raise Http404('Image was not uploaded')
            uploaded_file = request.FILES['image']

            # Saving uploaded image in media directory
            fs = FileSystemStorage()
            name = fs.save(uploaded_file.name, uploaded_file)
            url = fs.url(name)

            binary_image = binaryMask(url[1:], DEFAULT_BLOCK_SIZE, DEFAULT_CONSTANT)

            # Saving binary image
            threshold_name = name[:-4] + 'EDIT' + '.jpg'
            cv2.imwrite('media/' + threshold_name, binary_image)
            threshold_url = fs.url(threshold_name)
            content = {'url': url, 'threshold_url': threshold_url, 'block_size': DEFAULT_BLOCK_SIZE,
                       'constant': DEFAULT_CONSTANT}
            return render(request, 'threshold.html', content)

    # Request method is GET to launch web app
    return render(request, 'home.html')


def threshold(request):
    """
    Threshold page where user can adjust the threshold
    parameters of the input image.
    """
    if request.method == 'POST':
        # Obtaining inputs from user
        original_image_path = request.POST.get("original", "")
        binary_image_path = request.POST.get("edit", "")
        block_size = request.POST.get("block_size", "")
        constant = request.POST.get("constant", "")
        print(request.POST.dict())

        binary_image = binaryMask(original_image_path[1:], int(block_size), int(constant))
        cv2.imwrite(binary_image_path[1:], binary_image)

        content = {'url': original_image_path, 'threshold_url': binary_image_path, 'block_size': block_size,
                   'constant': constant}
        return render(request, 'threshold.html', content)
    return render(request, 'threshold.html')


def pick(request):
    """
	Pick page where the user can adjust how many colonies
	they want to select to be exported.
    """
    global original_blob_list
    if request.method == 'POST':
        original_image_path = request.POST.get("original", "")
        binary_image_path = request.POST.get("edit", "")
        from_thresh = request.POST.get("from_thresh", "")
        binary_image = cv2.imread(binary_image_path[1:], 0)
        original_image = cv2.imread(original_image_path[1:])
        cutoff = 0

        # Detecting Blobs for first time
        if from_thresh == "1":
            key_points = detectColonies(binary_image)
            blob_list = analyzeColonies(key_points, binary_image)
            original_blob_list = rankColonies(blob_list)
            cutoff = len(original_blob_list)
        else:
            cutoff = int(request.POST.get("cutoff", ""))

        binary_key_points, original_key_points = highlightKeyPoints(original_image, binary_image,
                                                                    original_blob_list, cutoff)
        coordinates = formatKeyPoints(original_blob_list, cutoff)

        # Saving images and coordinates
        fs = FileSystemStorage()
        name = original_image_path[7:-4] + "BLOB" + ".jpg"
        name_binary = binary_image_path[7:-4] + "BLOB" + ".jpg"
        coordinate_name = "colonyCoordinates.csv"

        cv2.imwrite('media/' + name, original_key_points)
        cv2.imwrite('media/' + name_binary, binary_key_points)
        np.savetxt('media/' + coordinate_name, coordinates, delimiter=",")

        blob_url = fs.url(name)
        blob_url_binary = fs.url(name_binary)
        coordinate_url = fs.url(coordinate_name)

        content = {"original": original_image_path, "edit": binary_image_path, "blob": blob_url,
                   "blob_binary": blob_url_binary, "coordinates": coordinate_url,
                   "count": len(original_blob_list), "cutoff": cutoff}
        return render(request, 'pick.html', content)
    return render(request, 'pick.html')
