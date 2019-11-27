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
from .utils import rankColonies

# global variables
url = ""
thresholdUrl = ""
originalBlobList = None

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

		outDict = {'url': originalImagePath, 'thresholdUrl': binaryImagePath, 'blockSize': blockSize, 'constant': constant}
		return render(request, 'threshold.html', outDict)
	return render(request, 'threshold.html')

def pick(request):
	global originalBlobList
	if request.method == 'POST':
		originalImagePath = request.POST.get("original", "")
		binaryImagePath = request.POST.get("edit", "")
		fromThresh = request.POST.get("fromThresh", "")
		binaryImage = cv2.imread(binaryImagePath[1:],0)
		originalImage = cv2.imread(originalImagePath[1:])
		cutoff = 0
		# Detecting Blobs for first time
		if fromThresh == "1":
			keypoints = detectColonies(binaryImage)
			blobList = analyzeColonies(keypoints, binaryImage)
			originalBlobList = rankColonies(blobList)
			cutoff = len(originalBlobList)
		else:
			cutoff = int(request.POST.get("cutoff", ""))
		# keyPointList = [cv2.KeyPoint(x = blob.pt[0], y = blob.pt[1], _size = blob.size) for blob in originalBlobList]
		binaryKeypoints, originalKeypoints = highlightKeyPoints(originalImage, binaryImage, originalBlobList, cutoff)
		# Saving images with blob detection
		fs = FileSystemStorage()
		name = originalImagePath[7:-4] + "BLOB" + ".jpg"
		nameBinary = binaryImagePath[7:-4] + "BLOB" + ".jpg"
		cv2.imwrite('media/'+name, originalKeypoints)
		cv2.imwrite('media/'+nameBinary, binaryKeypoints)
		blobUrl = fs.url(name)
		blobUrlBinary = fs.url(nameBinary)
		outDict = {"original": originalImagePath, "edit": binaryImagePath, "blob": blobUrl, "blobBinary": blobUrlBinary, "count": len(originalBlobList), "cutoff": cutoff}
		return render(request, 'pick.html', outDict)
	return render(request, 'pick.html')
