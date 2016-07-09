# -*- coding:utf-8 -*-

from SceneModule.SceneResManager import SceneResManager
from SceneModule.camera_controller import CameraController
from SceneModule.light_controller import LightController
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

sceneMgr = SceneResManager()

modelPath = "/e/models/ralph.egg"
actorPath = "/e/models/ralph.egg"
actionPath = {
    "jump" : "/e/models/ralph-jump.egg",
    "walk" : "/e/models/ralph-walk.egg"
}
terrainHeightfield = "/e/models/sky.jpg"
terrainColorMap = "/e/models/grass.jpg"

#loadPrcFileData('', 'fullscreen true')
loadPrcFileData("", "window-title Reborn:The Soul Of Devil")

class Test(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        model = sceneMgr.load_res(modelPath)
        actor = sceneMgr.load_res(actorPath, actionPath)
        self.terrain = sceneMgr.load_res(terrainHeightfield, terrainColorMap)

        model.reparentTo(self.render)
        actor.reparentTo(self.render)
        self.terrain.getRoot().reparentTo(self.render)
        self.terrain.getRoot().setPos(-10, -10, 0)
        self.terrain.setFocalPoint(self.cam)

        model.setPos(5, 5, 0)
        actor.setPos(-5, 5, 0)

        self.disableMouse()
        self.cam.setPos(0, 20, 20)
        self.cam.lookAt(0, 0, 0)

        lightMgr = LightController()

        light1 = lightMgr.create_light(lightType = "AmbientLight",
                                       lightColor = Vec4(0.2, 0.1, 0.1, 1.0),
                                       parentNode = self.render)
        lightMgr.set_light_to(light1, self.render)

        #ambLight = AmbientLight("ambLight")
        #ambLight.setColor(Vec4(0.2, 0.1, 0.1, 1.0))
        #ambNode = self.render.attachNewNode(ambLight)
        #self.render.setLight(ambNode)

        light2 = lightMgr.create_light(lightType = "DirectionalLight",
                                       lightColor = Vec4(0.1, 0.4, 0.1, 1.0),
                                       lightHpr = Vec3(60, 0, 90),
                                       parentNode = self.render)
        lightMgr.set_light_to(light2, self.render)

        #dirLight = DirectionalLight("dirLight")
        #dirLight.setColor(Vec4(0.1, 0.4, 0.1, 1.0))
        #dirNode = self.render.attachNewNode(dirLight)
        #dirNode.setHpr(60, 0, 90)
        #self.render.setLight(dirNode)

        light3 = lightMgr.create_light(lightType = "PointLight",
                                       lightColor = Vec4(0.8, 0.8, 0.8, 1.0),
                                       lightPos = Vec3(0, 0, 15),
                                       parentNode = self.render)
        lightMgr.set_light_to(light3, model)

        #pntLight = PointLight("point")
        #pntLight.setColor(Vec4(0.8, 0.8, 0.8, 1.0))
        #pntNode = self.render.attachNewNode(pntLight)
        #pntNode.setPos(0, 0, 15)
        #model.setLight(pntNode)

        light4 = lightMgr.create_light(lightType = "SpotLight",
                                       lightColor = Vec4(1.0, 1.0, 1.0, 1.0),
                                       lightPos = Vec3(0, 10, 10),
                                       parentNode = self.render,
                                       target = model)
        lightMgr.set_light_to(light4, self.render)

        lightMgr.print_lightInfo()

        #sptLight = Spotlight("sptLight")
        #sptLens = PerspectiveLens()
        #sptLight.setLens(sptLens)
        #sptLight.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        #sptLight.setShadowCaster(True)
        #sptNode = self.render.attachNewNode(sptLight)
        #sptNode.setPos(0, 10, 10)
        #sptNode.lookAt(model)
        #self.render.setLight(sptNode)

        self.render.setShaderAuto()

        camCtrlr = CameraController(self.cam, globalClock)

        self.accept("y", camCtrlr.accept_event, ["move_forward", True])
        self.accept("y-up", camCtrlr.accept_event, ["move_forward", False])
        self.accept("h", camCtrlr.accept_event, ["move_backward", True])
        self.accept("h-up", camCtrlr.accept_event, ["move_backward", False])
        self.accept("g", camCtrlr.accept_event, ["move_left", True])
        self.accept("g-up", camCtrlr.accept_event, ["move_left", False])
        self.accept("j", camCtrlr.accept_event, ["move_right", True])
        self.accept("j-up", camCtrlr.accept_event, ["move_right", False])
        self.accept("t", camCtrlr.accept_event, ["move_up", True])
        self.accept("t-up", camCtrlr.accept_event, ["move_up", False])
        self.accept("u", camCtrlr.accept_event, ["move_down", True])
        self.accept("u-up", camCtrlr.accept_event, ["move_down", False])

        self.accept("q", camCtrlr.accept_event, ["rotate_h_cw", True])
        self.accept("q-up", camCtrlr.accept_event, ["rotate_h_cw", False])
        self.accept("w", camCtrlr.accept_event, ["rotate_h_ccw", True])
        self.accept("w-up", camCtrlr.accept_event, ["rotate_h_ccw", False])
        self.accept("a", camCtrlr.accept_event, ["rotate_p_cw", True])
        self.accept("a-up", camCtrlr.accept_event, ["rotate_p_cw", False])
        self.accept("s", camCtrlr.accept_event, ["rotate_p_ccw", True])
        self.accept("s-up", camCtrlr.accept_event, ["rotate_p_ccw", False])
        self.accept("z", camCtrlr.accept_event, ["rotate_r_cw", True])
        self.accept("z-up", camCtrlr.accept_event, ["rotate_r_cw", False])
        self.accept("x", camCtrlr.accept_event, ["rotate_r_ccw", True])
        self.accept("x-up", camCtrlr.accept_event, ["rotate_r_ccw", False])

        self.taskMgr.add(camCtrlr.camera_control, "camera_control")

        sceneMgr.print_resMap()

        self.taskMgr.add(self.update_terrain, "update_terrain")



    def update_terrain(self, task):

        self.terrain.update()
        return task.cont

test = Test()
test.run()