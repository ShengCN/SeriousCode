# -*- coding:utf-8 -*-

# Author : 戴熹
#
# Last Updated : 2016-06-20
#
# Description : 相机控制器，为相机添加各种操作

import SeriousTools.SeriousTools as SeriousTools
from ArchiveModule.archive_package import ArchivePackage

from direct.showbase.MessengerGlobal import messenger
from panda3d.core import *
import math

# 定义常量
CAM_MOVE_FORWARD       = "move_forward"
CAM_MOVE_BACKWARD      = "move_backward"
CAM_MOVE_LEFT          = "move_left"
CAM_MOVE_RIGHT         = "move_right"
CAM_MOVE_UP            = "move_up"
CAM_MOVE_DOWN          = "move_down"
CAM_ROTATE_H_CW        = "rotate_h_cw"
CAM_ROTATE_H_CCW       = "rotate_h_ccw"
CAM_ROTATE_P_CW        = "rotate_p_cw"
CAM_ROTATE_P_CCW       = "rotate_p_ccw"
CAM_ROTATE_R_CW        = "rotate_r_cw"
CAM_ROTATE_R_CCW       = "rotate_r_ccw"
CAM_ROTATE_AROUND_UP   = "rotate_around_up"
CAM_ROTATE_AROUND_DOWN = "rotate_around_down"
CAM_ROTATE_AROUND_CW   = "rotate_around_cw"
CAM_ROTATE_AROUND_CCW  = "rotate_around_ccw"

