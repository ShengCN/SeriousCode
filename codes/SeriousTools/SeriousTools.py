# -*- coding:utf-8 -*-

from panda3d.core import *

#####################

# 获取文件名后缀，如"models/demo.egg"的后缀为"egg"
# 如果该路径并没有写入后缀，则默认为egg文件
def get_filepath_suffix(filepath):

    if isinstance(filepath, str):

        dotIdx = filepath.rfind('.')

        if dotIdx <= 1:
            return "egg"

        return filepath[(dotIdx + 1):]

    return None

#####################

# 根据key查找字典中的value
def find_value_in_dict(key, _dict):

    if isinstance(_dict, dict):

        if key in _dict.keys():

            return _dict[key]

    return None

#####################

# 根据value查找其所对应的key
def find_key_in_dict(value, _dict):

    if isinstance(_dict, dict):

        for k, v in _dict.iteritems():

            if v == value:

                return k

    return None

#####################

# 创建一个空的NodePath
def empty_NP():

    return NodePath()

#####################

# 计算两点间的距离
def cal_distance(p1, p2):

    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2) ** 0.5

#####################

# 计算两个向量的余弦值
def cos(p1, p2):

    zero = Vec3(0, 0, 0)

    return (p1[0] * p2[0] + p1[1] * p2[1] + p1[2] * p2[2]) / (cal_distance(p1, zero) * cal_distance(p2, zero))

#####################

def extract_name_from_Id(Id):

    if isinstance(Id, str): #or isinstance(Id, unicode):

        name = ""

        for c in Id:

            if c.isalpha():

                name += c

            else:

                return name

        return name

    else:

        return None

