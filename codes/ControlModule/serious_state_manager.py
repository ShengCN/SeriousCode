# coding=utf-8
from direct.fsm.FSM import FSM
from direct.showbase.MessengerGlobal import messenger


class SeriousFSM(FSM):
    def __init__(self):
        FSM.__init__(self,'SeriousFSM')

    def enterMenu(self):
        print '现在是菜单状态'
        messenger.send("serious_menu")
        
    def exitMenu(self):
        print '退出菜单状态'
        self.__window.destroy()
        self.__menu_window.destroy()

    # 参数用来决定是新建游戏还是载入
    def enterGame(self,isNew):
        print '进入游戏状态'
        if isNew:
            print '新建游戏'
            messenger.send("serious_new_game")
        else:
            print '读取游戏'
            messenger.send("serious_load_game")

    def exitGame(self):
        print '退出游戏状态'
        self.__game_window.destroy()

    def enterSetting(self):
        print '进入设置界面'

    def exitSetting(self):
        print '退出设置界面'
        self.__setting_window.destroy()

    def set_menu_window(self,window):
        self.__menu_window = window

    def set_game_window(self,window):
        self.__game_window = window

    def set_setting_window(self,window):
        self.__setting_window = window

# myFSM = SeriousFSM()
# myFSM.request('Walk')
# currentFSM = myFSM.state
# print '确定当前状态是:',currentFSM

# myFSM.request('Swim')
# currentFSM = myFSM.state
# print "确定当前状态是",currentFSM