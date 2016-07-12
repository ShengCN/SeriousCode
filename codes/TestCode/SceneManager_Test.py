
from SceneModule.scene_manager import SceneManager
from SceneModule.camera_controller import CameraController
from SceneModule.light_controller import LightController
from RoleModule.role_manager import RoleManager
from ResourcesModule.load_plot import LoadPlot
from ResourcesModule.archives import Archives

from pandac.PandaModules import AntialiasAttrib
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.showbase.MessengerGlobal import messenger

import sys

config = """
framebuffer-multisample 1
multisamples 2
framebuffer-stencil #t
threading-model Cull/Draw
fullscreen #f
interpolate-frames 1
window-title Reborn : The Soul Of Devil
# preload-textures 0
# preload-simple-textures 1
texture-compression 1
allow-incomplete-render 1
allow-async-bind 1
restore-initial-pose 0
hardware-animated-vertices #t
model-cache-textures #t
support-threads #t
display-list-animation 1
display-lists 1
gl-finish #f
loader-num-threads 4
show-occlusion #t
"""

loadPrcFileData("", config)

modelRootPath = "/e/Serious2/Material/ModelEGGS/"

village = modelRootPath + "Outer/Outer.egg"

hunterPath = modelRootPath + "Hunter/hunter_Alarm1.egg"
hunterActionsPath = {
    "run_forward" : modelRootPath + "Hunter/hunter_RunWithGun1.egg",
    "run_backward" : modelRootPath + "Hunter/hunter_RunBackWithGun1.egg",
    "rda" : modelRootPath + "Hunter/hunter_WithGunRightDefence.egg",
    "lda" : modelRootPath + "Hunter/hunter_WithGunLeftDefenceUpdate",
    "bda" : modelRootPath + "Hunter/hunter_WithGunBackDefenceUpdate.egg",
    "attack" : modelRootPath + "Hunter/hunter_Attack1.egg",
    "stand" : modelRootPath + "Hunter/hunter_Alarm1Pose.egg"
}

wifeZombiePath = modelRootPath + "WifeZombie/WifeZombie_Stand.egg"
wifeZombieActionsPath = {
    "run" : modelRootPath + "WifeZombie/WifeZombie_Walk.egg",
    "attack" : modelRootPath + "WifeZombie/WifeZombie_Attack3.egg"
}

# house1Path = modelRootPath + "/Material/ModelEGGS/Village/house1.egg"

hookZombiePath = modelRootPath + "HookZombie/HookZombie_Pose.egg"
hookZombieActionsPath = {
    "walk" : modelRootPath + "HookZombie/HookZombie_Walk_v2.egg",
    "attack" : modelRootPath + "HookZombie/HookZombie_OffencePose.egg"
}

normalZombiePath = modelRootPath + "Zombie/Zombie_Pose.egg"
normalZombieActionsPath = {
    "walk"   : modelRootPath + "Zombie/Zombie_Walk.egg",
    "attack" : modelRootPath + "Zombie/Zombie_Offence.egg"
}

girlPath = modelRootPath + "Girl/GIRL_Pose.egg"


nunv = modelRootPath + "NUNV/NUNV_Pose.egg"

stealer = modelRootPath + "Stealer2/StealerWithPose.egg"

roomPath = modelRootPath + "Room/Room.egg"

coinPath = modelRootPath + "Coin/Coin.egg"

chestPath = modelRootPath + "Chest/Chest1.egg"
chestActionsPath = {
    "open" : modelRootPath + "Chest/Chest1_Open.egg"
}

EMPTY_NODEPATH = NodePath("EmptyNodePath")

