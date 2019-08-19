from django.shortcuts import render
from base64 import b64encode
from django.core.files.storage import FileSystemStorage
from django.core.files import File
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
		print(thresholdUrl)
		return render(request, 'threshold.html', {'url': url, 'thresholdUrl': thresholdUrl})
	return render(request, 'home.html')

def threshold(request):
	return render(request, 'threshold.html')

def pick(request):
	name1 = request.POST.get("original", "")
	name2 = request.POST.get("edit", "")
	return render(request, 'pick.html', {"original": name1, "edit": name2})
