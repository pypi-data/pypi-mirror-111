#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2021/3/27 11:07:29

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
import torch
#===============================================================================
# 
#===============================================================================

def _guess_input(input):
    return input

def save_model(model, filename, input = None):
    '''保存 trace 模型,使用 eval模式固化执行路径;
    :param model: 模型
    :param filename: 文件
    :param input: 测试用例
    :return: trace 模型
    '''
    if isinstance(model, torch.jit.TracedModule):
        traced_model = model
    else:
        try:
            mode = model.training
            model.eval()
            traced_model = torch.jit.trace(model, input)
        finally:
            model.train(mode)

    traced_model.save(filename)
    return traced_model



def load_model(filename):
    ''' 加载 trace 模型
    :param filename: 模型文件
    :return: torch script model
    '''
    return torch.jit.load(filename)
