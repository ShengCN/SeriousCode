# -*- coding:utf-8 -*-

from ArchiveModule.archive_package import ArchivePackage

from panda3d.core import AmbientLight
from panda3d.core import DirectionalLight
from panda3d.core import PointLight
from panda3d.core import Spotlight
from panda3d.core import Light
from panda3d.core import NodePath
from panda3d.core import PerspectiveLens

AMBIENT_LIGHT     = "AmbientLight"
DIRECTIONAL_LIGHT = "DirectionalLight"
POINT_LIGHT       = "PointLight"
SPOT_LIGHT        = "SpotLight"

class LightController(object):

    def __init__(self):

        self.__lightType = [ AMBIENT_LIGHT,
                             DIRECTIONAL_LIGHT,
                             POINT_LIGHT,
                             SPOT_LIGHT ]

        self.__ambientCount = 0
        self.__directionalCount = 0
        self.__pointCount = 0
        self.__spotCount = 0

        self.__lightMap = dict()

        self.__lightParentId = dict()

        self.__targetMap = dict()

        self.__setorMap = dict()

        self.__sceneMgr = None

        self.__arcPkg = ArchivePackage(arcPkgName = "light",
                                       itemsName = [
                                           "lightId",
                                           "color",
                                           "Pos",
                                           "Hpr",
                                           "targetId",
                                           "setorId",
                                           "parentId"
                                       ])

    """""""""""
    各类灯光的创建
    """""""""""

    # 需要创建光源实例，并且封装为NodePath
    def create_light(self,
                     lightType,
                     lightColor,
                     parentId,
                     _lightId = None,
                     lightPos = None,
                     lightHpr = None,
                     shadow = False,
                     targetId = None
                     ):

        lightNP = None
        lightId = ""

        # Ambient Light
        if lightType == self.__lightType[0]:

            self.__ambientCount += 1

            if _lightId == None:

                lightId += (lightType + str(self.__ambientCount))

            else:

                lightId = _lightId

            lightNP = self.__create_ambient_light(lightId, lightColor)

        # Directional Light
        elif lightType == self.__lightType[1]:

            self.__directionalCount += 1

            if _lightId == None:

                lightId += (lightType + str(self.__directionalCount))

            else:

                lightId = _lightId

            lightNP = self.__create_directional_light(lightId, lightColor, lightHpr, shadow)

        # Point Light
        elif lightType == self.__lightType[2]:

            self.__pointCount += 1

            if _lightId == None:

                lightId += (lightType + str(self.__pointCount))

            else:

                lightId = _lightId

            lightNP = self.__create_point_light(lightId, lightColor, lightPos, shadow)

        # Spot Light
        elif lightType == self.__lightType[3]:

            self.__spotCount += 1

            if _lightId == None:

                lightId += (lightType + str(self.__spotCount))

            else:

                lightId = _lightId

            lightNP = self.__create_spot_light(lightId, lightColor, lightPos, targetId, shadow)

        else:

            return None

        #print self.__sceneMgr.get_res(parentId)

        lightNP.reparentTo(self.__sceneMgr.get_res(parentId))

        self.__lightMap[lightId] = lightNP
        self.__lightParentId[lightId] = parentId

        return lightNP

    #########################################

    # 创建Ambient Light节点
    def __create_ambient_light(self,
                               lightId,
                               lightColor):

        ambientLight = AmbientLight(lightId)
        ambientLight.setColor(lightColor)

        ambientLightNP = NodePath(ambientLight)

        return ambientLightNP

    #########################################

    # 创建Directional Light节点
    def __create_directional_light(self,
                                   lightId,
                                   lightColor,
                                   lightHpr,
                                   shadow = True):

        directionalLight = DirectionalLight(lightId)
        directionalLight.setColor(lightColor)
        directionalLight.setShadowCaster(shadow)

        directionalLightNP = NodePath(directionalLight)

        directionalLightNP.setHpr(lightHpr)

        return directionalLightNP

    #########################################

    # 创建Point Light节点
    def __create_point_light(self,
                             lightId,
                             lightColor,
                             lightPos,
                             shadow = True):

        pointLight = PointLight(lightId)
        pointLight.setColor(lightColor)
        pointLight.setShadowCaster(shadow)

        pointLightNP = NodePath(pointLight)

        pointLightNP.setPos(lightPos)

        return pointLightNP

    #########################################

    # 创建Spot Light节点
    def __create_spot_light(self,
                            lightId,
                            lightColor,
                            lightPos,
                            targetId,
                            shadow = True):

        spotLight = Spotlight(lightId)
        spotLight.setColor(lightColor)
        spotLight.setLens(PerspectiveLens())
        spotLight.setShadowCaster(shadow)

        spotLightNP = NodePath(spotLight)

        spotLightNP.setPos(lightPos)

        if isinstance(targetId, list) is True:
            spotLightNP.lookAt(self.__sceneMgr.get_res(targetId[0]))
        else:
            spotLightNP.lookAt(self.__sceneMgr.get_res(targetId))

        if self.__targetMap.has_key(lightId) is False:

            self.__targetMap[lightId] = []

        self.__targetMap[lightId].append(targetId)

        return spotLightNP

    #########################################

    # 设置光源直射物体
    def set_light_to(self, lightId, setorId):

        light = self.get_light(lightId)
        #print "in set_light_to : lightId ", lightId
        if setorId == "render":
            #print "in set_light_to : render ", self.__sceneMgr.get_render()
            #print "in set_light_to : light ", light
            self.__sceneMgr.get_render().setLight(light)

        else:

            self.__sceneMgr.get_res(setorId).setLight(light)

        if self.__setorMap.has_key(lightId) is False:

            self.__setorMap[lightId] = []

        self.__setorMap[lightId].append(setorId)

    def bind_SceneManager(self, sceneMgr):

        self.__sceneMgr = sceneMgr

    """""""""""
    光源查询函数
    """""""""""

    def get_sceneMgr(self):

        return self.__sceneMgr

    def get_lightMap(self):

        return self.__lightMap

    def get_targetMap(self):

        return self.__targetMap

    def get_setorMap(self):

        return self.__setorMap

    def get_light(self, lightId):
        #print "in get_light", len(self.__lightMap.keys())
        # for lightId in self.__lightMap.keys():
        #     print lightId

        if lightId not in self.__lightMap.keys():

            return None

        else:

            return self.__lightMap[lightId]

    def get_lightId(self, light):

        for k, v in self.__lightMap.iteritems():

            if v == light:

                return k

        return None

    def get_arcPkg(self):

        return self.__arcPkg

    """""""""""""""""""""""
    信息打印函数，主要用于调试
    """""""""""""""""""""""

    def print_lightInfo(self):
        print "----- The Light Info -----"
        for k, v in self.__lightMap.iteritems():
            print "%s : %s" % (k, v)
        print "--------------------"
