#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2021/1/18 19:52:47

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
import torch as t
from laok.core.kprint import _kp_data, kprint
#===============================================================================
# 
#===============================================================================
@_kp_data.register_print(t.Tensor)
def _print_torch_arr(d, show_data = True):
    '''打印 torch array数据
    '''
    msg = str(f'-----id:{id(d)} type:{type(d)}\n'
              f'    device:{d.device}\n'
              f'    is_cuda:{d.is_cuda}\n'
              f'    is_leaf:{d.is_leaf}\n'
              f'    is_meta:{d.is_meta}\n'
              f'    is_mkldnn:{d.is_mkldnn}\n'
              f'    is_quantized:{d.is_quantized}\n'
              f'    is_sparse:{d.is_sparse}\n'
              f'    dtype:{d.dtype}\n'
              f'    layout:{d.layout}\n'
              f'    name:{d.name}\n'
              f'    requires_grad:{d.requires_grad}\n'
              f'    ndim:{d.ndim}\n'
              f'    shape:{d.shape}\n')
    if show_data:
        msg += f'{d.data}'
    return msg
