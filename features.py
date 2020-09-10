# -*- coding: utf-8 -*-
"""
Created on Sat May 16 21:06:05 2020

@author: walia
"""


import os
import cv2
import numpy as np
from random import shuffle


def integral_pushpinder(img):
    
    integral_img = img
    for j in range(1, img.shape[1]):
        integral_img[0,j] = integral_img[0,j-1] + img[0,j]
    for i in range(1, img.shape[0]):
        integral_img[i,0] = integral_img[i-1,0] + img[i,0]
    for i in range(1,img.shape[0]):
        for j in range(1, img.shape[1]):
            integral_img[i,j] = img[i,j] + integral_img[i-1,j] + integral_img[i,j-1] - integral_img[i-1,j-1]
            
    return integral_img


def typerect2(img, i, j, width, height):
    if (i==0 and j==0):
        return abs(img[i+width-1, j+height-1] - (img[i+width-1, j+height+height-1] - img[i+width-1, j+height-1]))
    elif(i==0 and j!=0):
        left = img[i+width-1, j+height-1] - img[i+width-1, j-1]
        right = img[i+width-1, j+height+height-1] - img[i+width-1, j+height-1]
        return abs(left-right)
    elif(i!=0 and j==0):
        left = img[i+width-1, j+height-1] - img[i-1,  j+height-1]
        right = img[i+width-1, j+height+height-1] - img[i+width-1, j+height-1] - img[i-1, j+height+height-1]+ img[i-1, j+height-1]
        return abs(left-right)
    else:
        left = img[i+width-1, j+height-1] - img[i+width-1, j-1] - img[i-1, j+height-1]+ img[i-1, j-1]
        right = img[i+width-1, j+height+height-1] - img[i+width-1, j+height-1] - img[i-1, j+height+height-1]+ img[i-1, j+height-1]
        return abs(left-right)
    

def typerect3(img, i, j, width, height):
    if (i==0 and j==0):
        left = img[i+width-1, j+height-1]
        mid = img[i+width-1, j+(height*2)-1] - img[i+width-1, j+height-1]
        right = img[i+width-1, j+(height*3)-1] - img[i+width-1, j+(height*2)-1]
        return abs(left+right-mid)
    elif(i==0 and j!=0):
        left = img[i+width-1, j+height-1] - img[i+width-1, j-1]
        mid = img[i+width-1, j+(height*2)-1] - img[i+width-1, j+height-1]
        right = img[i+width-1, j+(height*3)-1] - img[i+width-1, j+(height*2)-1]
        return abs(left+right-mid)
    elif(i!=0 and j==0):
        left = img[i+width-1, j+height-1] - img[i-1, j+height-1]
        mid = img[i+width-1, j+(height*2)-1] - img[i+width-1, j+height-1] - img[i-1, j+(height*2)-1]+ img[i-1, j+height-1]
        right = img[i+width-1, j+(height*3)-1] - img[i+width-1, j+(height*2)-1] - img[i-1, j+(height*3)-1]+ img[i-1, j+(height*2)-1]
        return abs(left+right-mid)
    else:
        left = img[i+width-1, j+(height)-1] - img[i+width-1, j-1] - img[i-1, j+(height)-1]+ img[i-1, j-1]
        mid = img[i+width-1, j+(height*2)-1] - img[i+width-1, j+height-1] - img[i-1, j+(height*2)-1]+ img[i-1, j+height-1]
        right = img[i+width-1, j+(height*3)-1] - img[i+width-1, j+(height*2)-1] - img[i-1, j+(height*3)-1]+ img[i-1, j+(height*2)-1]
        return abs(left+right-mid)

