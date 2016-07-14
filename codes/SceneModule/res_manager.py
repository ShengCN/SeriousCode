# -*- coding:utf-8 -*-

import SeriousTools.SeriousTools as SeriousTools
from ArchiveModule.archive_package import ArchivePackage

class ResManager(object):

    def __init__(self, resType):

        self._resType = resType
        self._resCount = 0
        self._resMap = dict()
        self._resPath = dict()

    """""""""""""""""
    加载资源,子类必须重写
    """""""""""""""""

    def load_res(self, resPath, extraResPath, _resId = None):

        # load the resource here
        res = None
        resId = None

        self._resCount += 1

        if _resId == None:

            resId = self._gen_resId()

        else:

            resId = _resId

        self._resMap[resId] = res
        self._resPath[resId] = [resPath, extraResPath]

        return res

    #####################

    # 生成资源ID
    def _gen_resId(self):

        return self._resType + str(self._resCount)

    """""""""""
    资源查询函数
    """""""""""
    # 根据资源ID获取资源
    def get_resId(self, res):

        return SeriousTools.find_key_in_dict(res, self._resMap)

    # 根据资源获取资源ID
    def get_res(self, resId):

        return SeriousTools.find_value_in_dict(resId, self._resMap)

    """""""""""""""""
    成员变量的get函数
    """""""""""""""""

    def get_resType(self):

        return self._resType

    def get_resCount(self):

        return self._resCount

    def get_resMap(self):

        return self._resMap

    def get_resPath(self):

        return self._resPath
