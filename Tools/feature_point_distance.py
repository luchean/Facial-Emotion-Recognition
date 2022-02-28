#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
描述：
    根据脸部特征点来计算关键帧的不同方法
Author: Gray_Gl
Last edited: February  2022
"""

from imutils import face_utils
import numpy as np
import imutils
import dlib
import cv2

# imutils中包含对各个特征点的标签
# FACIAL_LANDMARKS_IDXS = OrderedDict([
# 	("mouth", (48, 68)),
# 	("right_eyebrow", (17, 22)),
# 	("left_eyebrow", (22, 27)),
# 	("right_eye", (36, 42)),
# 	("left_eye", (42, 48)),
# 	("nose", (27, 35)),
# 	("jaw", (0, 17))
# ])

def o_distance(shape):
    '''
    通过传入的shape特征点，计算脸部主要器官关于中心特征点的相对位置移动和方向变化
    计算所有的点和中间点的欧氏距离和余弦距离，分别表示方向和距离的变化
    描述：
    :param shape:
    :return:
    '''
    for (name,(i,j)) in  face_utils.Face_LANDMARKS_IDXS.items():
        # name是部位的名称
        # (i,j)是各个部位的坐标

