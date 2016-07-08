# -*- coding:utf-8 -*-

from res_manager import ResManager
import SeriousTools.SeriousTools as SeriousTools
from ArchiveModule.archive_package import ArchivePackage

from panda3d.core import GeoMipTerrain

class TerrainManager(ResManager):

    def __init__(self, resType = "terrain"):

        ResManager.__init__(self, resType)

        self.__currTerraId = None

        self.__arcPkg = ArchivePackage(arcPkgName = "terrain",
                                       itemsName = [
                                           "terrainId",
                                           "heightfieldPath",
                                           "colormapPath",
                                           "pos",
                                           "hpr",
                                           "scale",
                                           "parentId"
                                       ])

        self.__arcPkg.append_metaData("currTerraId")

    #########################################

    # 加载地形资源
    def load_res(self,
                 resPath,
                 extraResPath,
                 _resId = None):

        self._resCount += 1

        resId = None

        if _resId == None:

            resId = self._gen_resId()

        else:

            resId = _resId

        self.__currTerraId = resId

        res = GeoMipTerrain(resId)

        res.setHeightfield(resPath)
        res.setColorMap(extraResPath)

        self._resMap[resId] = res
        self._resPath[resId] = [resPath, extraResPath]

        return res

    #########################################

    # 设置当前所使用的地形
    def set_currTerrain(self, terrainId):

        self.__currTerraId = terrainId

        for id in self._resMap.keys():

            if id == self.__currTerraId:

                self._resMap[id].getRoot().show()

            else:

                self._resMap[id].getRoot().hide()

    #########################################

    def get_currTerrain(self):

        return self.__currTerraId

    # 更新地形
    def update_terrain(self, task):

        # task.setTaskChain("terraTaskChain")
        #
        # self._resMap[self.__currTerraId].update()

        return task.cont

    def get_arcPkg(self):

        return self.__arcPkg



