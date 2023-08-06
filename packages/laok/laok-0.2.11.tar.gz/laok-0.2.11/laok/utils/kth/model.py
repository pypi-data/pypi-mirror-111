#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2021/3/27 11:21:00

@author: LiuKuan
@copyright: Apache License, Version 2.0
'''
import itertools, re, time
from functools import partial
import torch
import torchvision.models as tmodels
import torchvision.transforms as T
import PIL
from laok.core.kconfig import path_model as _path_model
import os.path
from laok.core.ktime import Timer
#===============================================================================
# 模型后缀一般是 .pt .pth
#===============================================================================
__all__ = ['save_model', 'load_model', 'save_model_params', 'load_model_params',
           'get_model_list', 'get_model_file', 'get_model']
############################################################### 模型加载和保存
def save_model(model, filename):
    '''该方式无需自定义网络模型，保存时已把网络结构保存
    :param model:   net model instance
    :param filename: model filename
    :return:
    '''
    torch.save(model, filename)

def load_model(filename):
    '''加载模型
    :param filename: 模型文件
    :return: 模型
    '''
    return torch.load(filename)

def save_model_params(model, filename):
    ''' 保存模型的参数
    :param model: 模型
    :param filename: 模型文件
    :return: None
    '''
    torch.save(model.state_dict(), filename)

def _state_dict_name_normal(state_dict):
    # '.'s are no longer allowed in module names, but previous _DenseLayer
    # has keys 'norm.1', 'relu.1', 'conv.1', 'norm.2', 'relu.2', 'conv.2'.
    # They are also in the checkpoints in model_urls. This pattern is used
    # to find such keys.
    pattern = re.compile(
        r'^(.*denselayer\d+\.(?:norm|relu|conv))\.((?:[12])\.(?:weight|bias|running_mean|running_var))$')
    for key in list(state_dict.keys()):
        res = pattern.match(key)
        if res:
            new_key = res.group(1) + res.group(2)
            state_dict[new_key] = state_dict[key]
            del state_dict[key]

def load_model_params(model, filename, replace_dot_name = False):
    '''加载模型参数
    :param model: 模型
    :param filename: 文件名字
    :param replace_dot_name: 替换模型层中.包含在名字中的层
    :return: 模型
    '''
    _obj = torch.load(filename)
    state_dict = None
    if isinstance(_obj, torch.nn.Module):
        state_dict = _obj.state_dict()
    elif isinstance(_obj, dict):
        state_dict = _obj

    if replace_dot_name and state_dict:
        _state_dict_name_normal(state_dict)
    # print('load ', filename)
    model.load_state_dict(state_dict)
    return model

############################################################### 模型仓库
# 默认缓冲在 C:\Users\user\.cache\torch\hub\checkpoints
_classify_models = {
    'alexnet': { 'creator': tmodels.alexnet, 'path' : 'alexnet-owt-4df8aa71.pth'},
    'densenet121':  { 'creator': tmodels.densenet121,'path' : 'densenet121-a639ec97.pth'},
    'densenet169': { 'creator': tmodels.densenet169,'path' : 'densenet169-b2777c0a.pth'},
    'densenet201': { 'creator': tmodels.densenet201,'path' : 'densenet201-c1103571.pth'},
    'densenet161': { 'creator': tmodels.densenet161,'path' : 'densenet161-8d451a50.pth'},
    'googlenet': { 'creator': partial(tmodels.googlenet,init_weights=False),'path' : 'googlenet-1378be20.pth'},
    'inception_v3_google': { 'creator': partial(tmodels.inception_v3,init_weights=False),'path' : 'inception_v3_google-1a9a5a14.pth'},
    'mnasnet0_5': { 'creator': tmodels.mnasnet0_5,'path' : 'mnasnet0.5_top1_67.823-3ffadce67e.pth'},
    'mnasnet0_75': { 'creator': tmodels.mnasnet0_75,'path' : ''},
    'mnasnet1_0': { 'creator': tmodels.mnasnet1_0,'path' : 'mnasnet1.0_top1_73.512-f206786ef8.pth'},
    'mnasnet1_3': { 'creator': tmodels.mnasnet1_3,'path' : ''},
    'mobilenet_v2': { 'creator': tmodels.mobilenet_v2,'path' : 'mobilenet_v2-b0353104.pth'},
    'mobilenet_v3_small': { 'creator': tmodels.mobilenet_v3_small,'path' : 'mobilenet_v3_small-047dcff4.pth'},
    'mobilenet_v3_large': { 'creator': tmodels.mobilenet_v3_large,'path' : 'mobilenet_v3_large-8738ca79.pth'},
    'resnet18': { 'creator': tmodels.resnet18,'path' : 'resnet18-5c106cde.pth'},
    'resnet34': { 'creator': tmodels.resnet34,'path' : 'resnet34-333f7ec4.pth'},
    'resnet50': { 'creator': tmodels.resnet50,'path' : 'resnet50-19c8e357.pth'},
    'resnet101': { 'creator': tmodels.resnet101,'path' : 'resnet101-5d3b4d8f.pth'},
    'resnet152': { 'creator': tmodels.resnet152,'path' : 'resnet152-b121ed2d.pth'},
    'resnext50_32x4d': { 'creator': tmodels.resnext50_32x4d,'path' : 'resnext50_32x4d-7cdf4587.pth'},
    'resnext101_32x8d': { 'creator': tmodels.resnext101_32x8d,'path' : 'resnext101_32x8d-8ba56ff5.pth'},
    'wide_resnet50_2': { 'creator': tmodels.wide_resnet50_2,'path' : 'wide_resnet50_2-95faca4d.pth'},
    'wide_resnet101_2': { 'creator': tmodels.wide_resnet101_2,'path' : 'wide_resnet101_2-32ee1156.pth'},
    'shufflenet_v2_x0_5': { 'creator': tmodels.shufflenet_v2_x0_5,'path' : 'shufflenetv2_x0.5-f707e7126e.pth'},
    'shufflenet_v2_x1_0': { 'creator': tmodels.shufflenet_v2_x1_0,'path' : 'shufflenetv2_x1-5666bf0f80.pth'},
    'shufflenet_v2_x1_5': { 'creator': tmodels.shufflenet_v2_x1_5,'path' : ''},
    'shufflenet_v2_x2_0': { 'creator': tmodels.shufflenet_v2_x2_0,'path' : ''},
    'squeezenet1_0': { 'creator': tmodels.squeezenet1_0,'path' : 'squeezenet1_0-a815701f.pth'},
    'squeezenet1_1': { 'creator': tmodels.squeezenet1_1,'path' : 'squeezenet1_1-f364aa15.pth'},
    'vgg11': { 'creator': tmodels.vgg11,'path' : 'vgg11-bbd30ac9.pth'},
    'vgg13': { 'creator': tmodels.vgg13,'path' : 'vgg13-c768596a.pth'},
    'vgg16': { 'creator': tmodels.vgg16,'path' : 'vgg16-397923af.pth'},
    'vgg19': { 'creator': tmodels.vgg19,'path' : 'vgg19-dcbb9e9d.pth'},
    'vgg11_bn': { 'creator': tmodels.vgg11_bn,'path' : 'vgg11_bn-6002323d.pth'},
    'vgg13_bn': { 'creator': tmodels.vgg13_bn,'path' : 'vgg13_bn-abd245e5.pth'},
    'vgg16_bn': { 'creator': tmodels.vgg16_bn,'path' : 'vgg16_bn-6c64b313.pth'},
    'vgg19_bn': { 'creator': tmodels.vgg19_bn,'path' : 'vgg19_bn-c79401a0.pth'},
}

_detection_models = {
    'fasterrcnn_mobilenet_v3_large_320_fpn': {'creator': tmodels.alexnet, 'path': 'fasterrcnn_mobilenet_v3_large_320_fpn-907ea3f9.pth'},
    'fasterrcnn_mobilenet_v3_large_fpn': {'creator': tmodels.alexnet, 'path': 'fasterrcnn_mobilenet_v3_large_fpn-fb6a3cc7'},
    'fasterrcnn_resnet50_fpn': {'creator': tmodels.alexnet, 'path': 'fasterrcnn_resnet50_fpn_coco-258fb6c6.pth'},
    'keypointrcnn_resnet50_fpn': {'creator': tmodels.alexnet, 'path': 'keypointrcnn_resnet50_fpn_coco-fc266e95.pth'},
    'maskrcnn_resnet50_fpn_coco': {'creator': tmodels.alexnet, 'path': 'maskrcnn_resnet50_fpn_coco-bf2d0c1e.pth'},
    'retinanet_resnet50_fpn_coco': {'creator': tmodels.alexnet, 'path': 'retinanet_resnet50_fpn_coco-eeacb38b.pth'},
}


# def _segmentation_load_weights(model, arch_type, backbone, progress):
#     arch = arch_type + '_' + backbone + '_coco'
#     model_url = model_urls.get(arch, None)
#     if model_url is None:
#         raise NotImplementedError('pretrained {} is not supported as of now'.format(arch))
#     else:
#         state_dict = load_state_dict_from_url(model_url, progress=progress)
#         model.load_state_dict(state_dict)
#
# tmodels.segmentation._load_weights = _segmentation_load_weights

_segmentation_models = {
    'deeplabv3_mobilenet_v3_large': {'creator': tmodels.segmentation.deeplabv3_mobilenet_v3_large, 'path': 'deeplabv3_mobilenet_v3_large-fc3c493d.pth'},
    'deeplabv3_resnet50': {'creator': tmodels.segmentation.deeplabv3_resnet50, 'path': 'deeplabv3_resnet50_coco-cd0a2569.pth'},
    'deeplabv3_resnet101': {'creator': tmodels.segmentation.deeplabv3_resnet101, 'path': 'deeplabv3_resnet101_coco-586e9e4e.pth'},
    'fcn_resnet50': {'creator': tmodels.segmentation.fcn_resnet50, 'path': 'fcn_resnet50_coco-1167a1af.pth'},
    'fcn_resnet101': {'creator': tmodels.segmentation.fcn_resnet101, 'path': 'fcn_resnet101_coco-7ecb50ca.pth'},
    'lraspp_mobilenet_v3_large': {'creator': tmodels.segmentation.lraspp_mobilenet_v3_large, 'path': 'lraspp_mobilenet_v3_large-d234d4ea.pth'},
}

_video_models = {
    'mc3_18': {'creator': tmodels.alexnet, 'path': 'mc3_18-a90a0ba3.pth'},
    'r2plus1d_18': {'creator': tmodels.alexnet, 'path': 'r2plus1d_18-91a641e6.pth'},
    'r3d_18': {'creator': tmodels.alexnet, 'path': 'r3d_18-b3b3357e.pth'},
}

_quantization_models = {
    'googlenet_fbgemm': {'creator': tmodels.alexnet, 'path': 'googlenet_fbgemm-c00238cf.pth'},
    'inception_v3_google_fbgemm': {'creator': tmodels.alexnet, 'path': 'inception_v3_google_fbgemm-71447a44.pth'},
    'mobilenet_v2_qnnpack': {'creator': tmodels.alexnet, 'path': 'mobilenet_v2_qnnpack_37f702c5.pth'},
    'resnet18_fbgemm': {'creator': tmodels.alexnet, 'path': 'resnet18_fbgemm_16fa66dd.pth'},
    'resnet50_fbgemm': {'creator': tmodels.alexnet, 'path': 'resnet50_fbgemm_bf931d71.pth'},
    'resnext101_32x8_fbgemm': {'creator': tmodels.alexnet, 'path': 'resnext101_32x8_fbgemm_09835ccf.pth'},
    'shufflenetv2_x1_fbgemm': {'creator': tmodels.alexnet, 'path': 'shufflenetv2_x1_fbgemm-db332c57.pth'},
}

def get_model_list(model_type = None):
    '''
    :param model_type: 'classify','detection','segmentation', 'video', 'quantization',None
    :return:
    '''
    model_type_list = []

    if model_type is not None:
        model_type = model_type.lower()

    if model_type is None:
        model_type_list.extend([_classify_models, _detection_models, _segmentation_models, _video_models, _quantization_models])
    elif model_type == 'classify':
        model_type_list.append(_classify_models)
    elif model_type == 'detection':
        model_type_list.append(_detection_models)
    elif model_type == 'segmentation':
        model_type_list.append(_segmentation_models)
    elif model_type == 'video':
        model_type_list.append(_video_models)
    elif model_type == 'quantization':
        model_type_list.append(_quantization_models)
    for k in itertools.chain(*model_type_list):
        yield k

def get_model_file(model_name):
    fpath = None
    model_name = model_name.lower()
    if model_name in _classify_models:
        fpath = _path_model('Torch/classify/' + _classify_models[model_name]['path'])
    elif model_name in _detection_models:
        fpath = _path_model('Torch/detection/' + _detection_models[model_name]['path'])
    elif model_name in _segmentation_models:
        fpath = _path_model('Torch/segmentation/' + _segmentation_models[model_name]['path'])
    elif model_name in _video_models:
        fpath = _path_model('Torch/video/' + _video_models[model_name]['path'])
    elif model_name in _quantization_models:
        fpath = _path_model('Torch/quantization/' + _quantization_models[model_name]['path'])
    if fpath and os.path.isfile(fpath):
        return fpath

def get_model(model_name, load_params = True, **kws):
    ctor = None
    model_name = model_name.lower()
    if model_name in _classify_models:
        ctor = _classify_models[model_name]['creator']
    elif model_name in _detection_models:
        ctor = _detection_models[model_name]['creator']
    elif model_name in _segmentation_models:
        ctor = _segmentation_models[model_name]['creator']
    elif model_name in _video_models:
        ctor = _video_models[model_name]['creator']
    elif model_name in _quantization_models:
        ctor = _quantization_models[model_name]['creator']

    if ctor is None:
        return

    model = ctor()
    if load_params:
        model_file = get_model_file(model_name)
        if model_file:
            replace_dot_name = 'densenet' in model_name
            load_model_params(model, model_file, replace_dot_name= replace_dot_name)
    return model

############################################################### 模型训练和测试
# model.train() ：启用 BatchNormalization 和 Dropout
# model.eval() ：不启用 BatchNormalization 和 Dropout


def get_device():
    return torch.device("cuda:0" if _g_has_cuda else "cpu")

_g_has_cuda = torch.cuda.is_available()
_g_device = get_device()

def transform_image_eval():
    return T.Compose([T.Resize(256),
                      T.CenterCrop(224),
                      T.ToTensor(),
                      T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])

def transform_image_train():
    return T.Compose([
        T.RandomResizedCrop(size=256, scale=(0.8, 1.0)),
        T.RandomRotation(degrees=15),
        T.RandomHorizontalFlip(),
        T.CenterCrop(size=224),
        T.ToTensor(),
        T.Normalize([0.485, 0.456, 0.406],
                    [0.229, 0.224, 0.225])])

def inference_image_classify(img, model, classes = None, topk=1, transform = None, device = None):
    if isinstance(img, str):
        _img = PIL.Image.open(img).convert('RGB')
        if transform is None:
            transform = transform_image_eval()
    else:
        _img = img

    if transform == 'default':
        transform = transform_image_eval()

    img_t = transform(_img) if transform else _img
    batch_t =  torch.unsqueeze(img_t, 0) if img_t.dim() == 3 else img_t

    # Validation - No gradient tracking needed
    with torch.no_grad():
        model.eval()

        if _g_has_cuda and device is None:
            model = model.to(_g_device)
            batch_t = batch_t.to(_g_device)

        t1 = time.time()
        out = model(batch_t)
        t2 = time.time()

    percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100
    values, indices = torch.sort(out, descending=True)

    ret = []
    for i in range(topk):
        idx = indices[0][i].item()
        val = values[0][i].item()
        score = percentage[idx].item()
        label = classes[idx] if classes and idx < len(classes) else ''
        obj = {
            'index':idx,
            'value': val ,
            'label': label,
            'score': score,
            'inference_time':  f"{1000* (t2-t1):.6}(ms)"
        }

        if isinstance(img, str):
            obj['file'] = os.path.basename(img)
        ret.append(obj)
    return ret

def model_train():
    pass

def model_validate():
    pass

def model_inference():
    pass

def model_inference_image_classify():
    pass


def train(data_loader, model, optimizer = None, criterion = None, epoches = 10, batches_display=100, device = None):
    '''训练模型的基本步骤
    :param data_loader:
    :param model:
    :param optimizer:
    :param criterion:
    :param epoches:
    :param batches_display:
    :param device:
    :return:
    '''
    if criterion is None:
        criterion = torch.nn.CrossEntropyLoss()

    if optimizer is None:
        optimizer = torch.optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

    if _g_has_cuda and device is None:
        print('=====Convert to [cuda] device')
        model.to(_g_device)

    if device:
        model.to(_g_device)

    print('======Trainning start....')
    totalTimer = Timer()
    batchTimer = Timer()
    for epoch in range(epoches):  # loop over the dataset multiple times
        running_loss = 0.0

        sampleCount = 0
        batchTimer.restart()
        for i, data in enumerate(data_loader, 0):
            # get the inputs; data is a list of [inputs, labels]
            inputs, targets = data
            sampleCount += inputs.size(0)

            if _g_has_cuda and device is None:
                inputs, targets = inputs.to(_g_device), targets.to(_g_device)

            if device:
                inputs, targets = inputs.to(_g_device), targets.to(_g_device)

            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            outputs = model(inputs)
            loss = criterion(outputs, targets)

            loss.backward()
            optimizer.step()

            # print statistics
            running_loss += loss.item()
            if i % batches_display == (batches_display-1):  # print every 2000 mini-batches
                print('[Ep:%d,%d] loss: %.6f time:%.6f(s)' %
                      (epoch + 1, i + 1, running_loss/sampleCount, batchTimer.elapse()))
                running_loss = 0.0
                sampleCount = 0
                batchTimer.restart()

    print('======Trainning finished, cosume time:%.6f(s)....' % totalTimer.elapse())

def eval_classify(data_loader, model, classes, topk=1, device = None):
    class_correct = list(0. for i in classes)
    class_total = list(0. for i in classes)

    if _g_has_cuda and device is None:
        model.to(_g_device)
    model.eval()

    for data in data_loader:
        inputs, targets = data

        if _g_has_cuda and device is None:
            inputs, targets = inputs.to(_g_device), targets.to(_g_device)

        outputs = model(inputs)
        _, predicted = torch.max(outputs, topk)
        c = (predicted == targets).squeeze()

        for i,target in enumerate(targets):
            class_correct[target] += c[i].item()
            class_total[target] += 1

    correct_total = 0
    total = 0.0
    for i,cls in enumerate(classes):
        correct_total += class_correct[i]
        total += class_total[i]
        if class_total[i]:
            percent = 100 * class_correct[i] / class_total[i]
        else:
            percent = 0
        print('Accuracy of %5s : %2d %%' % (cls, percent))
    print('Final Accuracy : %2d %%' % (correct_total/total * 100) )