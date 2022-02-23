#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
涉及所有处理json文件工具：包括将新导入的图片生成统一的json，
                        读取并修改对应json文件

Author: Gray_Gl
Last edited: February  2022
"""

# 将原来的图片生成对应json信息，统一记录在一个json文件中
def GenJson(
        filename:str
):
    '''
    对应json格式：
        "文件名（注意，这里是写相对路径）": {
        "image_h": 12,
        "image_w": 23,
        "boundingbox（这里切出来的人脸坐标）": [1,2,3,4,5,6,7,8],
        "label": "undersatanding",
        "feature_point(68个特征点)": [1,2,3,40],
        "feature_distance(特征距离)": []
    将获取的图片，根据图片的信息生成对应json信息，如果当前暂时为空置为none
    :return:对应单条字典对，key：value
    '''
    # 获取文件的名称

    # 获取文件的长宽

    # 获取文件特征点


