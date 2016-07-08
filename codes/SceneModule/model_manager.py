# -*- coding:utf-8 -*-

from res_manager import ResManager
from ArchiveModule.archive_package import ArchivePackage

from direct.showbase.Loader import Loader

class ModelManager(ResManager):

    def __init__(self, resType = "model"):

        ResManager.__init__(self, resType)

        self.__loader = Loader(self)

        self.__arcPkg = ArchivePackage(arcPkgName = "model",
                                       itemsName = [
                                           "modelId",
                                           "modelPath",
                                           "pos",
                                           "hpr",
                                           "scale",
                                           "parentId"
                                       ])

    #########################################

    # 加载静态模型
    def load_res(self,
                 resPath,
                 extraResPath = None,
                 _resId = None):

        res = self.__loader.loadModel(resPath)
        resId = None

        self._resCount += 1

        if _resId == None:

            resId = self._gen_resId()

        else:

            resId = _resId

        self._resMap[resId] = res
        self._resPath[resId] = resPath

        return res

    #########################################

    def get_arcPkg(self):

        return self.__arcPkg