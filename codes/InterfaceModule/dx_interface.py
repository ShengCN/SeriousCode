<<<<<<< HEAD
# -*- coding:utf-8 -*-

from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData
from pandac.PandaModules import AntialiasAttrib

from SceneModule.scene_manager import SceneManager
from SceneModule.light_controller import LightController
from SceneModule.camera_controller import CameraController
from RoleModule.role_manager import RoleManager
from ResourcesModule.archives import Archives

extraConfiguration = """
framebuffer-multisample 1
multisamples 2
fullscreen #f
interpolate-frames 1
window-title Reborn : The Soul Of Devil
preload-textures 0
preload-simple-textures 1
texture-compression 1
allow-incomplete-render 1
allow-async-bind 1
restore-initial-pose 0
"""

loadPrcFileData("", extraConfiguration)

class DXInterface(object):

    def __init__(self):

        object.__init__(self)

        self.__showbase = ShowBase()

        self.__showbase.disableMouse()

        self.__showbase.render.setAntialias(AntialiasAttrib.MAuto)
        self.__showbase.render.setShaderAuto()
        self.__showbase.render.setTwoSided(True)

        self.__archive = Archives()
        self.__archive.read_from_file()
        arcList = self.__archive.select_archive(2)

        self.__sceneMgr = SceneManager()
        self.__sceneMgr.build_on(self.__showbase)
        self.__sceneMgr.import_sceneArcPkg(arcList[0])
        self.__sceneMgr.get_ActorMgr().set_clock(globalClock)
        self.__sceneMgr.get_CamCtrlr().set_clock(globalClock)

        print arcList[0][2].get_itemsData()
        print "in interface : ", self.__sceneMgr.get_camCtrlr().get_camToCtrl().getPos()

        self.__roleMgr = RoleManager()
        self.__roleMgr.bind_SceneManager(self.__sceneMgr)
        self.__roleMgr.import_arcPkg(arcList[1])

        self.__sceneMgr.get_ActorMgr().bind_RoleManager(self.__roleMgr)

        # for role in self.__roleMgr.get_roleMap().values():
        #     role.print_all_attr()
        #self.__roleMgr.print_roleModelMap()

        self.__showbase.taskMgr.setupTaskChain("actorTaskChain", numThreads=3)
        self.__showbase.taskMgr.setupTaskChain("terraTaskChain")
        self.__showbase.taskMgr.setupTaskChain("cameraTaskChain", numThreads=3)

        self.__showbase.taskMgr.add(self.__sceneMgr.update_scene, "update_scene")

    def get_showbase(self):

        return self.__showbase

    def get_game_window(self):

        return self.__showbase.win

    def add_scenery(self):

        pass

    def add_figure(self):

        pass

    def get_figure(self):

        pass

    def get_figure_node(self):

        pass

    def set_figure_move(self):

        pass

    def set_figure_attack(self):

        pass

=======
# -*- coding:utf-8 -*-

from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData
from pandac.PandaModules import AntialiasAttrib

from SceneModule.scene_manager import SceneManager
from SceneModule.light_controller import LightController
from SceneModule.camera_controller import CameraController
from RoleModule.role_manager import RoleManager
from ResourcesModule.archives import Archives

extraConfiguration = """
framebuffer-multisample 1
multisamples 2
fullscreen #f
interpolate-frames 1
window-title Reborn : The Soul Of Devil
preload-textures 0
preload-simple-textures 1
texture-compression 1
allow-incomplete-render 1
allow-async-bind 1
restore-initial-pose 0
"""

loadPrcFileData("", extraConfiguration)

class DXInterface(object):

    def __init__(self):

        object.__init__(self)

        self.__showbase = ShowBase()

        self.__showbase.disableMouse()

        self.__showbase.render.setAntialias(AntialiasAttrib.MAuto)
        self.__showbase.render.setShaderAuto()
        self.__showbase.render.setTwoSided(True)

        self.__archive = Archives()
        self.__archive.read_from_file()
        arcList = self.__archive.select_archive(2)

        self.__sceneMgr = SceneManager()
        self.__sceneMgr.build_on(self.__showbase)
        self.__sceneMgr.import_sceneArcPkg(arcList[0])
        self.__sceneMgr.get_ActorMgr().set_clock(globalClock)
        self.__sceneMgr.get_CamCtrlr().set_clock(globalClock)

        print arcList[0][2].get_itemsData()
        print "in interface : ", self.__sceneMgr.get_camCtrlr().get_camToCtrl().getPos()

        self.__roleMgr = RoleManager()
        self.__roleMgr.bind_SceneManager(self.__sceneMgr)
        self.__roleMgr.import_arcPkg(arcList[1])

        self.__sceneMgr.get_ActorMgr().bind_RoleManager(self.__roleMgr)

        # for role in self.__roleMgr.get_roleMap().values():
        #     role.print_all_attr()
        #self.__roleMgr.print_roleModelMap()

        self.__showbase.taskMgr.setupTaskChain("actorTaskChain", numThreads=3)
        self.__showbase.taskMgr.setupTaskChain("terraTaskChain")
        self.__showbase.taskMgr.setupTaskChain("cameraTaskChain", numThreads=3)

        self.__showbase.taskMgr.add(self.__sceneMgr.update_scene, "update_scene")

    def get_showbase(self):

        return self.__showbase

    def get_game_window(self):

        return self.__showbase.win

    def add_scenery(self):

        pass

    def add_figure(self):

        pass

    def get_figure(self):

        pass

    def get_figure_node(self):

        pass

    def set_figure_move(self):

        pass

    def set_figure_attack(self):

        pass

>>>>>>> 36f45132a7c451a2ded3cac5e2d58db92af207c3
