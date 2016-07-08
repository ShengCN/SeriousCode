
from direct.showbase.ShowBase import ShowBase

class KeyboardInputDemo(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        self.accept("w", self.print_event, ["w"])
        self.accept("w-up", self.print_event, ["w-up"])
        self.accept("s", self.print_event, ["s"])
        self.accept("s-up", self.print_event, ["s-up"])
        self.accept("a", self.print_event, ["a"])
        self.accept("a-up", self.print_event, ["a-up"])
        self.accept("d", self.print_event, ["d"])
        self.accept("d-up", self.print_event, ["d-up"])


    def print_event(self, event):

        print event + " happen"

demo = KeyboardInputDemo()
demo.run()