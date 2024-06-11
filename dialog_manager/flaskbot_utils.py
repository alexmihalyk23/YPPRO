import os
import shutil
import PIL
import base64
import io
import numpy as np
import json
import subprocess
import random

import yolov5.detect as detect
import yolov5.export as export

PRE_PATH = os.getcwd()
VALID_DATA_PERCENTAGE = 0.2
BUSY = False


def train_yolo(path, epochs_n=2, res=448):
    global BUSY
    if BUSY is True:
        return False, '' # png_path
    
    proj_dir = PRE_PATH # os.path.join(PRE_PATH, path)
    weights = 'yolov5m_leaky.pt'
    batch = 2
    num_epochs = epochs_n
    result_dir = os.path.join(proj_dir,'train')
    data_dir = os.path.join(proj_dir, path)
    config_dir = os.path.join(data_dir,'data.yaml')
    new_lines = [
    'train: ../dataset/train/images\n',
    'val: ../dataset/valid/images\n',
    'test: ../dataset/test/images\n']

# Read the contents of the file
    with open(os.path.join(data_dir, 'data.yaml'), 'r') as file:
        lines = file.readlines()

# Replace the first three lines with the new lines
    lines[:3] = new_lines

# Write the modified lines back to the file
    with open(os.path.join(data_dir, 'data.yaml'), 'w') as file:
        file.writelines(lines)

    model_dir = os.path.join(PRE_PATH, 'yolov5/models/yolov5m.yaml')
    #_, weights = model_scan(path) Всегда начинаем тренировку с 'yolov5m_leaky.pt'
    weights = '../yolov5m_leaky.pt'
    freeze = 10
    if not os.path.exists(data_dir+'valid/labels'):  os.makedirs(data_dir+'valid/labels')
    # if len(os.listdir(os.path.join(data_dir,'valid/labels'))) <= 1:
    #     return 'Добавьте ещё данных. Тренировка не была запущена.', '' # png_path
    BUSY = True
    savedPath = os.getcwd()
    os.chdir(os.getcwd()+'/yolov5/')
    command = os.getcwd()+'/train.py'
    params = f'--weights {weights} --data {config_dir} --imgsz {res} --cfg {model_dir} --batch {batch} --freeze {freeze} --epochs {num_epochs} --project {result_dir}'
    popen = subprocess.Popen('python3 '+ command +' ' +  params, executable='/bin/bash', shell=True)
    popen.wait()
    os.chdir(savedPath)
    BUSY = False
    png_path = os.path.join(result_dir, 'results.png')
    return True, png_path
def check_model(path, conf=0.1, res=448):
    
    weights_path = os.path.join(PRE_PATH, 'best.pt')
    test_images_dir = os.path.join(PRE_PATH, path, 'test/images')
    source = os.path.join(PRE_PATH, 'data/images')  # Path to images for testing
    os.chdir(os.getcwd()+'/yolov5')
    command = os.getcwd()+'/detect.py'
    result_path = os.path.join(PRE_PATH, 'detect_results')
    img = random.choice(os.listdir(test_images_dir))
    params = f'--weights {weights_path} --source {test_images_dir}/{img} --imgsz {res} --project {result_path}  --conf-thres {conf}'
    popen = subprocess.Popen('python3 '+ command +' ' +  params, executable='/bin/bash', shell=True)
    popen.wait()
    os.chdir(PRE_PATH)
    exp = os.listdir(result_path)
    print(exp)
    if len(exp) == 0:
        return
    exp.sort()
    exp.sort(key=len)
    exp = exp[-1]
    # # Return path to results or other relevant info
    results_path = os.path.join("detect_results", f"{exp}") + f"/{img}"
    print(results_path)
    return results_path


def bestpt_copy():
    path = PRE_PATH+'/dataset' #os.path.join(PRE_PATH, path)
    if os.path.isfile(os.path.join(path, 'best.pt')):
        os.remove(os.path.join(path, 'best.pt'))
    result_dir = PRE_PATH+'/train' #result_dir = os.path.join(path, 'train')

    exp = os.listdir(PRE_PATH+'/train')
    print(exp)
    if len(exp) == 0:
        return
    exp.sort()
    exp.sort(key=len)
    # sorted_subdirectories = sorted(filtered_subdirectories, reverse=True)
    # latest_folder = sorted_subdirectories[0]

    if '.ipynb' in exp[-1]:
        _ = exp.pop()
    exp = exp[-1]
    weights = os.path.join(result_dir, f'{exp}', 'weights', 'best.pt')
    shutil.copyfile(weights, PRE_PATH+'/best.pt')
    return


def pt2onnx(path):
    proj_dir = PRE_PATH #os.path.join(PRE_PATH, path)
    # weights_path = os.path.join(proj_dir, 'best.pt')
    # config_file = os.path.join(PRE_PATH, path, 'custom.yaml')
    # opt = export.parse_opt()
    # opt.weights = weights_path
    # opt.data = config_file
    # opt.opset = 11
    # export.main(opt)
    onnx_path = os.path.join(proj_dir, 'best.pt')
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
    args = (PRE_PATH+'/convert_tool/convert_tool',
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

    args = (PRE_PATH+'/quant_tool/quant_tool_uint8',
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
