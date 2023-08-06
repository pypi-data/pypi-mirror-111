#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2020/7/24 11:59:16

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
import cv2
import numpy as np
from .convert import is_pil_image, pil2cv
#===============================================================================
# 
#===============================================================================

__all__ = ['show_img', 'wait_escape']


def show_img(img, winName='test', w=0, interpolation=cv2.INTER_LINEAR):
    '''
    :param winName: 窗口名字
    :param img: 图片数据
    :param w: 窗口宽度
    :param interpolation:
    :return:
    '''
    if img is None:
        return

    if is_pil_image(img):
        img = pil2cv(img)

    if img.dtype in [np.bool]: #转换bool 类型
        img = img.astype(np.uint8) * 255

    elif img.dtype not in [np.uint8, ]:  #转换 其它类型
        maxV = img.max()
        if 0 < maxV <= 1.0:  #如果是浮点类型
            img = img * 255

        img = img.astype(np.uint8)

    # 将尺寸放缩
    if w != 0:
        _h, _w = img.shape[:2]

        if w == -1:
            w = 1200 if _w > 1200 else _w

        h = 1.0 * _h * w / _w

        showImg = cv2.resize(img, dsize=(int(w), int(h)), interpolation=interpolation)
    else:
        showImg = img

    # 显示
    cv2.imshow(winName, showImg)


def wait_escape(delay=0, closeWindow=False):
    ''' delay: 延时 (ms)
        closeWindow:是否关闭窗口
    '''
    try:
        key = cv2.waitKey(delay)
        if key == 27:#退出
            cv2.destroyAllWindows()
            raise SystemExit
        return key
    finally:
        if closeWindow:
            cv2.destroyAllWindows()