# -*- coding:utf-8 -*-

from SceneModule.camera_controller import CameraController

from direct.showbase.ShowBase import ShowBase

class Test(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        model = self.loader.loadModel("/e/models/ralph")
        model.reparentTo(self.render)
        model.setPos(0, 0, 0)

        self.disableMouse()
        #self.trackball.node().setPos(0, 10, -2)
        self.cam.setPos(0, 100, 100)
        self.cam.lookAt(0, 0, 0)

        camCtrlr = CameraController(self.cam, globalClock)

        camCtrlr.focus_on(model, 10)
        print self.cam.getPos()

        camCtrlr.set_camToggleHost(self)

        camCtrlr.add_toggle_to_opt("y", "move_forward")
        camCtrlr.add_toggle_to_opt("z", "rotate_up")
        camCtrlr.add_toggle_to_opt("x", "rotate_down")

        # self.accept("y", camCtrlr.accept_event, ["move_forward", True])
        # self.accept("y-up", camCtrlr.accept_event, ["move_forward", False])
        # self.accept("h", camCtrlr.accept_event, ["move_backward", True])
        # self.accept("h-up", camCtrlr.accept_event, ["move_backward", False])
        # self.accept("g", camCtrlr.accept_event, ["move_left", True])
        # self.accept("g-up", camCtrlr.accept_event, ["move_left", False])
        # self.accept("j", camCtrlr.accept_event, ["move_right", True])
        # self.accept("j-up", camCtrlr.accept_event, ["move_right", False])
        # self.accept("t", camCtrlr.accept_event, ["move_up", True])
        # self.accept("t-up", camCtrlr.accept_event, ["move_up", False])
        # self.accept("u", camCtrlr.accept_event, ["move_down", True])
        # self.accept("u-up", camCtrlr.accept_event, ["move_down", False])
        #
        # self.accept("q", camCtrlr.accept_event, ["rotate_h_cw", True])
        # self.accept("q-up", camCtrlr.accept_event, ["rotate_h_cw", False])
        # self.accept("w", camCtrlr.accept_event, ["rotate_h_ccw", True])
        # self.accept("w-up", camCtrlr.accept_event, ["rotate_h_ccw", False])
        # self.accept("a", camCtrlr.accept_event, ["rotate_p_cw", True])
        # self.accept("a-up", camCtrlr.accept_event, ["rotate_p_cw", False])
        # self.accept("s", camCtrlr.accept_event, ["rotate_p_ccw", True])
        # self.accept("s-up", camCtrlr.accept_event, ["rotate_p_ccw", False])
        # self.accept("z", camCtrlr.accept_event, ["rotate_r_cw", True])
        # self.accept("z-up", camCtrlr.accept_event, ["rotate_r_cw", False])
        # self.accept("x", camCtrlr.accept_event, ["rotate_r_ccw", True])
        # self.accept("x-up", camCtrlr.accept_event, ["rotate_r_ccw", False])

        self.taskMgr.add(camCtrlr.camera_control, "camera_control")

        camCtrlr.print_optsSwitch()

test = Test()
test.run()

