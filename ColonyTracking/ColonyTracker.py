#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2
import numpy as np
from matplotlib import pyplot as plt


# ## Stitching code

# In[2]:


#List of range,Path to image folder, a tuple of camera "shape", a tuple of percentage overlap
def stitch(toStitch,shape,overlap):
    #crop the images
    toStitch = crop(toStitch,overlap)
    #stitch them together
    stitched =list()
    for img in range(len(toStitch[0])):
        xStitched = list()
        for x in range(shape[0]-1):
            xStitched = list()
            for y in range(shape[1]):
                concat = np.concatenate((toStitch[x+y*shape[0]][img],toStitch[x+y*shape[0]+1][img]),axis=0)
                xStitched.append(concat)
        concat = [[0]]
        for y in range(shape[1]-1):
            concat = np.concatenate((xStitched[y],xStitched[y+1]),axis=1)
        stitched.append(concat)
    if shape == [1,1]:
        return toStitch[0]
    else:
        return stitched


# In[3]:


def testStitch(toStitch,shape,overlap):
    #crop the images
    toStitch = crop(toStitch,overlap)
    #stitch them together
    stitched =list()
    for img in range(len(toStitch[0])):
        xStitched = list()
        for x in range(shape[0]-1):
            xStitched = list()
            for y in range(shape[1]):
                concat = np.concatenate((toStitch[x+y*shape[0]][img],toStitch[x+y*shape[0]+1][img]),axis=0)
                xStitched.append(concat)
        cv2.namedWindow("0", cv2.WINDOW_NORMAL)
        cv2.imshow('0',xStitched[0])
        cv2.namedWindow("1", cv2.WINDOW_NORMAL)
        cv2.imshow('1',xStitched[1])
        cv2.waitKey(0)
        concat = [[0]]
        for y in range(shape[1]-1):
            concat = np.concatenate((xStitched[y],xStitched[y+1]),axis=1)
        stitched.append(concat)
    return stitched


# In[4]:


def crop(toStitch, overlap):
    pixelOverlap = (overlap[0]*toStitch[0][0].shape[0],overlap[1]*toStitch[0][0].shape[1])
    cropped = list()
    for cam in range(len(toStitch)):
        perCam = list()
        for i in range(len(toStitch[cam])):
            perCam.append(toStitch[cam][i][0:int(toStitch[cam][i].shape[1]-(pixelOverlap[1]/2)),0:int(toStitch[cam][i].shape[0]-(pixelOverlap[0]/2))])
        cropped.append(perCam)
    return cropped


# In[13]:


TL = cv2.imread("Plate Images/2019-06-27_16.21.09/Camera-3/2/image-00000.jpg")
TR = cv2.imread("Plate Images/2019-06-27_16.21.09/Camera-2/2/image-00000.jpg")
BL = cv2.imread("Plate Images/2019-06-27_16.21.09/Camera-1/2/image-00000.jpg")
BR = cv2.imread("Plate Images/2019-06-27_16.21.09/Camera-0/2/image-00000.jpg")
plt.imshow(BL, cmap = 'gray', interpolation = 'bicubic')
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.show()


# In[14]:


toStitch = [[TL],[BL],[TR],[BR]]
res = stitch(toStitch,(2,2),(0.11,0.11))
for img in res:
    cv2.namedWindow("img", cv2.WINDOW_NORMAL)
    cv2.imshow('img',img)
    cv2.waitKey(0)


# ## Segmentation & Binary Mask

# In[2]:


plateImage = cv2.imread("Plate Images/croppedPlate.jpg",0)


# In[3]:


plt.imshow(plateImage, 'gray')
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.show()


# In[4]:


hist = cv2.calcHist([plateImage],[0],None,[256],[0,256])


# In[40]:


plt.hist(plateImage.ravel(),256,[0,256]); plt.show()


# In[20]:


ret,th1 = cv2.threshold(plateImage,127,255,cv2.THRESH_BINARY)
plt.imshow(th1, 'gray')
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.title("Global Thresholding (v = 127)")
plt.show()


# In[33]:


b1 = 21; c1 = 5; 
b2 = 11; c2 = 5; 
b3 = 21; c3 = 2; 
adapMean1 = cv2.adaptiveThreshold(plateImage,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,b1, c1)
adapMean2 = cv2.adaptiveThreshold(plateImage,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,b2, c2)
adapMean3 = cv2.adaptiveThreshold(plateImage,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,b3, c3) 

titles = ['Original Image', 'Box Size: ' + str(b1) + ', Constant: ' + str(c1),
            'Box Size: ' + str(b2) + ', Constant: ' + str(c2), 'Box Size: ' + str(b3) + ', Constant: ' + str(c3)]
images = [plateImage, adapMean1, adapMean2, adapMean3]

for i in range(4):
    plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()


# In[35]:


b1 = 21; c1 = 5; 
b2 = 11; c2 = 5; 
b3 = 21; c3 = 2; 
adapGauss1 = cv2.adaptiveThreshold(plateImage,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,b1, c1)
adapGauss2 = cv2.adaptiveThreshold(plateImage,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,b2, c2)
adapGauss3 = cv2.adaptiveThreshold(plateImage,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, b3, c3) 

titles = ['Original Image', 'Box Size: ' + str(b1) + ', Constant: ' + str(c1),
            'Box Size: ' + str(b2) + ', Constant: ' + str(c2), 'Box Size: ' + str(b3) + ', Constant: ' + str(c3)]
images = [plateImage, adapGauss1, adapGauss2, adapGauss3]

for i in range(4):
    plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()


# In[39]:


# global thresholding
ret1,th1 = cv2.threshold(plateImage,127,255,cv2.THRESH_BINARY)

# Otsu's thresholding
ret2,th2 = cv2.threshold(plateImage,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

# Otsu's thresholding after Gaussian filtering
blur = cv2.GaussianBlur(plateImage,(5,5),0)
ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

# plot all the images and their histograms
images = [plateImage, 0, th1,
          plateImage, 0, th2,
          plateImage, 0, th3]
titles = ['Original Noisy Image','Histogram','Global Thresholding (v=127)',
          'Original Noisy Image','Histogram',"Otsu's Thresholding",
          'Gaussian filtered Image','Histogram',"Otsu's Thresholding"]

for i in range(3):
    plt.subplot(3,3,i*3+1),plt.imshow(images[i*3],'gray')
    plt.title(titles[i*3]), plt.xticks([]), plt.yticks([])
    plt.subplot(3,3,i*3+2),plt.hist(images[i*3].ravel(),256)
    plt.title(titles[i*3+1]), plt.xticks([]), plt.yticks([])
    plt.subplot(3,3,i*3+3),plt.imshow(images[i*3+2],'gray')
    plt.title(titles[i*3+2]), plt.xticks([]), plt.yticks([])
plt.show()


# In[ ]:




