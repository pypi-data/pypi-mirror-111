#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2020/7/21 10:33:17

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
import re, os, sys
from PyQt5.QtWidgets import QWidget, QMainWindow
from PyQt5.uic import loadUi, compileUi
#===============================================================================
#
#===============================================================================

__all__ = ['DyUiMainWindow', 'DyUiWidget', 'compile_ui_file']

def _init_ui_file(obj):
    if hasattr(obj, 'ui_file'):
        ui_file = getattr(obj, 'ui_file')
    else:
        module_file = sys.modules[obj.__module__].__file__
        ui_file = os.path.splitext(module_file)[0] + ".ui"
    if not os.path.exists(ui_file):
        raise ValueError(f"you need config 'ui_file' in your class of[{obj.__class__}]")
    loadUi(ui_file, obj)  # 初始化Ui
    return ui_file

class DyUiMainWindow(QMainWindow):
    def __new__(cls, *args, **kwargs):
        obj = super(DyUiMainWindow, cls).__new__(cls)   # 构造对象
        QMainWindow.__init__(obj)                       # 调用父类
        _init_ui_file(obj)                              # 初始化ui
        return obj

class DyUiWidget(QWidget):
    def __new__(cls, *args, **kwargs):
        obj = super(DyUiWidget, cls).__new__(cls)   # 构造对象
        QWidget.__init__(obj)                       # 调用父类
        _init_ui_file(obj)                          # 初始化ui
        return obj


def compile_ui_file(ui_file, save_file=None):
    '''
        保存 X_ui.py 文件
    '''
    if save_file is None:
        save_file = os.path.splitext(ui_file)[0] + '_ui.py'
    with open(save_file, 'w', encoding='utf8') as f:
        compileUi(uifile=ui_file, pyfile=f)


# def dy_gen_ui_class(ui_file):
#     '''
#     根据 ui路径或者 _ui路径
#     :return:  返回 ui_class
#     '''
#     py_file = ui_file
#     if not ui_file.endswith('.ui'):
#         ui_file = os.path.splitext(ui_file)[0] + ".ui"
#
#     if uipath.endswith('.ui'):
#         pypath = uipath.replace('.ui', '_ui.py')
#         # 如果存在 ui文件,则编译UI
#         if os.path.exists(uipath):
#             with open(py_file, 'w', encoding='utf8') as f:
#                 uic.compileUi(uifile=uipath, pyfile=f)
#
#     # 开始动态导入 py 模块
#     ui_mod = dy_load_module(pypath)
#     for k in dir(ui_mod):
#         if k.startswith('Ui_'):
#             ui_class = getattr(ui_mod, k)
#             return ui_class
#     else:
#         raise RuntimeError("cannot find class Ui_*")
#
# class StaticUiMainWindow(QMainWindow):
#     def __new__(cls, *args, **kwargs):
#         obj = super(StaticUiMainWindow, cls).__new__(cls)   # 构造对象
#         QMainWindow.__init__(obj)                           # 调用父类
#         _init_ui_file(obj)                                  # 初始化ui
#         return obj
