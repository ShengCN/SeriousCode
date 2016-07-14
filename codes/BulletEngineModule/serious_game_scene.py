# coding=utf-8
"""""""""""""""
SeriousGameScene 主要用来封装整个游戏的场景，统一接口。
编写人： codingblack
编写时间：2016.7.12
"""""""""""""""

import sys

from SceneModule.camera_controller import CameraController

sys.path.append('../')

from direct.showbase.DirectObject import DirectObject
from direct.showbase.InputStateGlobal import inputState
from direct.showbase.ShowBase import ShowBase, AntialiasAttrib, NodePath, LPoint3f
from direct.task.TaskManagerGlobal import taskMgr

from panda3d.core import AmbientLight
from panda3d.core import DirectionalLight
from panda3d.core import Vec3
from panda3d.core import Vec4
from panda3d.core import Point3
from panda3d.core import TransformState
from panda3d.core import BitMask32
from pandac.PandaModules import AntialiasAttrib, LODNode
from panda3d.bullet import *
from BulletEngineModule.bullet_engine_manager import BulletEngineMgr

class SeriousGameScene(DirectObject):
    def __init__(self, base,sceneMgr,roleMgr,resMgr):
        DirectObject.__init__(self)
        self.base = base
        self.initAll(sceneMgr,roleMgr,resMgr)


    def initAll(self,sceneMgr,roleMgr,resMgr):
        self.worldNP = self.base.render.attachNewNode('World')
        self.__init_shader()
        self.__init_light_camear()
        self.bullet_mgr = BulletEngineMgr(self.base,self.worldNP,sceneMgr,roleMgr,resMgr)
        self.sceneMgr = sceneMgr
        self.roleMgr = roleMgr
        self.resMgr = resMgr
        self.base.setBackgroundColor(0, 0, 0, 1)

    # shader 初始化
    def __init_shader(self):
        self.base.backfaceCullingOn()
        self.base.setFrameRateMeter(True)
        self.base.render.flattenStrong()
        self.base.render.setTwoSided(True)
        self.base.render.setAntialias(AntialiasAttrib.MAuto)
        self.worldNP.setTwoSided(True)

        # LOD 优化
        lod = LODNode("lod")
        lodnp = NodePath(lod)
        lodnp.reparentTo(self.base.render)

    # 灯光、镜头初始化
    def __init_light_camear(self):
        self.base.setFrameRateMeter(True)

        self.base.cam.setPos(0, 0, 100)
        self.base.cam.lookAt(0, 0, -90)

        # Light
        alight = AmbientLight('ambientLight')
        alight.setColor(Vec4(0.5, 0.5, 0.5, 1))
        alightNP = self.base.render.attachNewNode(alight)

        dlight = DirectionalLight('directionalLight')
        dlight.setDirection(Vec3(1, 1, -1))
        dlight.setColor(Vec4(0.7, 0.7, 0.7, 1))
        dlightNP = self.base.render.attachNewNode(dlight)

        self.base.render.clearLight()
        self.base.render.setLight(alightNP)
        self.base.render.setLight(dlightNP)

    def cam_control(self,isFixed,pos=Point3(0,0,0),hpr=Vec3(0,0,0),lookAt=Point3(0,0,0)):
        self.bullet_mgr.cam_control(isFixed,pos,hpr,lookAt)

    def load_game_scene(self,scene_path,scale,box,height=0):
        home = self.sceneMgr.add_model_scene(scene_path, self.base.render)
        home.setScale(scale)
        home.setZ(height)
        box_world = box
        self.bullet_mgr.add_bullet_world(box_world)

    def load_game_scene_ball_rigid(self,scene_path,scale,radius):
        home = self.sceneMgr.add_model_scene(scene_path, self.base.render)
        home.setScale(scale)
        return self.bullet_mgr.add_ball_bullet_world(radius)

    # 新增游戏主角
    def add_player_role(self,pos=Point3(-30,30,15),hpr=Vec3(0,0,0)):
        self.bullet_mgr.add_player_role(pos,hpr)

    def add_NPC_role(self,character_name,pos,scale,hpr=Vec3(0,0,0)):
        self.bullet_mgr.add_NPC_role(character_name,pos,scale,hpr)

    # 新增怪物
    def add_enemy_role(self,pos,scale,model_path,model_action_path):
        self.bullet_mgr.add_enemy_role(pos,scale,model_path,model_action_path)

    # 增加室内房屋碰撞体
    def add_rigid_box(self,pos,size,hpr,id):
        self.bullet_mgr.add_rigid_box(pos,size,hpr,id)

    def task_update(self):
        self.bullet_mgr.task_update()

    def stop_update(self):
        self.bullet_mgr.stop_update()

    def reset_update(self):
        self.bullet_mgr.reset_update()

    def destroy(self):
        # destory bullet
        self.bullet_mgr.stop_update()
        self.bullet_mgr.cleanup()
        # destory game scene, 要保留相机
        allChildren = self.base.render.getChildren()
        for childNode in allChildren:
            if childNode.getName() == "camera":
                cameraNP = childNode
        print "in destroy :::: ", self.base.render.find("**/hunter_Alarm1*")
        self.base.render.node().removeAllChildren()
        self.base.render.attachNewNode(cameraNP.node())


# 世界碰撞体
class BoxWorld(object):
    def __init__(self,west_pos,east_pos,north_pos,south_pos):
        object.__init__(self)
        self.west = west_pos
        self.east = east_pos
        self.north = north_pos
        self.south = south_pos

