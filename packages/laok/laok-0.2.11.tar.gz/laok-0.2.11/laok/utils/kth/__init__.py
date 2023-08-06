#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2021/4/9 09:09:27

@author: laok
@copyright: Apache License, Version 2.0
'''


# ===============================================================================
#
# ===============================================================================

def after_conv_size(size, kernel_size, stride = 1, padding = 0):
    return (size - kernel_size + 2 * padding)/stride + 1

