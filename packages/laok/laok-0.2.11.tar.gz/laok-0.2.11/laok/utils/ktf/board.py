#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2021/3/17 23:09:07

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
from tensorboardX import SummaryWriter
#===============================================================================
# pip install tensorboardX
# 启动服务器: tensorboard --logdir=<log_dir>
# 默认使用 http://localhost:6006/ 打开查看
#===============================================================================
DEFAULT_PATH = 'D:/AllInOne/DataRaw/TensorBoardX'
DEFAULT_PATH = r'D:\AllInOne\klibpy\algs\AREL\data\save\tensorboard\default'
def run_server(logdir=None, port=6006, host='localhost', reload_interval=5, bind_all=False, start_webbrowser=True):
    import sys
    if logdir is None:
        logdir = DEFAULT_PATH
    args = [f'--logdir={logdir}',
            f'--reload_interval={reload_interval}',
            f'--port={port}',
            f'--window_title={logdir}',
            ]
    if bind_all:
        args.append('--bind_all')
    else:
        args.append(f'--host={host}')

    sys.argv.extend(args)
    print(f'cmd={sys.argv}')

    if start_webbrowser:
        import webbrowser
        webbrowser.open(url=f'http://localhost:{port}')

    from tensorboard.main import run_main
    run_main()


def get_summary_writer(logdir=None, name='test'):
    '''获取 数据写入器
    :param name: 根据名字,自动写入到
    :return:
    '''
    if logdir is None:
        logdir = f'{DEFAULT_PATH}/{name}'
    return SummaryWriter(logdir=logdir)

if __name__ == '__main__':
    run_server()