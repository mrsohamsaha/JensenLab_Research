from django.shortcuts import render
from base64 import b64encode
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.http import Http404
import os

import math
import pandas as pd
import cv2
import numpy as np

# global variables
url = ""
thresholdUrl = ""

def home(request):
	if request.method == 'POST':
		# Obtaining uploaded image from FILE dict
		if not request.FILES:
			raise Http404('Image was not uploaded')
		uploaded_file = request.FILES['image']

		# Saving uploaded image in media directory
		fs = FileSystemStorage()
		name = fs.save(uploaded_file.name, uploaded_file)
		url = fs.url(name)

		# Opening image in OpenCV
		plateImage = cv2.imread(url[1:],0)
		image = cv2.fastNlMeansDenoising(plateImage,None,10,7,21)
		binaryImage = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 2)

		# Saving thresholded image
		thresholdName = name[:-4]+'EDIT'+'.jpg'
		cv2.imwrite('media/'+thresholdName, binaryImage)
		thresholdUrl = fs.url(thresholdName)
		outDict = {'url': url, 'thresholdUrl': thresholdUrl, 'blockSize': 21, 'constant': 2}
		return render(request, 'threshold.html', outDict)
	return render(request, 'home.html')

def threshold(request):
	if request.method == 'POST':
		# Obtaining inputs from user
		name1 = request.POST.get("original", "")
		name2 = request.POST.get("edit", "")
		blockSize = request.POST.get("blockSize", "")
		constant = request.POST.get("constant", "")

		# Making Updates
		plateImage = cv2.imread(name1[1:],0)
		image = cv2.fastNlMeansDenoising(plateImage,None,10,7,21)
		binaryImage = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, int(blockSize), int(constant))
		cv2.imwrite(name2[1:], binaryImage)

		outDict = {'url': name1, 'thresholdUrl': name2, 'blockSize': blockSize, 'constant': constant}
		return render(request, 'threshold.html', outDict)
	return render(request, 'threshold.html')

def pick(request):
	original = request.POST.get("original", "")
	edit = request.POST.get("edit", "")
	fromThresh = request.POST.get("fromThresh", "")
	print(type(fromThresh))
	print(fromThresh)

	# Setting up Blob Detection Parameters
	params = cv2.SimpleBlobDetector_Params()
	params.filterByColor = True
	params.blobColor = 255
	params.filterByInertia = True
	params.minInertiaRatio = 0.01
	params.filterByConvexity = True
	params.minConvexity = 0.9

	# Detecting version of OpenCV
	is_v2 = cv2.__version__.startswith("2.")
	if is_v2:
		detector = cv2.SimpleBlobDetector(params)
	else:
		detector = cv2.SimpleBlobDetector_create(params)

	# Detecting Blobs
	plateImage = cv2.imread(edit[1:],0)
	keypoints = detector.detect(plateImage)

	# Ranking Blobs

	# Saving image with blob detection
	fs = FileSystemStorage()
	im_with_keypoints = cv2.drawKeypoints(plateImage, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
	name = original[7:-4] + "BLOB" + ".jpg"
	cv2.imwrite('media/'+name, im_with_keypoints)
	blobUrl = fs.url(name)
	outDict = {"original": original, "edit": edit, "blob": blobUrl, "count": len(keypoints), "countSelected": len(keypoints)}
	return render(request, 'pick.html', outDict)
