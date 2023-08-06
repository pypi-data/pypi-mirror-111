#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2021/3/18 00:22:29

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
import torch.optim as optim
#===============================================================================
# 
#===============================================================================

_optim_map = {
    'adam': optim.Adam,
    'SGD' : optim.SGD,
    'Adadelta': optim.Adadelta,
    'RMSprop':optim.RMSprop,
}

def get_optim(model, name, **kws):
    pass

    # if opt.optim == 'Adam':
    #     optimizer = optim.Adam(filter(lambda p: p.requires_grad, model.parameters()),
    #                            lr=opt.learning_rate,
    #                            betas=(opt.optim_alpha, opt.optim_beta),
    #                            eps=opt.optim_epsilon,
    #                            weight_decay=opt.weight_decay)
    # elif opt.optim == 'SGD':
    #     optimizer = optim.SGD(filter(lambda p: p.requires_grad, model.parameters()),
    #                           lr=opt.learning_rate,
    #                           momentum=opt.momentum)
    # elif opt.optim == "momSGD":
    #     optimizer = torch.optim.SGD(filter(lambda p: p.requires_grad, model.parameters()),
    #                                 lr=opt.learning_rate,
    #                                 momentum=opt.momentum)
    # elif opt.optim == 'Adadelta':
    #     optimizer = optim.Adadelta(filter(lambda p: p.requires_grad, model.parameters()),
    #                                lr=opt.learning_rate,
    #                                weight_decay=opt.weight_decay)
    # elif opt.optim == 'RMSprop':
    #     optimizer = optim.RMSprop(filter(lambda p: p.requires_grad, model.parameters()), lr=opt.learning_rate)
    # else:
    #     logging.error("Unknown optimizer: {}".format(opt.optim))
    #     raise Exception("Unknown optimizer: {}".format(opt.optim))
    #
    # # Load the optimizer
    # if opt.resume_from is not None:
    #     optim_path = os.path.join(opt.resume_from, "optimizer.pth")
    #     if os.path.isfile(optim_path):
    #         logging.info("Load optimizer from {}".format(optim_path))
    #         optimizer.load_state_dict(torch.load(optim_path))
    #         opt.learning_rate = optimizer.param_groups[0]['lr']
    #         logging.info("Loaded learning rate is {}".format(opt.learning_rate))
    #
    # return optimizer