class CameraController(object):

    def __init__(self):

        self.__camToCtrl = None    # 所要进行控制的相机
        self.__clock = None        # 全局时钟，偏移量的计算依赖于时钟
        self.__moveSpeed = 10      # 相机移动速度
        self.__rotateSpeed = 0.1    # 相机旋转速度

        self.__camCurrX = None
        self.__camCurrY = None
        self.__camCurrZ = None
        self.__camCurrH = None
        self.__camCurrP = None
        self.__camCurrR = None

        self.__camMoveOffset = 0   # 相机单位时间的偏移量
        self.__camRotateOffset = 0 # 相机单位事件的旋转量

        self.__objectToFocus = None
        self.__radius = 0
        self.__objectPrevPos = None

        self.__correctionFactorV = 2
        self.__correctionFactorH = 5

        self.__camToggleHost = None
        self.__parentNode = None

        self.__directionsVector = {
            "N"  : LVector3f(0, 1, 0),
            "NE" : LVector3f(1, 1, 0),
            "E"  : LVector3f(1, 0, 0),
            "ES" : LVector3f(1, -1, 0),
            "S"  : LVector3f(0, -1, 0),
            "SW" : LVector3f(-1, -1, 0),
            "W"  : LVector3f(-1, 0, 0),
            "WN" : LVector3f(-1, 1, 0)
        }

        # 每个控制选项所对应的函数
        self.__optsFunc = {
            CAM_MOVE_FORWARD       : self.__move_forward,
            CAM_MOVE_BACKWARD      : self.__move_backward,
            CAM_MOVE_LEFT          : self.__move_left,
            CAM_MOVE_RIGHT         : self.__move_right,
            CAM_MOVE_UP            : self.__move_up,
            CAM_MOVE_DOWN          : self.__move_down,
            CAM_ROTATE_H_CW        : self.__rotate_h_cw,
            CAM_ROTATE_H_CCW       : self.__rotate_h_ccw,
            CAM_ROTATE_P_CW        : self.__rotate_p_cw,
            CAM_ROTATE_P_CCW       : self.__rotate_p_ccw,
            CAM_ROTATE_R_CW        : self.__rotate_r_cw,
            CAM_ROTATE_R_CCW       : self.__rotate_r_ccw,
            CAM_ROTATE_AROUND_UP   : self.__rotate_around_up,
            CAM_ROTATE_AROUND_DOWN : self.__rotate_around_down,
            CAM_ROTATE_AROUND_CW   : self.__rotate_around_cw,
            CAM_ROTATE_AROUND_CCW  : self.__rotate_around_ccw
        }

        # 每个控制选项有两个开关，第一个是触发事件，第二个是开关函数
        self.__optsSwitch = {
            CAM_MOVE_FORWARD       : [False, True],
            CAM_MOVE_BACKWARD      : [False, True],
            CAM_MOVE_LEFT          : [False, True],
            CAM_MOVE_RIGHT         : [False, True],
            CAM_MOVE_UP            : [False, True],
            CAM_MOVE_DOWN          : [False, True],
            CAM_ROTATE_H_CW        : [False, True],
            CAM_ROTATE_H_CCW       : [False, True],
            CAM_ROTATE_P_CW        : [False, True],
            CAM_ROTATE_P_CCW       : [False, True],
            CAM_ROTATE_R_CW        : [False, True],
            CAM_ROTATE_R_CCW       : [False, True],
            CAM_ROTATE_AROUND_UP   : [False, True],
            CAM_ROTATE_AROUND_DOWN : [False, True],
            CAM_ROTATE_AROUND_CW   : [False, True],
            CAM_ROTATE_AROUND_CCW  : [False, True]
        }

        self.__toggleEventToOpts = dict()

        self.__arcPkg = ArchivePackage(arcPkgName = "camera",
                                       itemsName = [
                                           "pos",
                                           "hpr",
                                           "moveSpeed",
                                           "rotateSpeed",
                                           "focusObjId",
                                           "radius",
                                           "optsSwitch",
                                           "toggleEventToOpts",
                                           #"parentId"
                                       ])

    def bind_camera(self, camera):

        self.__camToCtrl = camera

        self.__parentNode = camera.getParent()

        self.__camCurrX = self.__camToCtrl.getX()
        self.__camCurrY = self.__camToCtrl.getY()
        self.__camCurrZ = self.__camToCtrl.getZ()
        self.__camCurrH = self.__camToCtrl.getH()
        self.__camCurrP = self.__camToCtrl.getP()
        self.__camCurrR = self.__camToCtrl.getR()

    """""""""""""""""""""
    相机控制事件处理函数
    """""""""""""""""""""

    def bind_ToggleHost(self, host):

        self.__camToggleHost = host

        #self.__camToggleHost.accept("update_camera", self.__correct_camera_to_object)

    def set_clock(self, clock):

        self.__clock = clock

    #########################################

    def add_toggle_to_opt(self, toggleEvent, opt):

        if opt in self.__optsSwitch.keys():

            self.__camToggleHost.accept(event = toggleEvent,
                                        method = self.__change_first_switch,
                                        extraArgs = [opt, True])

            self.__camToggleHost.accept(event = toggleEvent + "-up",
                                        method = self.__change_first_switch,
                                        extraArgs = [opt, False])

            self.__toggleEventToOpts[toggleEvent] = opt

    #########################################

    def __change_first_switch(self, key, value):

        self.__optsSwitch[key][0] = value

        #print key, " : ", value

    #########################################

    # 相机总控制
    def update_camera(self, task):

        #task.setTaskChain("cameraTaskChain")

        self.__dt = self.__clock.getDt()

        self.__camMoveOffset = self.__dt * self.__moveSpeed
        self.__camRotateOffset = self.__dt * self.__rotateSpeed

        # # 移动相机位置
        # if self.__optsSwitch[CAM_MOVE_FORWARD][0] and \
        #         self.__optsSwitch[CAM_MOVE_FORWARD][1]:
        #
        #     self.__move_forward()
        #
        #     #print self.__optsSwitch[CAM_MOVE_FORWARD]
        #
        # if self.__optsSwitch[CAM_MOVE_BACKWARD][0] and \
        #         self.__optsSwitch[CAM_MOVE_BACKWARD][1]:
        #
        #     self.__move_backward()
        #
        # if self.__optsSwitch[CAM_MOVE_LEFT][0] and \
        #         self.__optsSwitch[CAM_MOVE_LEFT][1]:
        #
        #     self.__move_left()
        #
        # if self.__optsSwitch[CAM_MOVE_RIGHT][0] and \
        #         self.__optsSwitch[CAM_MOVE_RIGHT][1]:
        #
        #     self.__move_right()
        #
        # if self.__optsSwitch[CAM_MOVE_UP][0] and \
        #         self.__optsSwitch[CAM_MOVE_UP][1]:
        #
        #     self.__move_up()
        #
        # if self.__optsSwitch[CAM_MOVE_DOWN][0] and \
        #         self.__optsSwitch[CAM_MOVE_DOWN][1]:
        #
        #     self.__move_down()
        #
        # # 移动相机镜头方向
        # if self.__optsSwitch[CAM_ROTATE_H_CW][0] and \
        #         self.__optsSwitch[CAM_ROTATE_H_CW][1]:
        #
        #     self.__rotate_h_cw()
        #
        # if self.__optsSwitch[CAM_ROTATE_H_CCW][0] and \
        #         self.__optsSwitch[CAM_ROTATE_H_CCW][1]:
        #
        #     self.__rotate_h_ccw()
        #
        # if self.__optsSwitch[CAM_ROTATE_P_CW][0] and \
        #         self.__optsSwitch[CAM_ROTATE_P_CW][1]:
        #
        #     self.__rotate_p_cw()
        #
        # if self.__optsSwitch[CAM_ROTATE_P_CCW][0] and \
        #         self.__optsSwitch[CAM_ROTATE_P_CCW][1]:
        #
        #     self.__rotate_p_ccw()
        #
        # if self.__optsSwitch[CAM_ROTATE_R_CW][0] and \
        #         self.__optsSwitch[CAM_ROTATE_R_CW][1]:
        #
        #     self.__rotate_r_cw()
        #
        # if self.__optsSwitch[CAM_ROTATE_R_CCW][0] and \
        #         self.__optsSwitch[CAM_ROTATE_R_CCW][1]:
        #
        #     self.__rotate_r_ccw()


        self.__update_camera()

        return task.cont

    # 相机跟踪物体
    def focus_on(self, target, radius):

        self.__objectToFocus = target
        self.__radius = radius

        self.__objectPrevPos = target.getPos()

        targetPos = target.getPos()
        cameraPos = self.__camToCtrl.getPos()

        #print "The Pos of Camera : ", cameraPos
        #print "The Pos of Target : ", targetPos

        ctVector = cameraPos - targetPos
        ctvLen = ctVector.length()
        ctVector.normalize()

        #print "The e Vector : ", ctVector

        disOffset = math.fabs(ctvLen - radius)

        #print "The Distance Offset ： ", disOffset

        if ctvLen > radius:

            cameraPos -= ctVector * disOffset

        elif ctvLen < radius:

            cameraPos += ctVector * disOffset

        #print "The Camera Move To : ", cameraPos

        self.__camCurrX = cameraPos[0]
        self.__camCurrY = cameraPos[1]
        self.__camCurrZ = cameraPos[2]

        self.__camToCtrl.setPos(cameraPos)
        self.__camToCtrl.lookAt(target)

        self.__update_directionsVector()

        self.turn_off_ctrl_options(
            options = [CAM_MOVE_FORWARD,
                       CAM_MOVE_BACKWARD,
                       CAM_MOVE_LEFT,
                       CAM_MOVE_RIGHT,
                       CAM_MOVE_UP,
                       CAM_MOVE_DOWN,
                       CAM_ROTATE_H_CW,
                       CAM_ROTATE_H_CCW,
                       CAM_ROTATE_P_CW,
                       CAM_ROTATE_P_CCW,
                       CAM_ROTATE_R_CW,
                       CAM_ROTATE_R_CCW])

        messenger.send("update_camera")

    """""""""""""""""
    相机控制选项开关函数
    """""""""""""""""

    # 开启控制选项
    def turn_on_ctrl_options(self, options=None):

        if options == None:

            for opt in self.__optsSwitch.keys():

                self.__optsSwitch[opt][1] = True

        else:

            for opt in options:

                if opt in self.__optsSwitch.keys():

                    self.__optsSwitch[opt][1] = True

    #########################################

    # 关闭控制选项
    def turn_off_ctrl_options(self, options=None):

        if options == None:

            for opt in self.__optsSwitch.keys():

                self.__optsSwitch[opt][1] = False

        else:

            for opt in options:

                if opt in self.__optsSwitch.keys():

                    self.__optsSwitch[opt][1] = False

    # 绑定设备输入
    def bind_input_to_(self, opt, inputEvent):

        if self.__optsFunc[opt] is not None:

            self.__optsFunc[opt][0] = inputEvent

    """""""""""""""""
    相机单个控制操作函数
    """""""""""""""""

    # 向前移动相机
    def __move_forward(self):

        self.__camCurrY -= self.__camMoveOffset

    # 向后移动相机
    def __move_backward(self):

        self.__camCurrY += self.__camMoveOffset

    # 向左移动相机
    def __move_left(self):

        self.__camCurrX += self.__camMoveOffset

    # 向右移动相机
    def __move_right(self):

        self.__camCurrX -= self.__camMoveOffset

    # 向上移动相机
    def __move_up(self):

        self.__camCurrZ += self.__camMoveOffset

    # 向下移动相机
    def __move_down(self):

        self.__camCurrZ -= self.__camMoveOffset

    # 绕Z轴顺时针旋转镜头
    def __rotate_h_cw(self):

        self.__camCurrH += self.__camRotateOffset

    # 绕Z轴逆时针旋转镜头
    def __rotate_h_ccw(self):

        self.__camCurrH -= self.__camRotateOffset

    # 绕X轴顺时针旋转镜头
    def __rotate_p_cw(self):

        self.__camCurrP += self.__camRotateOffset

    # 绕X轴逆时针旋转镜头
    def __rotate_p_ccw(self):

        self.__camCurrP -= self.__camRotateOffset

    # 绕Y轴顺时针旋转镜头
    def __rotate_r_cw(self):

        self.__camCurrR += self.__camRotateOffset

    # 绕Y轴逆时针旋转镜头
    def __rotate_r_ccw(self):

        self.__camCurrR -= self.__camRotateOffset

    # 绕聚焦物体向上旋转
    def __rotate_around_up(self):

        deltaAngle = self.__dt * self.__rotateSpeed * self.__correctionFactorV
        deltaAngle *= (math.pi / 180)

        ctVector = self.__camToCtrl.getPos() - self.__objectToFocus.getPos()

        e = Vec3(ctVector)
        e.normalize()

        n = Vec3(0, 0, 1)

        cosEN = SeriousTools.cos(e, n)

        c = math.acos(cosEN)

        if c > (math.pi / 2):

            c = math.pi - c

        a = math.pi / 2 - c

        if a + deltaAngle > math.pi / 3:

            deltaAngle = math.pi / 3 - a

        b = a + deltaAngle / 2

        deltaDis = 2 * self.__radius * math.cos((math.pi - deltaAngle) / 2)

        deltaZ = deltaDis * math.cos(b)

        cosH = math.fabs(self.__camCurrX) / ((self.__camCurrX) ** 2 + (self.__camCurrY) ** 2) ** 0.5
        sinH = math.fabs(self.__camCurrY) / ((self.__camCurrX) ** 2 + (self.__camCurrY) ** 2) ** 0.5

        deltaX = deltaDis * math.sin(b) * cosH
        deltaY = deltaDis * math.sin(b) * sinH

        if self.__camCurrX - self.__objectToFocus.getX() > 0 and \
            self.__camCurrY - self.__objectToFocus.getY() > 0:

            self.__camCurrX -= deltaX
            self.__camCurrY -= deltaY

        elif self.__camCurrX - self.__objectToFocus.getX() < 0 and \
              self.__camCurrY - self.__objectToFocus.getY() > 0:

            self.__camCurrX += deltaX
            self.__camCurrY -= deltaY

        elif self.__camCurrX - self.__objectToFocus.getX() < 0 and \
              self.__camCurrY - self.__objectToFocus.getY() < 0:

            self.__camCurrX += deltaX
            self.__camCurrY += deltaY

        elif self.__camCurrX - self.__objectToFocus.getX() > 0 and \
              self.__camCurrY - self.__objectToFocus.getY() < 0:

            self.__camCurrX -= deltaX
            self.__camCurrY += deltaY

        self.__camCurrZ += deltaZ

    # 绕聚焦物体向下旋转
    def __rotate_around_down(self):

        deltaAngle = self.__dt * self.__rotateSpeed * self.__correctionFactorV
        deltaAngle *= ( math.pi / 180 )

        ctVector = self.__camToCtrl.getPos() - self.__objectToFocus.getPos()

        e = Vec3(ctVector)
        e.normalize()

        n = Vec3(0, 0, 1)

        cosEN = SeriousTools.cos(e, n)

        c = math.acos(cosEN)

        if c > (math.pi / 2):

            c = math.pi / 2

        a = math.pi / 2 - c

        if c >= math.pi / 2:

            deltaAngle = 0#math.pi / 2 - c

        b = a + deltaAngle / 2

        deltaDis = 2 * self.__radius * math.cos((math.pi - deltaAngle) / 2)

        deltaZ = deltaDis * math.cos(b)

        cosH = math.fabs(self.__camCurrX) / ((self.__camCurrX) ** 2 + (self.__camCurrY) ** 2) ** 0.5
        sinH = math.fabs(self.__camCurrY) / ((self.__camCurrX) ** 2 + (self.__camCurrY) ** 2) ** 0.5

        deltaX = deltaDis * math.sin(b) * cosH
        deltaY = deltaDis * math.sin(b) * sinH

        if self.__camCurrX - self.__objectToFocus.getX() > 0 and \
            self.__camCurrY - self.__objectToFocus.getY() > 0:

            self.__camCurrX += deltaX
            self.__camCurrY += deltaY

        elif self.__camCurrX - self.__objectToFocus.getX() < 0 and \
              self.__camCurrY - self.__objectToFocus.getY() > 0:

            self.__camCurrX -= deltaX
            self.__camCurrY += deltaY

        elif self.__camCurrX - self.__objectToFocus.getX() < 0 and \
              self.__camCurrY - self.__objectToFocus.getY() < 0:

            self.__camCurrX -= deltaX
            self.__camCurrY -= deltaY

        elif self.__camCurrX - self.__objectToFocus.getX() > 0 and \
              self.__camCurrY - self.__objectToFocus.getY() < 0:

            self.__camCurrX += deltaX
            self.__camCurrY -= deltaY

        self.__camCurrZ -= deltaZ

    # 绕聚焦物体顺时针旋转
    def __rotate_around_cw(self):

        deltaAngle = self.__dt * self.__rotateSpeed * self.__correctionFactorH
        deltaAngle *= (math.pi / 180)

        deltaR = 2 * self.__radius * math.cos((math.pi / 2 - deltaAngle / 2))

        r = math.sqrt(self.__radius ** 2 - (self.__camCurrZ - self.__objectToFocus.getZ()) ** 2)

        deltaB = math.acos(1 - 0.5 * deltaR ** 2 / r ** 2)

        objX = self.__objectToFocus.getX()
        objY = self.__objectToFocus.getY()

        camCurrX = (self.__camCurrX - objX) * math.cos(deltaB) - (self.__camCurrY - objY) * math.sin(deltaB) + objX
        camCurrY = (self.__camCurrX - objX) * math.sin(deltaB) + (self.__camCurrY - objY) * math.cos(deltaB) + objY

        self.__camCurrX = camCurrX
        self.__camCurrY = camCurrY

    # 绕聚焦物体逆时针旋转
    def __rotate_around_ccw(self):

        deltaAngle = self.__dt * self.__rotateSpeed * self.__correctionFactorH
        deltaAngle *= (math.pi / 180)

        deltaR = 2 * self.__radius * math.cos((math.pi / 2 - deltaAngle / 2))

        r = math.sqrt(self.__radius ** 2 - (self.__camCurrZ - self.__objectToFocus.getZ()) ** 2)

        deltaB = math.acos(1 - 0.5 * deltaR ** 2 / r ** 2)

        objX = self.__objectToFocus.getX()
        objY = self.__objectToFocus.getY()

        camCurrX = (self.__camCurrX - objX) * math.cos(deltaB) + (self.__camCurrY - objY) * math.sin(deltaB) + objX
        camCurrY = (self.__camCurrY - objY) * math.cos(deltaB) - (self.__camCurrX - objX) * math.sin(deltaB) + objY

        self.__camCurrX = camCurrX
        self.__camCurrY = camCurrY

    """""""""""""""
    相机状态更新函数
    """""""""""""""
    # def __correct_camera_to_object(self):
    #
    #     if self.__objectToFocus is not None:
    #
    #         if self.__optsSwitch[CAM_ROTATE_AROUND_UP][0] and \
    #                 self.__optsSwitch[CAM_ROTATE_AROUND_UP][1]:
    #
    #             self.__rotate_around_up()
    #
    #             self.__update_cam_pos()
    #
    #         if self.__optsSwitch[CAM_ROTATE_AROUND_DOWN][0] and \
    #             self.__optsSwitch[CAM_ROTATE_AROUND_DOWN][1]:
    #             self.__rotate_around_down()
    #
    #             self.__update_cam_pos()
    #
    #         if self.__optsSwitch[CAM_ROTATE_AROUND_CW][0] and \
    #                 self.__optsSwitch[CAM_ROTATE_AROUND_CW][1]:
    #             self.__rotate_around_cw()
    #
    #             self.__update_cam_pos()
    #
    #             self.__update_directionsVector()
    #
    #         if self.__optsSwitch[CAM_ROTATE_AROUND_CCW][0] and \
    #                 self.__optsSwitch[CAM_ROTATE_AROUND_CCW][1]:
    #             self.__rotate_around_ccw()
    #
    #             self.__update_cam_pos()
    #
    #             self.__update_directionsVector()
    #
    #         objCurrPos = self.__objectToFocus.getPos()
    #
    #         self.__camToCtrl.setPos(self.__camToCtrl.getPos() + objCurrPos - self.__objectPrevPos)
    #
    #         self.focus_on(self.__objectToFocus, self.__radius)

    # 只有执行更新函数后相机的状态才会发生改变
    def __update_camera(self):

        # 如果相机没有聚焦在某个物体上，则相机的移动和旋转是相对于其前一个状态的
        if self.__objectToFocus is None:

            # self.__camToCtrl.setPos(self.__camCurrX,
            #                         self.__camCurrY,
            #                         self.__camCurrZ)
            self.__update_cam_pos()
            # self.__camToCtrl.setHpr(self.__camCurrH,
            #                         self.__camCurrP,
            #                         self.__camCurrR)
            self.__update_cam_hpr()
        # 如果相机聚焦在某个物体上，则相机围绕着以物体为中心的某个球面进行旋转，
        # 并且镜头始终朝向该物体，并且如果由玩家控制相机镜头的话，只能够将相机
        # 进行上下左右旋转，因此镜头的变化速度取决于self.__camRotateSpeed
        else:
            pass
            if self.__optsSwitch[CAM_ROTATE_AROUND_UP][0] and \
                    self.__optsSwitch[CAM_ROTATE_AROUND_UP][1]:

                self.__rotate_around_up()

                self.__update_cam_pos()

            if self.__optsSwitch[CAM_ROTATE_AROUND_DOWN][0] and \
                self.__optsSwitch[CAM_ROTATE_AROUND_DOWN][1]:

                self.__rotate_around_down()

                self.__update_cam_pos()

            if self.__optsSwitch[CAM_ROTATE_AROUND_CW][0] and \
                self.__optsSwitch[CAM_ROTATE_AROUND_CW][1]:

                self.__rotate_around_cw()

                self.__update_cam_pos()

                self.__update_directionsVector()

            if self.__optsSwitch[CAM_ROTATE_AROUND_CCW][0] and \
                self.__optsSwitch[CAM_ROTATE_AROUND_CCW][1]:

                self.__rotate_around_ccw()

                self.__update_cam_pos()

                self.__update_directionsVector()

            objCurrPos = self.__objectToFocus.getPos()
            camCurrPos = self.__camToCtrl.getPos()
            dVector = objCurrPos - camCurrPos
            dVector.setZ(0)
            dist = dVector.length()
            dVector.normalize()
            if dist > 120:
                self.__camToCtrl.setPos(camCurrPos + dVector * (dist - 120))
                dist = 120
            if dist < 80:
                self.__camToCtrl.setPos(camCurrPos - dVector * (80 - dist))
                dist = 80
            self.__camToCtrl.lookAt(self.__objectToFocus)
            self.__camCurrH = self.__camToCtrl.getH()
            self.__camCurrY = self.__camToCtrl.getY()
            self.__camCurrR = self.__camToCtrl.getR()
            self.__camCurrX = self.__camToCtrl.getX()
            self.__camCurrY = self.__camToCtrl.getY()
            self.__camCurrZ = self.__camToCtrl.getZ()
            # self.__camToCtrl.setPos(self.__camToCtrl.getPos() + objCurrPos - self.__objectPrevPos)
            #
            # self.focus_on(self.__objectToFocus, self.__radius)

    def __update_cam_pos(self):

        self.__camToCtrl.setPos(
            self.__camCurrX,
            self.__camCurrY,
            self.__camCurrZ
        )

    def __update_cam_hpr(self):

        self.__camToCtrl.setHpr(
            self.__camCurrH,
            self.__camCurrP,
            self.__camCurrR
        )

    def __update_directionsVector(self):

        # f = open("DirectionsVector.txt", "w")
        # f.write("----- DirectionsVector -----\n")

        dVector = self.__camToCtrl.getPos() - self.__objectToFocus.getPos()

        dVector.setZ(0)
        dVector.normalize()

        odvX = dVector.getX()
        odvY = dVector.getY()

        # f.write("odvX : " + str(odvX) + "\n")
        # f.write("odvY : " + str(odvY) + "\n")
        # f.write("dVector : " + str(dVector) + "\n")

        deltaAngle = 0
        self.__directionsVector["N"] = LPoint3f(odvX, odvY, 0)
        #f.write("dVector1 : " + str(dVector) + "\n")

        deltaAngle += math.pi / 4
        dvX = odvX * math.cos(deltaAngle) + odvY * math.sin(deltaAngle)
        dvY = odvY * math.cos(deltaAngle) - odvX * math.sin(deltaAngle)
        dVector.setX(dvX)
        dVector.setY(dvY)
        self.__directionsVector["NE"] = LPoint3f(dvX, dvY, 0)
        #f.write("dVector2 : " + str(dVector) + "\n")

        deltaAngle += math.pi / 4
        dvX = odvX * math.cos(deltaAngle) + odvY * math.sin(deltaAngle)
        dvY = odvY * math.cos(deltaAngle) - odvX * math.sin(deltaAngle)
        dVector.setX(dvX)
        dVector.setY(dvY)
        self.__directionsVector["E"] = LPoint3f(dvX, dvY, 0)
        #f.write("dVector3 : " + str(dVector) + "\n")

        deltaAngle += math.pi / 4
        dvX = odvX * math.cos(deltaAngle) + odvY * math.sin(deltaAngle)
        dvY = odvY * math.cos(deltaAngle) - odvX * math.sin(deltaAngle)
        dVector.setX(dvX)
        dVector.setY(dvY)
        self.__directionsVector["ES"] = LPoint3f(dvX, dvY, 0)
        #f.write("dVector4 : " + str(dVector) + "\n")

        deltaAngle += math.pi / 4
        dvX = odvX * math.cos(deltaAngle) + odvY * math.sin(deltaAngle)
        dvY = odvY * math.cos(deltaAngle) - odvX * math.sin(deltaAngle)
        dVector.setX(dvX)
        dVector.setY(dvY)
        self.__directionsVector["S"] = LPoint3f(dvX, dvY, 0)
        #f.write("dVector5 : " + str(dVector) + "\n")

        deltaAngle += math.pi / 4
        dvX = odvX * math.cos(deltaAngle) + odvY * math.sin(deltaAngle)
        dvY = odvY * math.cos(deltaAngle) - odvX * math.sin(deltaAngle)
        dVector.setX(dvX)
        dVector.setY(dvY)
        self.__directionsVector["SW"] = LPoint3f(dvX, dvY, 0)
        #f.write("dVector6 : " + str(dVector) + "\n")

        deltaAngle += math.pi / 4
        dvX = odvX * math.cos(deltaAngle) + odvY * math.sin(deltaAngle)
        dvY = odvY * math.cos(deltaAngle) - odvX * math.sin(deltaAngle)
        dVector.setX(dvX)
        dVector.setY(dvY)
        self.__directionsVector["W"] = LPoint3f(dvX, dvY, 0)
        #f.write("dVector7 : " + str(dVector) + "\n")

        deltaAngle += math.pi / 4
        dvX = odvX * math.cos(deltaAngle) + odvY * math.sin(deltaAngle)
        dvY = odvY * math.cos(deltaAngle) - odvX * math.sin(deltaAngle)
        dVector.setX(dvX)
        dVector.setY(dvY)
        self.__directionsVector["WN"] = LPoint3f(dvX, dvY, 0)
        #f.write("dVector8 : " + str(dVector) + "\n")

        # f.write("%s : %s\n" % ("N", self.__directionsVector["N"]))
        # f.write("%s : %s\n" % ("NE", self.__directionsVector["NE"]))
        # f.write("%s : %s\n" % ("E", self.__directionsVector["E"]))
        # f.write("%s : %s\n" % ("ES", self.__directionsVector["ES"]))
        # f.write("%s : %s\n" % ("S", self.__directionsVector["S"]))
        # f.write("%s : %s\n" % ("SW", self.__directionsVector["SW"]))
        # f.write("%s : %s\n" % ("W", self.__directionsVector["W"]))
        # f.write("%s : %s\n" % ("WN", self.__directionsVector["WN"]))
        # f.write("--------------------")
        # f.close()

        # x0 = self.__camCurrX
        # y0 = self.__camCurrY
        # x1 = self.__objectToFocus.getX()
        # y1 = self.__objectToFocus.getY()
        # x2 = 0
        # y2 = 0
        #
        # dVector = self.__objectToFocus
        # pVector = self.__camToCtrl
        # dVector.setZ(0)
        # pVector.setZ(0)
        #
        # deltaAngle = 0
        # x2 = (x1 - x0) * math.cos(deltaAngle) + (y1 - y0) * math.sin(deltaAngle) + x0
        # y2 = (y1 - y0) * math.cos(deltaAngle) - (x1 - x0) * math.sin(deltaAngle) + y0
        # dVector.setX(x2)
        # dVector.setY(y2)
        # rVector = dVector - pVector
        # rVector.normalize()
        # self.__directionsVector["N"] = Vec3(odvX, odvY, 0)

        #print self.__directionsVector

    """""""""""""""""""""
    成员变量的get和set函数
    """""""""""""""""""""

    # 相机的移动速度
    def set_moveSpeed(self, speed):

        self.__moveSpeed = max(speed, 0.0)

    def get_moveSpeed(self):

        return self.__moveSpeed

    # 相机的旋转速度
    def set_rotateSpeed(self, speed):

        self.__rotateSpeed = max(speed, 0.0)

    def get_rotateSpeed(self):

        return self.__rotateSpeed

    def get_arcPkg(self):

        return self.__arcPkg

    def get_camToCtrl(self):

        return self.__camToCtrl

    def get_focusObj(self):

        return self.__objectToFocus

    def get_rotateRadius(self):

        return self.__radius

    def get_toggleHost(self):

        return self.__camToggleHost

    def set_toggleEventToOpts(self, toggleEventToOpts):

        self.__toggleEventToOpts = toggleEventToOpts

    def get_toggleEventToOpts(self):

        return self.__toggleEventToOpts

    def set_one_directionsVector(self, key, value):

        if self.__directionsVector.has_key(key):

            self.__directionsVector[key] = value

    def set_directionsVector(self, directions):

        self.__directionsVector = directions

    def get_one_directionsVector(self, key):

        return SeriousTools.find_value_in_dict(key, self.__directionsVector)

    def get_directionsVector(self):

        return self.__directionsVector

    def set_optsSwitch(self, optsSwitch):

        self.__optsSwitch = optsSwitch

    def get_optsSwitch(self):

        return self.__optsSwitch

    """""""""""""""""""""""""""""
    一些数据的打印函数，主要用于调试
    """""""""""""""""""""""""""""

    def print_optsFunc(self):

        print "-- Options Map Functions --"

        for k, v in self.__optsFunc.iteritems():

            print "%s : %s" % (k, v)

        print "--------------------"

    def print_optsSwitch(self):

        print "-- Options Switch --"

        for k, v in self.__optsSwitch.iteritems():

            print "%s : %s" % (k, v)

        print "--------------------"