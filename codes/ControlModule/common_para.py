# coding=utf-8
from panda3d.core import Point3

modelRootPath = "/d/SeriousPresent"

CONFIG = """
framebuffer-multisample 1
multisamples 2
framebuffer-stencil #t
threading-model Cull/Draw
fullscreen #f
interpolate-frames 1
window-title Reborn : The Soul Of Devil
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
text-encoding utf8
text-default-font /c/Windows/Fonts/FZSTK.ttf
"""

"""""""""""""""
主角模型
"""""""""""""""
HUNTER_PATH = modelRootPath + "/Material/ModelEGGS/Hunter/hunter_AlarmPos1.egg"
HUNTER_ACTION_PATH = {
    "run" : modelRootPath + "/Material/ModelEGGS/Hunter/hunter_RunWithGun1.egg",
    "run_back" : modelRootPath + "/Material/ModelEGGS/Hunter/hunter_RunBackWithGun1.egg",
    "rda" : modelRootPath + "/Material/ModelEGGS/Hunter/hunter_WithGunRightDefence.egg",
    "lda" : modelRootPath + "/Material/ModelEGGS/Hunter/hunter_WithGunLeftDefenceUpdate.egg",
    "attack":modelRootPath+ "/Material/ModelEGGS/Hunter/hunter_Attack1.egg",
    "stand":modelRootPath+"/Material/ModelEGGS/Hunter/hunter_Alarm1Pose.egg"
}
BULLET_PATH = modelRootPath + "/Material/ModelEGGS/Bullet/Bullet.egg"

"""""""""""""""
僵尸模型
"""""""""""""""
WIFE_ZOMBIE_PATH = modelRootPath + "/Material/ModelEGGS/WifeZombie/WifeZombie_Stand.egg"
WIFE_ZOMBIE_ACTION_PATH = {
    "walk" : modelRootPath + "/Material/ModelEGGS/WifeZombie/WifeZombie_Walk.egg",
    "attack": modelRootPath+"/Material/ModelEGGS/WifeZombie/WifeZombie_Attack3.egg"
}

HOOK_ZOMBIE = modelRootPath + "/Material/ModelEGGS/HookZombie/HookZombie_Pose.egg"
HOOK_ZOMBIE_ACTION_PATH = {
    "walk" : modelRootPath+"/Material/ModelEGGS/HookZombie/HookZombie_Walk_v2.egg",
    "attack": modelRootPath+"/Material/ModelEGGS/HookZombie/HookZombie_OffencePose.egg"
}

ZOMBIE = modelRootPath + "/Material/ModelEGGS/Zombie/Zombie_Pose.egg"
ZOMBIE_ACTION_PATH = {
    "walk" : modelRootPath+"/Material/ModelEGGS/Zombie/Zombie_Walk.egg",
    "attack": modelRootPath+"/Material/ModelEGGS/Zombie/Zombie_Offence.egg"
}
"""""""""""""""
传送点位置
"""""""""""""""
VILLAGE_TO_ROOM = Point3(-250,-50,2)
VILLAGE_TO_OUTER = Point3(-225,-290,2)
VILLAGE_TO_HOME = Point3(140,-306,2)
HOME_TO_VILLAGE = Point3(-18,-18,0)
OUTER_TO_VILLAGE = Point3(446,-40,0)
ROOM_TO_VILLAGE = Point3(5,-85,3)


"""""""""""""""
NPC模型
"""""""""""""""
GIRL = modelRootPath + "/Material/ModelEGGS/Girl/GIRL_Pose.egg"
NUN = modelRootPath + "/Material/ModelEGGS/Nun/NUNV_Pose.egg"
STEALER = modelRootPath + "/Material/ModelEGGS/Stealer/StealerWithPose.egg"
CHEST = modelRootPath + "/Material/ModelEGGS/Chest/Chest1.egg"
CHEST_OPEN = {
    "open" : modelRootPath + "/Material/ModelEGGS/Chest/Chest1_Open.egg"
}
"""""""""""""""
HOME场景
"""""""""""""""
RING = modelRootPath + "/Material/ModelEGGS/Ring/ring.egg"

HOME = modelRootPath + "/Material/ModelEGGS/Home/home.egg"

"""""""""""""""
VILLAGE场景
"""""""""""""""
VILLAGE = modelRootPath + "/Material/ModelEGGS/Village/village.egg"

"""""""""""""""
OUTER场景
"""""""""""""""
OUTER = modelRootPath + "/Material/ModelEGGS/Outer/Outer_v2.egg"

# TERRAIN_H = modelRootPath + "/Material/Terrain/ground.jpg"
# TERRAIN_Map = modelRootPath + "/Material/Terrain/ground.jpg"
# HOUSE_PATH = modelRootPath + "/Material/ModelEGGS/Village/house1.egg"

"""""""""""""""
教堂场景
"""""""""""""""
ROOM = modelRootPath + "/Material/ModelEGGS/Room/Room.egg"

"""""""""""""""
test 用
"""""""""""""""
TEST_HOUSE1 = modelRootPath + "/house_test/house1.egg"
TEST_HOUSE2 = modelRootPath + "/house_test/house2.egg"
TEST_HOUSE3 = modelRootPath + "/house_test/house3.egg"
TEST_MAIN_SCENE = modelRootPath + "/house_test/village.egg"
TEST_SECOND_SCENE = modelRootPath + "/house_test/Outer_v2.egg"

"""""""""""""""
玩家的游戏参数
"""""""""""""""
SPEED = 50
JUMP_HEIGHT = 1.0
JUMP_SPEED = 10.0
ENEMY_MASS = 0.0
BULLET_MASS = 10.0
BULLET_SPEED = 1000.0
BULLET_SIZE = 3.0
DANGER_LENGTH = 100
REBORN_TIME = 12000
BOSS_HP = 1000
CHANGE_SCENE_DISTANCE = 10
"""""""""""""""
AI 参数
"""""""""""""""
