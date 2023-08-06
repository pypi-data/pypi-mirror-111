#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2020/6/5 17:49:37

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
from PyQt5.QtWidgets import QApplication, QWidget
import sys, inspect

from .ui import *
#===============================================================================
#
#===============================================================================

def qt_run(widget = None, before_run_func = None, after_run_func = None,  *args, **kwargs):

    try:
        app = QApplication(sys.argv)

        if before_run_func:
            before_run_func()

        win = widget
        if inspect.isclass(widget) or inspect.isfunction(widget):
            win = widget(*args, **kwargs)

        if isinstance(win, QWidget):
            win.show()

        ret = app.exec_()

        if after_run_func:
            after_run_func()

        sys.exit(ret)

    except Exception as e:
        import traceback
        traceback.print_exc()