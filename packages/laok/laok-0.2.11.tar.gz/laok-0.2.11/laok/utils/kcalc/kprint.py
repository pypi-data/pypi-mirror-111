#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2021/3/17 20:14:56

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
import numpy as np
from laok.core.kprint import _kp_data, kprint
#===============================================================================
# 
#===============================================================================

@_kp_data.register_print(np.ndarray)
def _print_numpy_arr(d, show_data = True):
    '''打印 numpy array数据
    '''
    msg = str(f'-----id:{id(d)} type:{type(d)}\n'
              f'    flags:\n'
              f'          C_CONTIGUOUS:{d.flags.c_contiguous}\n'
              f'          F_CONTIGUOUS:{d.flags.f_contiguous}\n'
              f'          OWNDATA:{d.flags.owndata}\n'
              f'          WRITEABLE:{d.flags.writeable}\n'
              f'          ALIGNED:{d.flags.aligned}\n'
              f'          WRITEBACKIFCOPY:{d.flags.writebackifcopy}\n'
              f'          UPDATEIFCOPY:{d.flags.updateifcopy}\n'
              f'    shape:{d.shape}\n'
              f'    strides:{d.strides}\n'   
              f'    ndim:{d.ndim}\n'
              f'    size:{d.size}\n'
              f'    itemsize:{d.itemsize}\n'
              f'    nbytes:{d.nbytes}\n'
              f'    dtype:{d.dtype}\n')

    if d.size > 1:
        try:
            max, min = d.max(), d.min()
        except:
            max, min = None, None

        msg += str(f'    max:{max}\n'
                   f'    min:{min}\n')

    if show_data:
        msg += f'{d}'
    return msg
