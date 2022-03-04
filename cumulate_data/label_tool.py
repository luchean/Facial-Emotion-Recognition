#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
根据已经生成json进行，标注，修改内容都是原来的json文件
注意：需要先将上传的图片生成对应json文件，才可以通过方法进行标注

Author: Gray_Gl
Last edited: February  2022
"""
import json
import os
from Tools.DataTool.GenJson import save_json
import cv2

def label_image(
    json_file:str,
    path_prefix:str
):
    '''
    根据json文件找到对应的图片进行标注，注意图片都已经是通过关键帧提取转存为了json格式
    :param json_file: json文件的路径，绝对路径或者相对路径都可以
    :param path_prefix: 单项数据的前缀文件，字典中都是从当前项目中出发的相对路径
    :return:
    '''
    # 读取并遍历json中每一个数据
    with open(os.path.join(path_prefix,json_file),'r') as f:
        data_json = json.load(f)
    print("0 is confused")
    print("1 is distracted")
    print("2 is listening")
    print("3 is tired")
    print("4 is understanding")
    print("5 表示未知")

    for key in data_json:
        # 打开对应文件
        print(key)
        print(path_prefix)
        file_path =path_prefix + key
        print(os._exists(key))
        img = cv2.imread(file_path)
        cv2.imshow('image',img)
        k = cv2.waitKey(0)
        cv2.destroyAllWindows()

        # 根据分类进行标记
        if k == 48:
            # confused类
            data_json[key]['label'] = 'confused'
        elif k == 49:
            # distracted类
            data_json[key]['label'] = 'distracted'
        elif k == 50:
            # listening类
            data_json[key]['label'] = 'listening'
        elif k == 51:
            # tired类
            data_json[key]['label'] = 'tired'
        elif k == 52:
            # understanding类
            data_json[key]['label'] = 'understanding'
        elif k == 53:
            # 未知
            data_json[key]['label'] = 'unknown'

    # 将数据保存到原来的json文件中
    with open(json_file, 'w+') as f:
        json.dump(data_json,f)


if __name__ == '__main__':
    label_image(r'dataset/Label3/new/image.json',
                r'C:\Users\gray\Desktop\FacialEmotion\Facial-Emotion-Recognition')