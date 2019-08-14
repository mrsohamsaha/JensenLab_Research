import cv2
import numpy as np
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
def crop(toStitch, overlap):
    pixelOverlap = (overlap[0]*toStitch[0][0].shape[0],overlap[1]*toStitch[0][0].shape[1])
    cropped = list()
    for cam in range(len(toStitch)):
        perCam = list()
        for i in range(len(toStitch[cam])):
            perCam.append(toStitch[cam][i][0:int(toStitch[cam][i].shape[1]-(pixelOverlap[1]/2)),0:int(toStitch[cam][i].shape[0]-(pixelOverlap[0]/2))])
        cropped.append(perCam)
    return cropped
# if __name__ == "__main__":
#     TL = cv2.imread(r'C:\Users\aslan\Documents\UIUC\Jensen Lab\Research\Colony Tracker\Archive\papercirclesTL.jpg')
#     TR = cv2.imread(r'C:\Users\aslan\Documents\UIUC\Jensen Lab\Research\Colony Tracker\Archive\papercirclesTR.jpg')
#     BL = cv2.imread(r'C:\Users\aslan\Documents\UIUC\Jensen Lab\Research\Colony Tracker\Archive\papercirclesBL.jpg')
#     BR = cv2.imread(r'C:\Users\aslan\Documents\UIUC\Jensen Lab\Research\Colony Tracker\Archive\papercirclesBR.jpg')
#     toStitch = [[TL,TL,TL],[BL,BL,BL],[TR,TR,TR],[BR,BR,BR]]
#     res = testStitch(toStitch,(2,2),(.11,.11))
#     for img in res:
#         cv2.namedWindow("img", cv2.WINDOW_NORMAL)
#         cv2.imshow('img',img)
#         cv2.waitKey(0)
