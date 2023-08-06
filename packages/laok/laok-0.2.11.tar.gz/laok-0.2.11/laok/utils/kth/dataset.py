#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2021/4/9 09:09:27

@author: laok
@copyright: Apache License, Version 2.0
'''
from torch.utils.data import DataLoader
import torchvision.datasets as datasets

# ===============================================================================
# 
# ===============================================================================
_vision_datasets = {
    'ImageFolder': { 'creator': datasets.ImageFolder },
    'MNIST': { 'creator': datasets.MNIST },
}


def _find_dataset(name):
    name = name.lower()
    for k,v in _vision_datasets.items():
        if k.lower() == name:
            return v


def get_dataset(name, **kws):
    _dataset = _find_dataset(name)
    if _dataset :
        return _dataset['creator'](**kws)


def get_dataset_loader(name):
    pass


