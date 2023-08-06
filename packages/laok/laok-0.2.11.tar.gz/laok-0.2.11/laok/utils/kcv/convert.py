#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2020/7/24 11:55:53

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
import cv2
import numpy as np
from PIL import Image
#===============================================================================
# skimage 图像格式        通道：RGB 像素值：[0.0,1.0]      (h,w)
# Opencv  图像格式        通道：BGR 像素值：[0,255]        (h,w)
# PIL     图像格式        (w,h)
#===============================================================================

__all__ = ['is_pil_image', 'is_numpy_image', 'gray2bgr', 'gray2rgb', 'bgr2gray', 'rgb2gray',
           'rgb2bgr', 'bgr2rgb', 'cv2pil', 'pil2cv', 'cv2sk', 'sk2cv']

def is_pil_image(img):
    return isinstance(img, Image.Image)

def is_numpy_image(img):
    return isinstance(img, np.ndarray) and img.ndim in {2, 3}

def gray2bgr(img):
    #cvtColor(src, code[, dst[, dstCn]]) -> dst
    if img.ndim == 3 and img.shape[-1] == 3:
        return img
    elif img.ndim == 2:
        return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    return img


def gray2rgb(img):
    if img.ndim == 3 and img.shape[-1] == 3:
        return img
    elif img.ndim == 2:
        return cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    return img


def bgr2gray(img):
    if img.ndim == 3:
        if img.shape[-1] == 3:
            return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY )
        elif img.shape[-1] == 4:
            return cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY )
    elif img.ndim == 2:
        return img
    return img


def rgb2gray(img):
    if img.ndim == 3:
        if img.shape[-1] == 3:
            return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY )
        elif img.shape[-1] == 4:
            return cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY )
    elif img.ndim == 2:
        return img
    return img


def rgb2bgr(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2BGR )


def bgr2rgb(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB )


def cv2pil(img):
    if img.ndim == 3 and img.shape[-1] == 3:
        image = Image.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB), mode = 'RGB')
    else:
        image = Image.fromarray(img, mode = 'L')
    return image


def pil2cv(img):
    if img.mode == 'RGB':
        image = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
    elif img.mode == 'RGBA':
        image = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGBA2BGRA)
    elif img.mode == 'L':
        image = np.asarray(img)
    return image


def cv2sk(img):
    if img.ndim == 3:
        if img.shape[-1] == 3:
            img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        elif img.shape[-1] == 4:
            img = cv2.cvtColor(img,cv2.COLOR_BGRA2RGBA)
    return img


def sk2cv(img):
    if img.ndim == 3:
        if img.shape[-1] == 3:
            img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
        elif img.shape[-1] == 4:
            img = cv2.cvtColor(img,cv2.COLOR_RGBA2BGRA)
    return img