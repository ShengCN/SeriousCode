
from direct.showbase.ShowBase import ShowBase

class Demo(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        #self.accept("mouse1", self.print_event, ["mouse1"])
        self.accept("mouse1-repeat", self.print_event, ["mouse1-repeat"])

    def print_event(self, event):

        print event

demo = Demo()
demo.run()