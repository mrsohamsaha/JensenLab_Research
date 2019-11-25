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

from .utils import binaryMask
from .utils import detectColonies
from .utils import analyzeColonies
from .utils import highlightKeyPoints

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

		binaryImage = binaryMask(url[1:], 21, 2)

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
		originalImagePath = request.POST.get("original", "")
		binaryImagePath = request.POST.get("edit", "")
		blockSize = request.POST.get("blockSize", "")
		constant = request.POST.get("constant", "")

		binaryImage = binaryMask(originalImagePath[1:], blockSize, constant)
		cv2.imwrite(binaryImagePath[1:], binaryImage)

		outDict = {'url': name1, 'thresholdUrl': name2, 'blockSize': blockSize, 'constant': constant}
		return render(request, 'threshold.html', outDict)
	return render(request, 'threshold.html')

def pick(request):
	originalImagePath = request.POST.get("original", "")[1:]
	binaryImagePath = request.POST.get("edit", "")[1:]
	fromThresh = request.POST.get("fromThresh", "")

	# Detecting Blobs
	keypoints = detectColonies(originalImagePath, binaryImagePath)
	blobList = analyzeColonies(keypoints, binaryImagePath)
	binaryKeypoints, originalKeypoints = highlightKeyPoints(originalImagePath, binaryImagePath, blobList, len(blobList))

	# Saving image with blob detection
	fs = FileSystemStorage()
	name = originalImagePath[7:-4] + "BLOB" + ".jpg"
	cv2.imwrite('media/'+name, originalKeypoints)
	blobUrl = fs.url(name)
	outDict = {"original": originalImagePath, "edit": binaryImagePath, "blob": blobUrl, "count": len(blobList), "countSelected": len(blobList)}
	return render(request, 'pick.html', outDict)
