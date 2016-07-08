
from SeriousTools.effert_msg_dispatcher import EffertMsgDispatcher
from direct.showbase.ShowBase import ShowBase

class Demo(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        dispatcher = EffertMsgDispatcher()
        dispatcher.accept_msg("w")

        self.accept("w_effert", self.print_w)
        self.accept("w_effert_end", self.print_w_up)

        print dispatcher.get_eventMessageMap()

    def print_w(self):

        print "w"

    def print_w_up(self):

        print "w-up"

demo = Demo()
demo.run()