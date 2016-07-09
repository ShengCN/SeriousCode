# coding=utf-8
from math import *

class MathHelper(object):
    def __init__(self):
        pass
# 获得 Point3 的长度
    def get_length(self,point3):
        x = point3.getX()
        y = point3.getY()
        z = point3.getZ()
        return sqrt(x*x + y*y +z*z)