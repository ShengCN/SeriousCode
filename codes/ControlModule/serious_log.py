# coding=utf-8
#
# Serious 项目的日志模块
# 主要用来调试程序,进行系统状态的追踪
# 编写人: Jason Sheng
# 最新更新日期: 2016.6.21
#

import logging
import logging.handlers
from direct.stdpy.file import *


class SeriousLog(object):

    @property
    def file_name(self):
        return self.__file_name

    @file_name.setter
    def file_name(self,file_name):
        self.__file_name = file_name

    # 初始化函数
    # IN: 希望日志记录的文件的文件名称
    def __init__(self,file_name):
        self.file_name = file_name

    # 日志函数
    # IN：level--显示的错误等级（分为info,warn,error三个等级,使用字符串即可） content--希望显示的日志信息内容（字符串）
    def log(self,level,content):
        log_file = self.__file_name

        handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=5)
        fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'

        formatter = logging.Formatter(fmt)  # 实例化formatter
        handler.setFormatter(formatter)

        logger = logging.getLogger(level)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

        logger.debug(content)

