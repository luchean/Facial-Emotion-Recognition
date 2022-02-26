#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
涉及所有处理json文件工具：包括将新导入的图片生成统一的json，
                        读取并修改对应json文件

Author: Gray_Gl
Last edited: February  2022
"""
from PIL import Image
import json
import os
import dlib
from imutils import face_utils
import numpy as np
import imutils
import cv2

# 加载与训练人脸检测的CNN模型
cnn_face_model = r"mmod_human_face_detector.dat"
cnn_face_detector = dlib.cnn_face_detection_model_v1(cnn_face_model)

# 加载人脸关键点检测模型
predictor_path = "shape_predictor_68_face_landmarks.dat"
predictor = dlib.shape_predictor(predictor_path)


def get_feature_point(
        image_path:str
):
    '''
    获取人脸中的特征点
    :param
        image:图片的具体路径
    :return:
        lsit:返回图片的所有的特征点
    '''

    # 加载图片并进行预处理，统一大小并转为灰度图片
    image = cv2.imread(image_path)
    image = imutils.resize(image,width=500)
    iamge_size = image.shape[:2]
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 检测灰度图片中的人脸
    # 这里指的是卷积层数
    rects = cnn_face_detector(image,1)

    # 遍历图片中检测出来的每一张人脸
    shape = []
    for (i, rect) in enumerate(rects):
        # 检测出人脸的面部器官区域，并将之转变为面部特征点
        shape = predictor(image, rect.rect)
        shape = face_utils.shape_to_np(shape)
    #
    #     ############################################
    #     # 下部分代码用可视化进行检查
    #     ############################################
    #     # 绘制在原图上
    #     (x,y,w,h) = face_utils.rect_to_bb(rect.rect)
    #     cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    #
    #     # 对脸进行编号
    #     cv2.putText(image, "Face #{}".format(i + 1), (x - 10, y - 10),
    #                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    #
    #     # 遍历所有的脸部特征点，并将之标注在图片上
    #     for (x, y) in shape:
    #         cv2.circle(image, (x, y), 1, (0, 0, 255), -1)
    # cv2.imshow("output",image)
    # cv2.waitKey(0)

    return shape,iamge_size


# 上传图片生成json文件
def gen_json_item_image(
        file_path:str,
        file_prefix:str
):
    '''
    对应json格式：
        "文件名（注意，这里是写相对路径）": {
        "recognition":0/1(0表示当前图片并没有被识别出来，1表示当前图片已经被识别出来)
        "image_size": (w,h)
        "boundingbox（这里切出来的人脸坐标）": [1,2,3,4,5,6,7,8],
        "label": "undersatanding",
        "feature_point(68个特征点)": [1,2,3,40],
        "feature_distance(特征距离)": []

    给出当前的图片所在文件夹的路径，默认是在当前文件中生成json文件
    :param
        file_prefix:项目在当前的主机中的绝对位置
        file_path:图片所在的文件所在当前项目中的位置
    :return:对应单条字典对，key：value
    '''

    # 声明result_all保存所有值
    result_all = dict()

    # 读取当前项目中的所有图片
    file_path_absolute = os.path.join(file_prefix,file_path)
    for file_path,dir_name,file_names in os.walk(file_path_absolute):
        for file in file_names:
            if file.endswith('.jpg'):

                # 获取文件相对路径，作为key保存
                key_file = os.path.join(file_path,file).replace(file_prefix,'')

                # 声名新的key-value键值对
                result = {key_file:{
                    "recognition":0,
                    "image_size":(0,0),
                    "boundingbox": [],
                    "label": "undersatanding",
                    "feature_point": [],
                    "feature_distance": 0
                     }
                }

                # 获取脸部bounding box和特征点
                shape,image_size = get_feature_point(os.path.join(file_path,file))
                result[key_file]['feature_point'] = shape.tolist()
                result[key_file]['image_size'] = image_size

                # 判定是否识别出对应脸部信息
                if len(shape) == 0:
                    result[key_file]["recognition"] = 0
                else:
                    result[key_file]["recognition"] = 1
                # 根据shape获取脸部边框
                    x_y_min = np.min(shape,axis = 0)
                    x_y_max = np.max(shape,axis = 0)
                    x_min = int(max(x_y_min[0]-10,0))
                    y_min = int(max(x_y_min[1]-10,0))
                    x_max = int(min(x_y_max[0]+10,image_size[0]))
                    y_max = int(min(x_y_max[1]+10,image_size[1]))
                    boundingbox = [[x_min,y_min],[x_min,y_max],[x_max,y_max],[x_max,y_max]]
                    result[key_file]["boundingbox"] = boundingbox

                    # 计算特征距离
                    result[key_file]["feature_distance"] = 0
            # 合并所有的字典
            result_all.update(result)

    # 在图片所在文件中保存对应路径
    json_path = os.path.join(file_prefix,file_path)
    json_path = json_path+'\\image.json'
    save_json(result_all,json_path)

    print("保存完成")

def save_json(source_dict,target_json):
    '''
    将source_dict保存到target_json对应路径中,将原来的文件进行覆盖
    :param source_dict:
    :param target_json:
    :return:
    '''
    with open(target_json,'w+') as f:
        json.dump(source_dict,f)


if __name__ == '__main__':
    # 遍历当前图片下的所有文件,生成统一的json文件
    file_path = r'dataset/Label3/new'
    file_prefix = r''























