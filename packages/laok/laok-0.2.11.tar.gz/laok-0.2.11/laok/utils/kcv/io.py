#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2020/7/24 11:50:07

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
import os
import cv2
import numpy as np
from PIL import Image

from .convert import is_pil_image, pil2cv
#===============================================================================
# 
#===============================================================================

__all__ = ['read_cv_img', 'read_pil_img', 'read_sk_img', 'read_cv_gray', 'read_cv_video', 'write_cv_img']

def read_cv_img(file, flags = cv2.IMREAD_COLOR):
    return cv2.imdecode(np.fromfile(file, dtype=np.uint8), flags)

def read_cv_gray(file):
    return read_cv_img(file, cv2.IMREAD_GRAYSCALE)

def read_sk_img(file):
    import skimage

def read_pil_img(file):
    img = Image.open(file)
    return img

def write_cv_img(img_file, data, params=None):
    '''
    img_file : 保存路径
    img : 图片数据
    '''
    name, ext = os.path.splitext(img_file)
    retval, buf = cv2.imencode(ext, data, params)
    return buf.tofile(img_file)

def read_cv_video(fileOrId=0):
    '''fileOrId: 视频文件或者相机id
       ret: 迭代器,返回图像数据
    '''
    try:
        cap = cv2.VideoCapture(fileOrId)

        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()

            if not ret:
                break

            yield frame

    finally:
        # When everything done, release the capture
        cap.release()