def typerect2_transpose(img, i, j, width, height):
    if (i==0 and j==0):
        return abs(img[i+width-1, j+height-1] - (img[i+(width*2)-1, j+height-1] - img[i+width-1, j+height-1]))
    elif(i==0 and j!=0):
        up = img[i+width-1, j+height-1] - img[i+width-1, j-1]
        down = img[i+(width*2)-1, j+height-1] - img[i+width-1, j+height-1] - img[i+(width*2)-1, j-1]+ img[i+width-1, j-1]
        return abs(up-down)
    elif(i!=0 and j==0):
        up = img[i+width-1, j+height-1] - img[i-1,  j+height-1]
        down = img[i+(width*2)-1, j+height-1] - img[i+width-1,  j+height-1]
        return abs(up-down)
    else:
        left = img[i+width-1, j+height-1] - img[i+width-1, j-1] - img[i-1, j+height-1]+ img[i-1, j-1]
        right = img[i+(width*2)-1, j+height-1] - img[i+width-1, j+height-1] - img[i+(width*2)-1, j-1]+ img[i+width-1, j-1]
        return abs(left-right)
    
def typerect4(img, i, j, width, height):
    if (i==0 and j==0):
        box1 =  img[i+width-1, j+height-1]
        box2 = img[i+width-1, j+height*2-1] - img[i+width-1, j+height-1]
        box3 = img[i+width*2-1, j+height-1] - img[i+width-1, j+height-1]
        box4 = img[i+width*2-1, j+height*2-1] - img[i+width*2-1, j+height-1] - img[i+width-1, j+height*2-1] + img[i+width-1, j+height-1]
        return (abs(box1+box4-box2-box3))
    elif(i==0 and j!=0):
        box1 =  img[i+width-1, j+height-1] - img[i+width-1, j-1]
        box2 = img[i+width-1, j+height*2-1] - img[i+width-1, j+height-1]
        box3 = img[i+width*2-1, j+height-1] - img[i+width-1, j+height-1] - img[i+width*2-1, j-1] + img[i+width-1, j-1]
        box4 = img[i+width*2-1, j+height*2-1] - img[i+width*2-1, j+height-1] - img[i+width-1, j+height*2-1] + img[i+width-1, j+height-1]
        return (abs(box1+box4-box2-box3))
    elif(i!=0 and j==0):
        box1 =  img[i+width-1, j+height-1] - img[i+width-1, j-1]
        box2 = img[i+width-1, j+height*2-1] - img[i+width-1, j+height-1] - img[i-1, j+height*2-1] + img[i+width-1, j+height-1]
        box3 = img[i+width*2-1, j+height-1] - img[i+width-1, j+height-1]
        box4 = img[i+width*2-1, j+height*2-1] - img[i+width*2-1, j+height-1] - img[i+width-1, j+height*2-1] + img[i+width-1, j+height-1]
        return (abs(box1+box4-box2-box3))
    else:
        box1 =  img[i+width-1, j+height-1]
        box2 = img[i+width-1, j+height*2-1] - img[i+width-1, j+height-1] - img[i-1, j+height*2-1] + img[i-1, j+height-1]
        box3 = img[i+width*2-1, j+height-1] - img[i+width*2-1, j-1] - img[i-1, j+height-1] + img[i-1, j-1]
        box4 = img[i+width*2-1, j+height*2-1] - img[i+width*2-1, j+height-1] - img[i+width-1, j+height*2-1] + img[i+width-1, j+height-1]
        return (abs(box1+box4-box2-box3))


def extract_features(img):
    
    feats = list()
    
    
    for i in range(0,img.shape[0]):
        for j in range(0, img.shape[1]):
        
        
            for width in range(1,img.shape[1]):
                for height in range(1, img.shape[0]):
                    
                    if (i + (width*2) - 1 < img.shape[0] and j + (height*2) - 1 < img.shape[1]):
                        feats.append(typerect2(img, i, j, width, height))
                    
                    if (i + (width*2) - 1 < img.shape[0] and j + (height*2) - 1 < img.shape[1]):
                        feats.append(typerect2_transpose(img, i, j, width, height)(img, i, j, width, height))
                    
                    if (i + (width*3) - 1 < img.shape[0] and j + (height*2) - 1 < img.shape[1]):
                        feats.append(typerect3(img, i, j, width, height))
                    
                    if (i + (width*2) - 1 < img.shape[0] and j + (height*2) - 1 < img.shape[1]):
                        feats.append(typerect4(img, i, j, width, height))
                    
                    
    return feats


img = cv2.imread("tatti.jpg", cv2.IMREAD_GRAYSCALE).astype(np.int32)

result = integral_pushpinder(img)
features = extract_features(img)
print(result, np.shape(result))