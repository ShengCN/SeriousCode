# -*- coding:utf-8 -*-

from actor_manager import ActorManager
from model_manager import ModelManager
from terrain_manager import TerrainManager
from camera_controller import CameraController
from light_controller import LightController
import SeriousTools.SeriousTools as SeriousTools

class SceneManager(object):

    def __init__(self):

        self.__actorMgr = ActorManager()
        self.__modelMgr = ModelManager()
        self.__terraMgr = TerrainManager()

        self.__render = None
        self.__showbase = None

        self.__camCtrlr = None
        self.__lightCtrlr = None

    """""""""""""""""""""""""""""""""""""""
    场景管理函数，包括创建、更新、剔除、隐藏等
    """""""""""""""""""""""""""""""""""""""

    def build_on(self, showbase):

        self.__showbase = showbase

        self.__render = self.__showbase.render

    # 添加动态模型场景
    def add_actor_scene(self,
                        resPath,
                        extraResPath,
                        parentNode):

        actor = self.__actorMgr.load_res(resPath, extraResPath)

        actor.reparentTo(parentNode)

        return actor

    #####################

    # 添加静态模型场景
    def add_model_scene(self,
                        resPath,
                        parentNode):

        model = self.__modelMgr.load_res(resPath)

        model.reparentTo(parentNode)

        return model

    #####################

    # 添加地形场景
    def add_terrain_scene(self,
                          resPath,
                          extraResPath,
                          parentNode):

        terrain = self.__terraMgr.load_res(resPath, extraResPath)

        terrain.getRoot().reparentTo(parentNode)

        return terrain

    #####################

    # 更新场景
    def update_scene(self, task):

        # 更新地形
        #self.__terraMgr.update_terrain(task)

        self.__actorMgr.update_actors(task)

        self.__camCtrlr.update_camera(task)

        return task.cont

    #####################

    # 总的资源ID查询
    def get_resId(self, res):

        resId = None

        resId =  self.__actorMgr.get_resId(res)

        if resId is None:

            resId = self.__modelMgr.get_resId(res)

            if resId is None:

                resId = self.__terraMgr.get_resId(res)

        return resId

    #####################

    # 总的资源查询
    def get_res(self, resId):

        if resId == "render":

            return self.__render

        res = self.__actorMgr.get_res(resId)

        if res is None:

            res = self.__modelMgr.get_res(resId)

            if res is None:

                res = self.__terraMgr.get_res(resId)

        return res

    def bind_CameraController(self, camCtrlr):

        self.__camCtrlr = camCtrlr

        self.__actorMgr.bind_CameraController(camCtrlr)

    def get_camCtrlr(self):

        return self.__camCtrlr

    def bind_LightController(self, lightCtrlr):

        self.__lightCtrlr = lightCtrlr

        self.__lightCtrlr.bind_SceneManager(self)

    def get_lightCtrlr(self):

        return self.__lightCtrlr

    """""""""""""""""""""
    读档存档的场景数据接口
    """""""""""""""""""""

    # Pos   : LPoint3f
    # Hpr   : LVecBase3f
    # Scale : LVecBase3f
    # Color : LVecBase4f
    # LVecBase4f, LVecBase3f((0, 0, 0))和LPoint3f((0, 0, 0))这样的初始化是可以的

    # 导入场景数据，用于读档
    def import_sceneArcPkg(self, sceneArcPkg):

        actorArcPkg = None

        for arcPkg in sceneArcPkg:

            if arcPkg.get_ArchivePackageName() == "actor":

                actorArcPkg = arcPkg

        actorMgr = ActorManager()

        self.__actorMgr = actorMgr

        #actorArcPkg.print_metaData()

        for actorItem in actorArcPkg.get_itemsData():

            actor = actorMgr.load_res(_resId = actorItem[0],
                                      resPath = actorItem[1],
                                      extraResPath = actorItem[2])

            #print "the sceneMgr get_res : ", self.get_res(actorItem[0])

            actor.setPos(actorItem[3])
            actor.setHpr(actorItem[4])
            actor.setScale(actorItem[5])

            parentNode = self.get_res(actorItem[6])
            actor.reparentTo(parentNode)

        eventActionRecord = actorArcPkg.get_metaData("eventActionRecord")
        eventEffertRecord = actorArcPkg.get_metaData("eventEffertRecord")

        #print "in import : eventActionRecord ", len(eventActionRecord)

        for actorId, record in eventActionRecord.iteritems():

            for toggleEvent, actionName in record.iteritems():

                actorMgr.add_toggle_to_actor(toggleEvent, actorId, actionName)

        for actorId, record in eventEffertRecord.iteritems():

            for toggleEvent, effertList in record.iteritems():

                for effert in effertList:

                    print "import eventEffertRecord : ", toggleEvent, ", ", actorId, ", ", effert

                    actorMgr.add_effert_to_actor(toggleEvent, actorId, effert[0])
        #actorMgr.set_clock(globalClock)

        actorMgr.print_eventActionRecord()
        actorMgr.print_eventEffertRecord()

        #self.__actorMgr = actorMgr

        # Model数据读档
        modelArcPkg = None

        for arcPkg in sceneArcPkg:

            if arcPkg.get_ArchivePackageName() == "model":

                modelArcPkg = arcPkg

        modelMgr = ModelManager()
        self.__modelMgr = modelMgr

        for modelItem in modelArcPkg.get_itemsData():

            model = modelMgr.load_res(_resId = modelItem[0],
                                      resPath = modelItem[1])

            model.setPos(modelItem[2])
            model.setHpr(modelItem[3])
            model.setScale(modelItem[4])

            parentNode = self.get_res(resId = modelItem[5])
            model.reparentTo(parentNode)

        # Terrain数据读档
        terraArcPkg = None
        terraMgr = TerrainManager()

        for arcPkg in sceneArcPkg:

            if arcPkg.get_ArchivePackageName() == "terrain":

                terraArcPkg = arcPkg

        for terraItem in terraArcPkg.get_itemsData():

            terrain = terraMgr.load_res(_resId = terraItem[0],
                                        resPath = terraItem[1],
                                        extraResPath = terraItem[2])

            terrain.getRoot().setPos(terraItem[3])
            terrain.getRoot().setHpr(terraItem[4])
            terrain.getRoot().setScale(terraItem[5])

            parentNode = self.get_res(resId = terraItem[6])
            terrain.getRoot().reparentTo(parentNode)

        terraMgr.set_currTerrain(terraArcPkg.get_metaData("currTerraId"))

        self.__terraMgr = terraMgr

        # Camera数据读档
        cameraArcPkg = None

        for arcPkg in sceneArcPkg:

            if arcPkg.get_ArchivePackageName() == "camera":
                cameraArcPkg = arcPkg

        camCtrlr = CameraController()
        self.__camCtrlr = camCtrlr
        camCtrlr.bind_camera(self.__showbase.cam)
        camCtrlr.bind_ToggleHost(self.__showbase)

        cameraArcPkg = cameraArcPkg.get_itemsData()[0]
        #print "in import : ", cameraArcPkg[0]
        camCtrlr.get_camToCtrl().setPos(cameraArcPkg[0])
        camCtrlr.get_camToCtrl().setHpr(cameraArcPkg[1])
        camCtrlr.set_moveSpeed(cameraArcPkg[2])
        camCtrlr.set_rotateSpeed(cameraArcPkg[3])

        objToFocus = self.get_res(cameraArcPkg[4])
        camCtrlr.focus_on(objToFocus, cameraArcPkg[5])

        camCtrlr.set_optsSwitch(cameraArcPkg[6])
        #camCtrlr.set_toggleEventToOpts(cameraArcPkg[7])

        self.__actorMgr.bind_CameraController(camCtrlr)

        for toggleEvent, opt in cameraArcPkg[7].iteritems():

            camCtrlr.add_toggle_to_opt(toggleEvent, opt)

        # print "Camera Pos : ", camCtrlr.get_camToCtrl().getPos()
        # print "Camera Hpr : ", camCtrlr.get_camToCtrl().getHpr()

        # Light数据读档
        lightArcPkg = None

        for arcPkg in sceneArcPkg:

            if arcPkg.get_ArchivePackageName() == "light":

                lightArcPkg = arcPkg

        lightCtrlr = LightController()
        self.__lightCtrlr = lightCtrlr
        lightCtrlr.bind_SceneManager(self)

        for lightItem in lightArcPkg.get_itemsData():

            light = lightCtrlr.create_light(_lightId = lightItem[0],
                                            lightType = SeriousTools.extract_name_from_Id(lightItem[0]),
                                            lightColor = lightItem[1],
                                            lightPos = lightItem[2],
                                            lightHpr = lightItem[3],
                                            targetId = lightItem[4],
                                            parentId = lightItem[6])
            #print "in import : ", light
            for setorId in lightItem[5]:

               lightCtrlr.set_light_to(lightItem[0], setorId)

    #####################

    # 导出场景数据，用于存档
    # 考虑到获取父节点ID的全局性，故将其他几种资源的存档数据放到这里进行保存
    def export_sceneArcPkg(self):

        # Actor数据存档
        actorArcPkg = self.__actorMgr.get_arcPkg()

        actorResPath = self.__actorMgr.get_resPath()

        #actorArcPkg.set_metaData("toggleEffert", self.__actorMgr.get_toggleEffert())
        actorArcPkg.set_metaData("eventActionRecord", self.__actorMgr.get_eventActionRecord())
        actorArcPkg.set_metaData("eventEffertRecord", self.__actorMgr.get_eventEffertRecord())

        for actorId, actor in self.__actorMgr.get_resMap().iteritems():

            actorItem = []

            actorItem.append(actorId)
            actorItem.append(actorResPath[actorId][0])
            actorItem.append(actorResPath[actorId][1])
            actorItem.append(actor.getPos())
            actorItem.append(actor.getHpr())
            actorItem.append(actor.getScale())

            parentNode = actor.getParent()

            if parentNode.getName() is "render":

                actorItem.append("render")

            else:

                parentId = self.get_resId(parentNode)

                if parentId is None:

                    actorItem.append("render")

                else:

                    actorItem.append(parentId)

            actorArcPkg.add_item(actorItem)

        ##########

        # Model数据存档
        modelArcPkg = self.__modelMgr.get_arcPkg()

        modelResPath = self.__modelMgr.get_resPath()

        for modelId, model in self.__modelMgr.get_resMap().iteritems():

            modelItem = []

            modelItem.append(modelId)
            modelItem.append(modelResPath[modelId])
            modelItem.append(model.getPos())
            modelItem.append(model.getHpr())
            modelItem.append(model.getScale())

            parentNode = model.getParent()

            if parentNode.getName() is "render":

                modelItem.append("render")

            else:

                parentId = self.get_resId(parentNode)

                if parentId is None:

                    modelItem.append("render")

                else:

                    modelItem.append(parentId)

            modelArcPkg.add_item(modelItem)

        ##########

        # Terrain数据存档
        terraArcPkg = self.__terraMgr.get_arcPkg()

        terraArcPkg.set_metaData("currTerraId", self.__terraMgr.get_currTerrain())

        terraResPath = self.__terraMgr.get_resPath()

        for terrainId, terrain in self.__terraMgr.get_resMap().iteritems():

            terrainItem = []

            terrainItem.append(terrainId)
            terrainItem.append(terraResPath[terrainId][0])
            terrainItem.append(terraResPath[terrainId][1])
            terrainItem.append(terrain.getRoot().getPos())
            terrainItem.append(terrain.getRoot().getHpr())
            terrainItem.append(terrain.getRoot().getScale())

            parentNode = terrain.getRoot().getParent()

            if parentNode.getName() is "render":

                terrainItem.append("render")

            else:

                parentId = self.get_resId(parentNode)

                if parentId is None:

                    terrainItem.append("render")

                else:

                    terrainItem.append(parentId)

            terraArcPkg.add_item(terrainItem)

        ##########

        # Camera数据存档
        camArcPkg = self.__camCtrlr.get_arcPkg()

        cam = self.__camCtrlr.get_camToCtrl()

        camItem = []

        camItem.append(cam.getPos())
        camItem.append(cam.getHpr())
        camItem.append(self.__camCtrlr.get_moveSpeed())
        camItem.append(self.__camCtrlr.get_rotateSpeed())

        focusObjId = self.get_resId(self.__camCtrlr.get_focusObj())
        camItem.append(focusObjId)

        camItem.append(self.__camCtrlr.get_rotateRadius())
        camItem.append(self.__camCtrlr.get_optsSwitch())
        camItem.append(self.__camCtrlr.get_toggleEventToOpts())
        #camItem.append(None)

        camArcPkg.add_item(camItem)

        ##########

        # Light数据存档
        lightArcPkg = self.__lightCtrlr.get_arcPkg()

        lightTargetMap = self.__lightCtrlr.get_targetMap()

        lightSetorMap = self.__lightCtrlr.get_setorMap()

        for lightId, light in self.__lightCtrlr.get_lightMap().iteritems():

            lightItem = []

            lightItem.append(lightId)
            lightItem.append(light.node().getColor())
            lightItem.append(light.getPos())
            lightItem.append(light.getHpr())

            if lightTargetMap.has_key(lightId) is True:

                lightItem.append(lightTargetMap[lightId])

            else:

                lightItem.append(None)

            lightItem.append(lightSetorMap[lightId])

            parentNode = light.getParent()

            if parentNode.getName() is "render":

                lightItem.append("render")

            else:

                parentId = self.get_resId(parentNode)

                if parentId is None:

                    lightItem.append("render")

                else:

                    lightItem.append(parentId)

            lightArcPkg.add_item(lightItem)

        ##########

        sceneArcPkg = [
            actorArcPkg,
            modelArcPkg,
            terraArcPkg,
            camArcPkg,
            lightArcPkg
        ]

        print "in export : ", len(lightArcPkg.get_itemsData())

        return sceneArcPkg


    """""""""""""""
    成员变量的get函数
    """""""""""""""

    def set_render(self, render):

        self.__render = render

    def get_render(self):

        return self.__render

    def get_ActorMgr(self):

        return self.__actorMgr

    def get_ModelMgr(self):

        return self.__modelMgr

    def get_TerraMgr(self):

        return self.__terraMgr

    def get_CamCtrlr(self):

        return self.__camCtrlr

    def get_LightCtrlr(self):

        return self.__lightCtrlr



