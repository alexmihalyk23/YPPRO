import os
import shutil
import PIL
import base64
import io
import numpy as np
import json
import subprocess

import yolov5.detect as detect
import yolov5.export as export

PRE_PATH = '/root/bot_lite'
VALID_DATA_PERCENTAGE = 0.2
BUSY = False


def train_yolo(path):
    global BUSY
    if BUSY is True:
        return False, '' # png_path
    epochs_n = 300 # get_epoch_n()
    proj_dir = PRE_PATH # os.path.join(PRE_PATH, path)
    weights = 'yolov5m_leaky.pt'
    batch = 16
    num_epochs = epochs_n
    result_dir = os.path.join(proj_dir,'train')
    data_dir = os.path.join(proj_dir, path)
    config_dir = os.path.join(data_dir,'custom.yaml')
    model_dir = os.path.join(PRE_PATH, 'yolov5/models/yolov5m.yaml')
    print(model_dir)
    #_, weights = model_scan(path) Всегда начинаем тренировку с 'yolov5m_leaky.pt'
    weights = 'yolov5m_leaky.pt'
    freeze = 10
    if not os.path.exists(data_dir+'valid/labels'):  os.makedirs(data_dir+'valid/labels')
    # if len(os.listdir(os.path.join(data_dir,'valid/labels'))) <= 1:
    #     return 'Добавьте ещё данных. Тренировка не была запущена.', '' # png_path
    BUSY = True
    savedPath = os.getcwd()
    os.chdir('/root/bot_lite/yolov5/')
    command = '/root/bot_lite/yolov5/train.py'
    params = f'--weights {weights} --data {config_dir} --cfg {model_dir} --batch {batch} --freeze {freeze} --epochs {num_epochs} --project {result_dir}'
    popen = subprocess.Popen('python3 '+ command +' ' +  params, executable='/bin/bash', shell=True)
    popen.wait()
    os.chdir(savedPath)
    BUSY = False
    png_path = os.path.join(result_dir, 'results.png')
    return True, png_path


def bestpt_copy():
    path = PRE_PATH #os.path.join(PRE_PATH, path)
    if os.path.isfile(os.path.join(path, 'best.pt')):
        os.remove(os.path.join(path, 'best.pt'))
    result_dir = os.path.join(path, 'train')
    exp = os.listdir(result_dir)
    if len(exp) == 0:
        return
    exp.sort()
    exp.sort(key=len)
    if '.ipynb' in exp[-1]:
        _ = exp.pop()
    exp = exp[-1]
    weights = os.path.join(result_dir, f'{exp}', 'weights', 'best.pt')
    shutil.copyfile(weights, path+'/best.pt')
    return


def pt2onnx(path):
    proj_dir = PRE_PATH #os.path.join(PRE_PATH, path)
    weights_path = os.path.join(proj_dir, 'best.pt')
    config_file = os.path.join(PRE_PATH, path, 'custom.yaml')
    opt = export.parse_opt()
    opt.weights = weights_path
    opt.data = config_file
    opt.opset = 11
    export.main(opt)
    onnx_path = os.path.join(proj_dir, 'best.onnx')
    return onnx_path

def onnx2tmfile():
    '''
        -f onnx 
        -m input model (best.onnx)
        -o output model (best.tmfile)

    '''
    proj_dir = PRE_PATH #os.path.join(PRE_PATH, path)
    onnx_path = os.path.join(proj_dir, 'best.onnx')
    tmfile_path = os.path.join(proj_dir, 'best.tmfile')
    args = ('/path/to/convert_tool/convert_tool',
                '-f', 'onnx',
                '-m', onnx_path,
                '-o', tmfile_path)
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()
    print('process', popen.returncode)
    return tmfile_path

def quantization(path):
    proj_dir = os.path.join(PRE_PATH, path)
    input_img = os.path.join(proj_dir, 'train', 'images') #'/path/to/img_calib'
    
    model_input_path = os.path.join(PRE_PATH, 'best.tmfile')
    model_output_path = os.path.join(PRE_PATH, 'best_int8.tmfile')

    args = ('/path/to/quant_tool/quant_tool_uint8',
                      '-m', model_input_path,
                      '-i', input_img,
                      '-o', model_output_path,
                      '-g', '3,352,352',
                      '-a', '0',
                      '-w', '0,0,0',
                      '-s', '0.003921,0.003921,0.003921',
                      '-c', '0',
                      '-t', '4',
                      '-b', '1',
                      '-k', '1',
                      '-y', '352,352'
                     )
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()
    return model_output_path