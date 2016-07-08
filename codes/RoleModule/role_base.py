# -*- coding:utf-8 -*-

import SeriousTools.SeriousTools as SeriousTools

from direct.showbase.DirectObject import DirectObject

class Role(DirectObject):

    _currState = None

    def __init__(self,
                 roleId,
                 modelId,
                 ableToTalk,
                 ableToCtrl,
                 ableToAtck,
                 ):

        DirectObject.__init__(self)

        self._roleAttr = dict()
        self._eventHandleMap = dict()

        self._roleAttr["roleId"] = roleId
        self._roleAttr["modelId"] = modelId         # 角色模型ID
        self._roleAttr["ableToTalk"] = ableToTalk   # 角色能否交流
        self._roleAttr["ableToCtrl"] = ableToCtrl   # 角色能否被玩家控制
        self._roleAttr["ableToAtck"] = ableToAtck   # 角色能否攻击
        self._roleAttr["states"] = []

    #########################################

    """""""""""""""
    状态属性管理函数
    """""""""""""""

    def add_state(self, state):

        self._roleAttr["states"].append(state)

    def set_curr_state(self, state):

        self._currState = state

    def get_curr_state(self):

        return self._currState

    # 添加角色属性以及其对应值
    def append_role_attr(self, key, value):

        if key in self._roleAttr.keys():

            print "the key '%s' in roleAttr is already existed" % key

        else:

            self._roleAttr[key] = value

    """""""""""""""""""""
    成员变量的get和set函数
    """""""""""""""""""""

    # 设置属性值
    def set_attr_value(self, key, value):

        if key not in self._roleAttr.keys():

            print "the key '%s' is not in roleAttr" % key

        else:

            self._roleAttr[key] = value

    #########################################

    # 获取属性值
    def get_attr_value(self, key):

        return SeriousTools.find_value_in_dict(key, self._roleAttr)

    #########################################

    # 获取所有属性
    def get_all_attr(self):

        return self._roleAttr

    # 判断角色是否含有某个属性
    def has_attr(self, attr):

        return self._roleAttr.has_key(attr)

    """""""""""""""""""""""
    信息打印函数，主要用于调试
    """""""""""""""""""""""

    # 打印出所有属性以及其对应值
    def print_all_attr(self):

        print "-- Attribute of Role '%s' --" % self._roleAttr["roleId"]

        for key in sorted(self._roleAttr.keys()):

            print "key:%s, value:%s" % (key, self._roleAttr[key])

        print "-------------------------"