class GameWorld_Test(ShowBase):

    def __init__(self):

        #PStatClient.connect()

        ShowBase.__init__(self)
        #self.oobeCull()
        self.backfaceCullingOn()
        self.setFrameRateMeter(True)
        #self.setSceneGraphAnalyzerMeter(True)
        self.render.flattenStrong()
        self.render.setAttrib(LightRampAttrib.makeDefault())
        self.render.setTwoSided(True)
        self.render.setAntialias(AntialiasAttrib.MAuto)


        #self.cam.node().getLens().setNear(5)
        #self.openWindow(pipe = self.makeModulePipe("p3tinydisplay"))

        self.disableMouse()
        sceneMgr = SceneManager()
        sceneMgr.build_on(self)

        model6 = self.loader.loadModel(village)
        model6.setPos(0, 0, 0)
        model6.setScale(5)
        model6.setTwoSided(True)
        model6.reparentTo(self.render)
        model6.clearLight()

        actor = sceneMgr.add_actor_scene(hunterPath,
                                         hunterActionsPath,
                                         self.render)
        actor.setPos(150, 150, 0)
        actor.setScale(1.6)
        #actor.setAntialias(AntialiasAttrib.MAuto)
        actor.setTwoSided(True)
        # self.render.removeNode(actor.node())
        #base.setBackgroundColor(color)
        #model6.reparentTo(lodnp)
        # house1 = sceneMgr.add_model_scene(house1Path, self.render)
        # house1.setPos(200, 0, 0)

        self.accept("escape", sys.exit)

        sceneMgr.get_ActorMgr().set_clock(globalClock)
        actorId = sceneMgr.get_ActorMgr().get_resId(actor)
        sceneMgr.get_ActorMgr().add_toggle_to_actor("w", actorId, "run_forward")
        sceneMgr.get_ActorMgr().add_toggle_to_actor("s", actorId, "run_backward")
        sceneMgr.get_ActorMgr().add_toggle_to_actor("player_be_attacked1", actorId, "rda")
        sceneMgr.get_ActorMgr().add_toggle_to_actor("player_be_attacked2", actorId, "lda")
        #sceneMgr.get_ActorMgr().add_toggle_to_actor("c", actorId, "bda")
        print "actorId : ", actorId

        sceneMgr.get_ActorMgr().add_effert_to_actor("w", actorId, "actor_move_forward")
        sceneMgr.get_ActorMgr().add_effert_to_actor("s", actorId, "actor_move_backward")
        sceneMgr.get_ActorMgr().add_effert_to_actor("a", actorId, "actor_rotate_cw")
        sceneMgr.get_ActorMgr().add_effert_to_actor("d", actorId, "actor_rotate_ccw")
        sceneMgr.get_ActorMgr().toggle_actor_attack("mouse1", actorId)
        sceneMgr.get_ActorMgr().add_toggle_for_player_to_interact("e", actorId)

        # _zombieWife = sceneMgr.add_actor_scene(wifeZombiePath,
        #                                        wifeZombieActionsPath,
        #                                        self.render)
        # _zombieWife.setPos(120, 120, 0)
        # zId = sceneMgr.get_resId(_zombieWife)
        #sceneMgr.get_ActorMgr().enemy_die_interval_play(zId)
        # sceneMgr.get_ActorMgr().add_toggle_to_actor("enemy_run", zId, "run")
        # sceneMgr.get_ActorMgr().add_toggle_to_actor("enemy_attack", zId, "attack")
        # #sceneMgr.get_ActorMgr().add_effert_to_actor("b", zId, "actor_move_forward")
        # self.cam.setPos(-200, 200, 100)

        # room = sceneMgr.add_model_scene(roomPath, self.render)
        # room.setPos(30, 50, 0)
        # room.setScale(5)

        hookzombie = sceneMgr.add_actor_scene(hookZombiePath, hookZombieActionsPath, self.render)
        hookzombie.setScale(3)
        hookzombie.setPos(40, 50, 0)
        hzId = sceneMgr.get_resId(hookzombie)
        #sceneMgr.get_ActorMgr().enemy_die_interval_play(hzId)
        sceneMgr.get_ActorMgr().add_toggle_to_actor("enemy_walk", hzId, "walk")
        sceneMgr.get_ActorMgr().add_toggle_to_actor("enemy_attack", hzId, "attack")
        #
        # _girl = sceneMgr.add_model_scene(girl, self.render)
        # _girl.setPos(50, 50, 0)

        # _nunv = sceneMgr.add_model_scene(nunv, self.render)
        # _nunv.setPos(60, 50, 0)

        _stealer = sceneMgr.add_actor_scene(stealer, {},  self.render)
        _stealer.setPos(70, 50, 0)
        _stealer.setH(60)

        chest = sceneMgr.add_actor_scene(chestPath, chestActionsPath, self.render)
        chest.setPos(-100, -100, 0)
        sceneMgr.get_ActorMgr().add_toggle_to_actor("open_chest", sceneMgr.get_resId(chest), "open")

        normalZombie = sceneMgr.add_actor_scene(normalZombiePath, normalZombieActionsPath, self.render)
        normalZombie.setPos(-30, -30, 0)
        normalZombie.setScale(3)

        camCtrlr = CameraController()
        camCtrlr.bind_camera(self.cam)
        camCtrlr.bind_ShowBase(self)
        camCtrlr.bind_ToggleHost(self)
        camCtrlr.set_clock(globalClock)
        camCtrlr.focus_on(actor, 200)
        camCtrlr.set_rotateSpeed(10)

        sceneMgr.bind_CameraController(camCtrlr)
        sceneMgr.get_ActorMgr().bind_CameraController(camCtrlr)

        self.accept("space", sys.exit)

        print self.render.getName()

        lightCtrlr = LightController()
        lightCtrlr.bind_SceneManager(sceneMgr)

        light1 = lightCtrlr.create_light(lightType = "AmbientLight",
                                         lightColor = (0.2, 0.1, 0.2, 1),
                                         parentId = self.render.getName()
                                         )
        lightId1 = lightCtrlr.get_lightId(light1)
        lightCtrlr.set_light_to(lightId1, self.render.getName())

        light2 = lightCtrlr.create_light(lightType = "DirectionalLight",
                                         lightColor = (1.0, 1.0, 1.0, 1.0),
                                         lightHpr = (0, 0, 0),
                                         parentId = "render")
        lightId2 = lightCtrlr.get_lightId(light2)
        lightCtrlr.set_light_to(lightId2, "render")

        light3 = lightCtrlr.create_light(lightType = "PointLight",
                                         lightColor = (0.8, 0.9, 0.7, 1.0),
                                         lightPos = (5, 5, 50),
                                         parentId = "render")
        lightId3 = lightCtrlr.get_lightId(light3)
        lightCtrlr.set_light_to(lightId3, "render")

        light4 = lightCtrlr.create_light(lightType = "SpotLight",
                                           lightColor = (1.0, 1.0, 1.0, 1.0),
                                           lightPos = (10, 10, 10),
                                           targetId = actorId,
                                           parentId = "render")
        lightId4 = lightCtrlr.get_lightId(light4)
        lightCtrlr.set_light_to(lightId4, "render")

        #self.render.setShaderAuto()

        sceneMgr.bind_LightController(lightCtrlr)

        print sceneMgr.get_ActorMgr().get_eventActionRecord()
        print sceneMgr.get_ActorMgr().get_eventEffertRecord()
        sceneMgr.get_ActorMgr().print_all_itvl_duration()

        self.cam.setPos(200, 200, 5)
        self.cam.lookAt(0, 0, 0)

        #actor.setRenderMode(RenderModeAttrib.MWireframe, 1)

        camCtrlr.add_toggle_to_opt("u", "rotate_around_up")
        camCtrlr.add_toggle_to_opt("j", "rotate_around_down")
        camCtrlr.add_toggle_to_opt("h", "rotate_around_cw")
        camCtrlr.add_toggle_to_opt("k", "rotate_around_ccw")

        #print camCtrlr.get_directionsVector()
        # arcPkgs = sceneMgr.export_sceneArcPkg()

        roleMgr = RoleManager()
        sceneMgr.bind_RoleManager(roleMgr)
        player = roleMgr.create_role(roleType = "PlayerRole",
                                     modelId = actorId)
        #player.set_attr_value("story", )
        # player.print_all_attr()
        #roleMgr.bind_SceneManager(sceneMgr)
        hookZombieRole = roleMgr.create_role(roleType = "EnemyRole",
                                             modelId = sceneMgr.get_resId(hookzombie))
        normalZombieRole = roleMgr.create_role(roleType = "EnemyRole",
                                               modelId = sceneMgr.get_resId(normalZombie))
        sceneMgr.get_ActorMgr().add_toggle_to_actor("enemy_walk", sceneMgr.get_resId(normalZombie), "walk")
        sceneMgr.get_ActorMgr().add_toggle_to_actor("enemy_attack", sceneMgr.get_resId(normalZombie), "attack")
        npc1 = roleMgr.create_role(roleType = "NPCRole",
                                   modelId = sceneMgr.get_resId(_stealer))
        print roleMgr.get_role_face_hpr(roleMgr.get_roleId(npc1))
        # npc1.print_all_attr()

        chest1 = roleMgr.create_role(roleType = "AttachmentRole",
                                     modelId = sceneMgr.get_resId(chest))

        # print self.render.getChildren()
        #
        # self.render.node().removeAllChildren()
        # actor.reparentTo(self.render)
        # self.cam.reparentTo(self.render)

        self.taskMgr.add(sceneMgr.update_scene, "update_scene")

        self.accept("l", self.__save_archive, [sceneMgr, roleMgr])

        self.accept("t", sceneMgr.get_ActorMgr().stop_all_itvls)
        self.accept("y", sceneMgr.get_ActorMgr().restart_all_itvls)

    def __save_archive(self, sceneMgr, roleMgr):

        print "Archiving.."

        archive = Archives()
        #archive.read_from_file()
        archive.save_archive(sceneMgr.export_sceneArcPkg(),
                             [roleMgr.export_arcPkg()],
                             -1,
                             "archive1")

    def check_event(self, event):

        print event, " happen"

    def dialog_show(self):

        demo = LoadPlot()

        demo.init_interface(2)

        demo.dialogue_next()

    def print_accept_event(self, event):

        print event
        #pass

game = GameWorld_Test()

game.run()



