# -*-coding:utf-8 -*-
# Author: codingblack
# Last Updated: 2016-06-29
# menu菜单
# 游戏的开始界面

from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenImage import OnscreenImage

from BulletEngineModule.serious_game_scene import SeriousGameScene, BoxWorld
from ResourcesModule.resources_manager import ResourcesManager
from RoleModule.role_manager import RoleManager
from SceneModule.scene_manager import SceneManager
from keyboard_mouse_handler import *
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import *
from panda3d.core import *
from direct.task import Task
from ControlModule.common_para import *

class MainMenu(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.__destroyMainGame = False
        self.__destroySetting = False
        self.__destroyTrade = False
        self.__destroyArchive = False
        self.__destroyHelp=False

        self.__imagePath = "../../resources/images/"

        self.__weapon2=0
        self.__weapon3=0
        self.init_Mgr()
        self.current_scene = None
        self.current_scene_name = None
        self.change_scene_input()
        self.accept("escape", self.setting_menu)

    def init_Mgr(self):
        self.__rm = ResourcesManager()
        self.roleMgr = RoleManager()
        self.sceneMgr = SceneManager()
        self.sceneMgr.bind_RoleManager(self.roleMgr)
        self.sceneMgr.get_ActorMgr().bind_ResourcesManager(self.__rm)
        self.roleMgr.bind_ResourcesManager(self.__rm)

    # 监听场景切换
    def change_scene_input(self):
        self.accept("change_to_scene_village",self.change_to_village)
        self.accept("movie_over2",self.change_to_outer)
        self.accept("change_to_scene_home",self.change_to_home)
        self.accept("change_to_scene_room",self.change_to_room)
        # self.accept("change_to_scene_mountain",self.changeto)

    """""""""""""""
    所有界面（菜单、设置、游戏中）
    """""""""""""""
    # 菜单界面
    def start(self):
        # #全屏
        # self.setFullScreen(0)
        #load background image
        self.__image = OnscreenImage(image='../../resources/images/menu/home1.png',scale=1)
        self.__image.setSx(self.getAspectRatio())
        self.__image.setTransparency(TransparencyAttrib.MAlpha)

        # 监听输入
        self.__keyInput = MenuPlayerInputHandler()
        self.accept("NewGame",self.__new_game)
        self.accept("LoadGame",self.__load_game)
        self.accept("Description",self.__description)
        self.accept("ChangeMenu",self.__change_menu)

        self.taskMgr.add(self.adapt_main, 'adaptMainTask')

        archiveList = [
            # {"name": "Archive1", "progress": "50%", "time": "2016/07/05 09:49", "id": "1"},
            # {"name": "Archive2", "progress": "60%", "time": "2016/07/05 09:50", "id": "2"},
            # {"name": "Archive3", "progress": "70%", "time": "2016/07/05 09:51", "id": "3"}
            # {"name":"Archive4","progress":"80%","time":"2016/07/05 09:52","id":"4"},
            # {"name":"Archive5","progress":"90%","time":"2016/07/05 09:53","id":"5"}
        ]
        self.accept("x",self.trade_menu)
        self.accept("y",self.archive_menu,[self,False,archiveList])
        self.accept("z",self.main_game)
        self.accept("u", self.destroy_main_game)

    def adapt_main(self, Task):
        self.__image.setSx(self.getAspectRatio())

        return Task.cont

    """""""""""""""
    菜单界面函数
    """""""""""""""
    # 清除菜单界面，清除监听
    def destroy(self):
        self.__image.destroy()
        self.__keyInput.destroy()
        taskMgr.remove('adaptMainTask')

    # 私有函数，进入新建游戏界面
    def __new_game(self):
        print '进入new game'
        # self.destroy()
        messenger.send("serious_new_game")
        print '发送了serious_new_game'

    # 私有函数，进入读取游戏界面
    def __load_game(self):
        print '进入load game'
        messenger.send("serious_load_game")
        print '发送了serious_load_game'
    # 设置全屏
    def setFullScreen(self,full):
        if full == 1 :
            self.__setFullscreen(2560,1600,0,0,1)
        else:
            self.__setFullscreen(800,600,150,50,0)

        # 私有函数，进入about界面

    def __description(self):
        print '进入description'
        messenger.send("serious_description")
        print '发送了serious_description'

    # 私有函数，选择全屏
    def __setFullscreen(self, width, height, posX, posY, full):
        winProps = WindowProperties()
        winProps.setOrigin(posX, posY)
        winProps.setSize(width, height)
        winProps.setFullscreen(full)
        self.win.requestProperties(winProps)

    # 私有函数，用来自建的选择进入的游戏界面
    def __change_mode(self,image_path):
        self.__image.setImage(image_path)

    # 私有函数，更改游戏目录
    def __change_menu(self):
        switch_count = {0:'../../resources/images/menu/home1.png',
                        1:'../../resources/images/menu/home2.png',
                        2:'../../resources/images/menu/home3.png',
                        3:'../../resources/images/menu/home4.png',}
        self.__change_mode(switch_count[self.__keyInput.get_count()])

    def __exit(self):
        print '进入exit'
        # self.__del__()
        exit()

    """""""""""""""
    设置界面函数
    """""""""""""""
    #设置界面
    def setting_menu(self):
        if self.__destroySetting==False:
            # 关闭游戏场景帧更新
            self.sceneMgr.get_ActorMgr().stop_all_itvls()
            if self.current_scene != None:
                self.current_scene.stop_update()
            # 设置界面背景图
            self.__background = OnscreenImage(image=self.__imagePath+'settings/setting_frame.png', pos=(0, 0, 0),
                                              scale=(1.0, 0, 0.7))
            self.__background.setTransparency(TransparencyAttrib.MAlpha)

            ##滑动条
            self.__slider = DirectSlider(pos=(0.16, 0, 0.26), scale=0.5, value=0.5, command=self.__setMusicSliderVolume,
                                         frameSize=(-1.0, 0.9, -0.06, 0.06),
                                         image=self.__imagePath + 'settings/slide_bar.png',
                                         image_pos=(-0.05, 0, 0.0), image_scale=(1.0, 0, 0.05),
                                         thumb_image='../../resources/images/settings/slide_btn.png',
                                         thumb_image_pos=(-0.0, 0, 0.0), thumb_image_scale=0.1,
                                         thumb_frameSize=(0.0, 0.0, 0.0, 0.0))
            self.__slider.setTransparency(TransparencyAttrib.MAlpha)

            # self.__musicButton = DirectButton(pos=(0.9, 0, 0.75), text="Close", scale=0.1, pad=(0.2, 0.2), rolloverSound=None,
            #                                   clickSound=None, command=self.toggleMusicBox,extraArgs=[base])

            # 继续按钮
            self.__continueButton = DirectButton(pos=(-0.25, 0, 0.0), text="", scale=(0.2, 0, 0.1),
                                                 command=self.__continue_game,
                                                 image=(self.__imagePath + 'settings/btn_continue_0.png',
                                                        self.__imagePath + 'settings/btn_continue_0.png',
                                                        self.__imagePath + 'settings/btn_continue_1.png'),
                                                 frameColor=(0, 0, 0, 0))
            self.__continueButton.setTransparency(TransparencyAttrib.MAlpha)

            # 存档按钮
            self.__saveButton = DirectButton(pos=(0.33, 0, 0.0), text="", scale=(0.2, 0, 0.1), command=self.__save_game,
                                             image=(self.__imagePath + 'settings/btn_save_0.png',
                                                    self.__imagePath + 'settings/btn_save_0.png',
                                                    self.__imagePath + 'settings/btn_save_1.png'),
                                             frameColor=(0, 0, 0, 0))
            self.__saveButton.setTransparency(TransparencyAttrib.MAlpha)

            # 帮助按钮
            self.__helpButton = DirectButton(pos=(-0.25, 0, -0.25), text="", scale=(0.2, 0, 0.1), command=self.__help,
                                             image=(self.__imagePath + 'settings/btn_help_0.png',
                                                    self.__imagePath + 'settings/btn_help_0.png',
                                                    self.__imagePath + 'settings/btn_help_1.png'),
                                             frameColor=(0, 0, 0, 0))
            self.__helpButton.setTransparency(TransparencyAttrib.MAlpha)

            # 回到主界面按钮
            self.__homeButton = DirectButton(pos=(0.33, 0, -0.25), text="", scale=(0.2, 0, 0.1), command=self.__return_home,
                                             image=(self.__imagePath + 'settings/btn_home_0.png',
                                                    self.__imagePath + 'settings/btn_home_0.png',
                                                    self.__imagePath + 'settings/btn_home_1.png'),
                                             frameColor=(0, 0, 0, 0))
            self.__homeButton.setTransparency(TransparencyAttrib.MAlpha)

            # 设置滑动条value
            self.__slider['value'] = self.__rm.get_volume()

            self.__destroySetting = True

    #移除设置界面所有控件
    def setting_destroy(self):
        if self.__destroySetting==True:
            self.__background.destroy()
            self.__rm.set_volume(self.__slider['value'])
            self.__slider.destroy()
            # self.__musicButton.destroy()
            self.__continueButton.destroy()
            self.__saveButton.destroy()
            self.__helpButton.destroy()
            self.__homeButton.destroy()
            self.__destroySetting = False

    # 设置音乐声音大小
    def __setMusicSliderVolume(self):
        newVolume = self.__slider.guiItem.getValue()
        self.__rm.set_volume(newVolume)

    # 设置界面，私有函数,继续游戏
    def __continue_game(self):
        self.setting_destroy()
        self.destroy_help()
        if self.current_scene != None:
            self.current_scene.reset_update()
        self.sceneMgr.get_ActorMgr().restart_all_itvls()
        self.__rm.play_sound(7)

    # 设置界面，私有函数,存档
    def __save_game(self):
        self.setting_destroy()
        archiveList=self.__rm.show_archives()
        if (len(archiveList)!=0):
            self.current_scene.destroy()
            self.archive_menu(self,True,archiveList)
        self.__rm.play_sound(7)

    # 设置界面，私有函数,游戏帮助
    def __help(self):
        self.setting_destroy()
        self.__rm.play_sound(7)
        # False:help
        # True:description
        self.help_menu(False)

    # 设置界面，私有函数,回到主界面
    def __return_home(self):
        self.current_scene.destroy()
        self.setting_destroy()
        self.__rm.play_sound(7)
        self.destroy_main_game()
        self.start()

    """""""""""""""
    交易界面函数
    """""""""""""""
    # 交易界面
    def trade_menu(self):
        if self.__destroyTrade == False:

            # self.__imageDict = dict()
            self.__imageDict["tf"] = self.__imagePath + "trade/trade_frame.png"
            self.__imageDict["tfbg"] = self.__imagePath + "trade/trade_frame_bg.png"
            self.__imageDict["purchase1"] = self.__imagePath + "trade/btn_perchase_0.png"
            self.__imageDict["purchase2"] = self.__imagePath + "trade/btn_perchase_1.png"
            self.__imageDict["btnUp"] = self.__imagePath + "trade/btn_up.png"
            self.__imageDict["btnDown"] = self.__imagePath + "trade/btn_down.png"
            self.__imageDict["closeTrade"] = self.__imagePath + "trade/close.png"

            #交易数量
            self.__tradeMedicineNumber = 0
            self.__tradeGun1Number = 0
            self.__tradeGun2Number = 0
            #物品单价
            self.__medicineUnitPrice = 20
            self.__gun1UnitPrice = 20
            self.__gun2UnitPrice = 20

            #交易金钱
            self.__medicineTotalPrice = 0
            self.__gun1TotalPrice = 0
            self.__gun2TotalPrice = 0

            #交易总价
            self.__totalPrice = 0

            #实际购买物品数量与金钱
            self.__purchaseMedicineNumber = 0
            self.__purchaseMoney = 0

            # 交易背景
            self.__tradeFrame = OnscreenImage(image=self.__imageDict["tf"], pos=(0.0, 0.0, 0.0), scale=(1.0, 0, 0.5))
            self.__tradeFrame.setTransparency(TransparencyAttrib.MAlpha)

            # 交易药品输入框
            self.__tradeMedicine = DirectEntry(text="", scale=.042, width=2.0, pos=(-0.71, 0.0, -0.005), text_scale=1.2,
                                               numLines=1, focus=0, text_fg=(0.5, 0.5, 0.5, 1), frameColor=(0, 0, 0, 0),
                                               initialText="0",
                                               command=self.set_medicine_total_price)
            # 增加药品按钮
            self.__medicineUpBtn = DirectButton(pos=(-0.625, 0, 0.03), text="", scale=(0.035, 0, 0.035),
                                                command=self.__add_medicine,
                                                image=self.__imageDict["btnUp"],
                                                frameColor=(0, 0, 0, 0))
            self.__medicineUpBtn.setTransparency(TransparencyAttrib.MAlpha)
            # 减少药品按钮
            self.__medicineDownBtn = DirectButton(pos=(-0.625, 0, -0.02), text="", scale=(0.035, 0, 0.029),
                                                  command=self.__minus_medicine,
                                                  image=self.__imageDict["btnDown"],
                                                  frameColor=(0, 0, 0, 0))
            self.__medicineDownBtn.setTransparency(TransparencyAttrib.MAlpha)

            # 交易枪支1输入框
            self.__tradeGun1 = DirectEntry(text="12", scale=.042, width=2.0, pos=(-0.17, 0.0, -0.005), text_scale=1.2,
                                           numLines=1, focus=0, text_fg=(0.5, 0.5, 0.5, 1), frameColor=(0, 0, 0, 0),
                                           initialText="0",
                                           command=self.set_gun1_total_price)
            # 增加枪支1按钮
            self.__gun1UpBtn = DirectButton(pos=(-0.08, 0, 0.03), text="", scale=(0.035, 0, 0.035),
                                            command=self.__add_gun1,
                                            image=self.__imageDict["btnUp"],
                                            frameColor=(0, 0, 0, 0))
            self.__gun1UpBtn.setTransparency(TransparencyAttrib.MAlpha)
            # 减少枪支1按钮
            self.__gun1DownBtn = DirectButton(pos=(-0.08, 0, -0.02), text="", scale=(0.035, 0, 0.029),
                                              command=self.__minus_gun1,
                                              image=self.__imageDict["btnDown"],
                                              frameColor=(0, 0, 0, 0))
            self.__gun1DownBtn.setTransparency(TransparencyAttrib.MAlpha)

            # 交易枪支2输入框
            self.__tradeGun2 = DirectEntry(text="12", scale=.042, width=2.0, pos=(0.38, 0.0, -0.005), text_scale=1.2,
                                           numLines=1, focus=0, text_fg=(0.5, 0.5, 0.5, 1), frameColor=(0, 0, 0, 0),
                                           initialText="0",
                                           command=self.set_gun2_total_price)
            # 增加枪支2按钮
            self.__gun2UpBtn = DirectButton(pos=(0.46, 0, 0.03), text="", scale=(0.035, 0, 0.035),
                                            command=self.__add_gun2,
                                            image=self.__imageDict["btnUp"],
                                            frameColor=(0, 0, 0, 0))
            self.__gun2UpBtn.setTransparency(TransparencyAttrib.MAlpha)
            # 减少枪支2按钮
            self.__gun2DownBtn = DirectButton(pos=(0.46, 0, -0.02), text="", scale=(0.035, 0, 0.029),
                                              command=self.__minus_gun2,
                                              image=self.__imageDict["btnDown"],
                                              frameColor=(0, 0, 0, 0))

            self.__gun2DownBtn.setTransparency(TransparencyAttrib.MAlpha)

            # 药品单价显示框
            self.__medicineCoin = OnscreenText(str(self.__medicineUnitPrice), pos=(-0.45, -0.005), scale=0.06,
                                               fg=(0.5, 0.5, 0.5, 1), shadow=(0, 0, 0, 1),
                                               mayChange=True)
            # 枪支1单价显示框
            self.__gun1Coin = OnscreenText(str(self.__gun1UnitPrice), pos=(0.09, -0.005), scale=0.06,
                                           fg=(0.5, 0.5, 0.5, 1), shadow=(0, 0, 0, 1),
                                           mayChange=True)
            # 枪支2单价显示框
            self.__gun2Coin = OnscreenText(str(self.__gun2UnitPrice), pos=(0.63, -0.005), scale=0.06,
                                           fg=(0.5, 0.5, 0.5, 1), shadow=(0, 0, 0, 1),
                                           mayChange=True)
            # 购买物品总价
            self.__totalCoin = OnscreenText(str(self.__totalPrice), pos=(-0.01, -0.21), scale=0.06,
                                            fg=(0.5, 0.5, 0.5, 1), shadow=(0, 0, 0, 1),
                                            mayChange=True)
            # 交易按钮
            self.__tradeBtn = DirectButton(pos=(0.0, 0, -0.32), text="", scale=(0.15, 0, 0.07),
                                           command=self.purchase,
                                           image=(self.__imageDict["purchase1"],
                                                  self.__imageDict["purchase1"],
                                                  self.__imageDict["purchase2"]),
                                           frameColor=(0, 0, 0, 0))
            self.__tradeBtn.setTransparency(TransparencyAttrib.MAlpha)

            self.__closeBtn = DirectButton(pos=(0.88, 0, 0.33), text="", scale=(0.035, 0, 0.035),
                                           command=self.destroy_trade,
                                           image=self.__imageDict["closeTrade"],
                                           frameColor=(0, 0, 0, 0))
            self.__closeBtn.setTransparency(TransparencyAttrib.MAlpha)

            self.__destroyTrade = True

    #移除交易界面控件
    def destroy_trade(self):
        self.__rm.play_sound(7)
        if self.__destroyTrade == True:
            self.__tradeFrame.destroy()
            self.__tradeMedicine.destroy()
            self.__medicineUpBtn.destroy()
            self.__medicineDownBtn.destroy()
            self.__tradeGun1.destroy()
            self.__gun1UpBtn.destroy()
            self.__gun1DownBtn.destroy()
            self.__tradeGun2.destroy()
            self.__gun2UpBtn.destroy()
            self.__gun2DownBtn.destroy()
            self.__medicineCoin.destroy()
            self.__gun1Coin.destroy()
            self.__gun2Coin.destroy()
            self.__totalCoin.destroy()
            self.__tradeBtn.destroy()
            self.__closeBtn.destroy()
            self.__destroyTrade = False

            messenger.send("trade_over")

    # 更新购买药品总价
    def set_medicine_total_price(self, textEntered):
        if (int(textEntered) <= 99 and int(textEntered) >= 0):
            self.__tradeMedicineNumber = int(textEntered)
        else:
            self.__tradeMedicineNumber = 0
            self.__tradeMedicine.set(str(self.__tradeMedicineNumber))
        self.__medicineTotalPrice = self.__medicineUnitPrice * int(self.__tradeMedicineNumber)
        # self.__medicineCoin.setText(str(self.__medicineTotalPrice))
        self.__totalPrice = self.__medicineTotalPrice + self.__gun1TotalPrice + self.__gun2TotalPrice
        self.__totalCoin.setText(str(self.__totalPrice))

    # 更新购买枪支1总价
    def set_gun1_total_price(self, textEntered):
        if (int(textEntered) <= 1 and int(textEntered) >= 0 and self.__weapon2==0):
            self.__tradeGun1Number = int(textEntered)
        else:
            self.__tradeGun1Number = 0
            self.__tradeGun1.set(str(self.__tradeGun1Number))
        self.__gun1TotalPrice = self.__gun1UnitPrice * int(self.__tradeGun1Number)
        # self.__gun1Coin.setText(str(self.__gun1TotalPrice))
        self.__totalPrice = self.__medicineTotalPrice + self.__gun1TotalPrice + self.__gun2TotalPrice
        self.__totalCoin.setText(str(self.__totalPrice))

    # 更新购买枪支2总价
    def set_gun2_total_price(self, textEntered):
        if (int(textEntered) <= 1 and int(textEntered) >= 0 and self.__weapon3==0):
            self.__tradeGun2Number = int(textEntered)
        else:
            self.__tradeGun2Number = 0
            self.__tradeGun2.set(str(self.__tradeGun2Number))
        self.__gun2TotalPrice = self.__gun2UnitPrice * int(self.__tradeGun2Number)
        # self.__gun2Coin.setText(str(self.__gun2TotalPrice))
        self.__totalPrice = self.__medicineTotalPrice + self.__gun1TotalPrice + self.__gun2TotalPrice
        self.__totalCoin.setText(str(self.__totalPrice))

    # 增加药品数量
    def __add_medicine(self):
        if (self.__tradeMedicineNumber <= 99):
            self.__tradeMedicineNumber += 1
            self.__tradeMedicine.set(str(self.__tradeMedicineNumber))
            self.set_medicine_total_price(str(self.__tradeMedicineNumber))

    # 减少药品数量
    def __minus_medicine(self):
        if (self.__tradeMedicineNumber > 0):
            self.__tradeMedicineNumber -= 1
            self.__tradeMedicine.set(str(self.__tradeMedicineNumber))
            self.set_medicine_total_price(str(self.__tradeMedicineNumber))

    # 增加枪支1数量
    def __add_gun1(self):
        if (self.__tradeGun1Number == 0 and self.__weapon2==0):
            self.__tradeGun1Number += 1
            self.__tradeGun1.set(str(self.__tradeGun1Number))
            self.set_gun1_total_price(str(self.__tradeGun1Number))

    # 减少枪支1数量
    def __minus_gun1(self):
        if (self.__tradeGun1Number == 1):
            self.__tradeGun1Number -= 1
            self.__tradeGun1.set(str(self.__tradeGun1Number))
            self.set_gun1_total_price(str(self.__tradeGun1Number))

    # 增加枪支2数量
    def __add_gun2(self):
        if (self.__tradeGun2Number == 0 and self.__weapon3==0):
            self.__tradeGun2Number += 1
            self.__tradeGun2.set(str(self.__tradeGun2Number))
            self.set_gun2_total_price(str(self.__tradeGun2Number))

    # 减少枪支2数量
    def __minus_gun2(self):
        if (self.__tradeGun2Number == 1):
            self.__tradeGun2Number -= 1
            self.__tradeGun2.set(str(self.__tradeGun2Number))
            self.set_gun2_total_price(str(self.__tradeGun2Number))

    #点击购买按钮
    # 涉及role_manager
    def purchase(self):
        self.__purchaseMedicineNumber = self.__tradeMedicineNumber
        self.__purchaseMoney = self.__totalPrice
        if self.__weapon2==0:
            self.__weapon2=self.__tradeGun1Number
        if self.__weapon3 == 0:
            self.__weapon3=self.__tradeGun2Number
        self.destroy_trade()
        money=self.get_money()
        medicineNumber=self.get_medicine_number()
        self.set_money(money-self.__purchaseMoney)
        self.set_medicine_number(medicineNumber+self.__purchaseMedicineNumber)

        # 传输数据给角色
        # 涉及role_manager
        print "money:",self.__purchaseMoney,"medicine:",self.__purchaseMedicineNumber
        self.roleMgr.buy_attachment(self.__purchaseMoney,self.__purchaseMedicineNumber,self.__weapon2,self.__weapon3)

    # #获取购买数量与花费金钱
    # def get_purchase(self):
    #     medicineNumber = self.__purchaseMedicineNumber
    #     money = self.__purchaseMoney
    #     return [money, medicineNumber]
    #
    # #判断是否关闭交易界面
    # def get_destroy_trade(self):
    #     return self.__destroyTrade

    # #设置购买药品数量
    # def set_purchase_medicine_number(self):
    #     self.__purchaseMedicineNumber = 0
    #
    # # 设置花费金钱数
    # def set_purchase_money(self):
    #     self.__purchaseMoney = 0


    """""""""""""""
    游戏进行中界面函数
    """""""""""""""
    def main_game(self):
        if self.__destroyMainGame == False:

            self.__destroyMonsterHpBar=False

            self.__imageDict = dict()
            self.__imageDict["cbg"] = self.__imagePath + "main/charactor_bg.png"
            self.__imageDict["ctop"] = self.__imagePath + "main/charactor_top.png"
            self.__imageDict["charactor"] = self.__imagePath + "main/charactor3.png"
            self.__imageDict["hpbg"] = self.__imagePath + "main/hp_bg.png"
            self.__imageDict["hp"] = self.__imagePath + "main/hp.png"
            self.__imageDict["hp1"] = self.__imagePath + "main/hp1.png"
            self.__imageDict["mf"] = self.__imagePath + "main/medicine_frame.png"
            self.__imageDict["medicine"] = self.__imagePath + "main/medicine.png"
            self.__imageDict["gf"] = self.__imagePath + "main/gun_frame.png"
            self.__imageDict["gun1"] = self.__imagePath + "main/gun_1.png"
            self.__imageDict["gun2"] = self.__imagePath + "main/gun_2.png"
            self.__imageDict["gun3"] = self.__imagePath + "main/gun_3.png"
            self.__imageDict["coin"] = self.__imagePath + "main/coin.png"

            self.__money = 0
            self.__medicineNum = 0

            self.__blood = 100
            self.__monsterBlood = 100

            #人物头像
            self.__charactorBg = OnscreenImage(image=self.__imageDict["cbg"], pos=(-1.6, 0, 0.8), scale=(0.16, 0, 0.16))
            self.__charactorBg.setTransparency(TransparencyAttrib.MAlpha)

            self.__charactorTop = OnscreenImage(image=self.__imageDict["ctop"], pos=(-1.6, 0, 0.8),
                                                scale=(0.16, 0, 0.16))
            self.__charactorTop.setTransparency(TransparencyAttrib.MAlpha)

            self.__charactor = OnscreenImage(image=self.__imageDict["charactor"], pos=(-1.6, 0, 0.8),
                                             scale=(0.15, 0, 0.15))
            self.__charactor.setTransparency(TransparencyAttrib.MAlpha)

            #血条
            self.__hpBg = OnscreenImage(image=self.__imageDict["hpbg"], pos=(-1.14, 0, 0.85), scale=(0.30, 0, 0.02))
            self.__hpBg.setTransparency(TransparencyAttrib.MAlpha)

            # self.__hp = OnscreenImage(image=self.__imageDict["hp"], pos=(-1.14, 0, 0.85), scale=(0.30, 0, 0.02))
            # self.__hp.setTransparency(TransparencyAttrib.MAlpha)

            self.__hpBar = DirectWaitBar(text="", value=100, pos=(-1.14, 0, 0.85), scale=(0.297, 0, 0.22),
                                         barTexture=self.__imageDict["hp"], frameColor=(0, 0, 0, 0))
            self.__hpBar.setTransparency(TransparencyAttrib.MAlpha)

            #药品
            self.__medicineFrame = OnscreenImage(image=self.__imageDict["mf"], pos=(-1.33, 0, 0.72),
                                                 scale=(0.09, 0, 0.09))
            self.__medicineFrame.setTransparency(TransparencyAttrib.MAlpha)

            self.__medicine = OnscreenImage(image=self.__imageDict["medicine"], pos=(-1.33, 0, 0.72),
                                            scale=(0.09, 0, 0.09))
            self.__medicine.setTransparency(TransparencyAttrib.MAlpha)

            #枪支
            self.__gunFrame = OnscreenImage(image=self.__imageDict["gf"], pos=(-0.95, 0, 0.72), scale=(0.27, 0, 0.09))
            self.__gunFrame.setTransparency(TransparencyAttrib.MAlpha)

            self.__gun = OnscreenImage(image=self.__imageDict["gun1"], pos=(-0.95, 0, 0.72), scale=(0.27, 0, 0.09))
            self.__gun.setTransparency(TransparencyAttrib.MAlpha)

            #金钱
            self.__coin = OnscreenImage(image=self.__imageDict["coin"], pos=(1.35, 0, 0.8), scale=(0.40, 0, 0.065))
            self.__coin.setTransparency(TransparencyAttrib.MAlpha)

            #药品数量
            self.__medicineNumber = OnscreenText(str(self.__medicineNum), pos=(-1.27, 0.65), scale=0.05,
                                                 fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
                                                 mayChange=True)
            #金钱数量
            self.__coinNumber = OnscreenText(str(self.__money), pos=(1.40, 0.78), scale=0.07, fg=(1, 1, 1, 1),
                                             shadow=(0, 0, 0, 1),
                                             mayChange=True)

            self.taskMgr.add(self.change_data_task, 'changeDataTask')

            self.__destroyMainGame = True

    #监听人物血量，金钱，药物的变化
    # 涉及role_manager
    def change_data_task(self,Task):
        money=self.roleMgr.get_player_money()
        medicine=self.roleMgr.get_player_medicine_num()
        hp=self.roleMgr.get_player_hp()
        if money!=self.get_money():
            self.set_money(money)
        if medicine!=self.get_medicine_number():
            self.set_medicine_number(medicine)
        if hp!=self.get_blood():
            self.set_blood(hp)

        #怪物
        if self.__destroyMonsterHpBar==True:
            monsterBlood=self.roleMgr.get_Boss_hp()
            if monsterBlood!=self.get_monster_blood():
                self.set_monster_blood(monsterBlood)
        return Task.cont

    def take_medicine(self):
        self.roleMgr.take_medicine()

    #显示怪物血条
    def show_monster_hp(self):
        if self.__destroyMonsterHpBar==False:
            # 怪物血条
            self.__monsterHpBg = OnscreenImage(image=self.__imageDict["hpbg"], pos=(-0.14, 0, 0.85),
                                               scale=(-0.30, 0, 0.02))
            self.__monsterHpBg.setTransparency(TransparencyAttrib.MAlpha)
            self.__monsterHpBar = DirectWaitBar(text="", value=100, pos=(-0.14, 0, 0.85), scale=(-0.297, 0, 0.22),
                                                barTexture=self.__imageDict["hp1"], frameColor=(0, 0, 0, 0))
            self.__monsterHpBar.setTransparency(TransparencyAttrib.MAlpha)

            self.__destroyMonsterHpBar = True

    #移除游戏进行中主要界面
    def destroy_main_game(self):
        if self.__destroyMainGame == True:
            self.__charactorBg.destroy()
            self.__charactorTop.destroy()
            self.__charactor.destroy()

            self.__hpBg.destroy()
            self.__hpBar.destroy()
            # self.__hp.destroy()

            self.__medicineFrame.destroy()
            self.__medicine.destroy()
            self.__medicineNumber.destroy()

            self.__gunFrame.destroy()
            self.__gun.destroy()

            self.__coin.destroy()
            self.__coinNumber.destroy()

            taskMgr.remove('changeDataTask')

            if self.__destroyMonsterHpBar==True:
                self.destroy_monster_hp()

            self.__destroyMainGame = False

    #移除怪物血条
    def destroy_monster_hp(self):
        if self.__destroyMonsterHpBar == True:
            self.__monsterHpBg.destroy()
            self.__monsterHpBar.destroy()
            self.__destroyMonsterHpBar = False

    #设置金钱
    def set_money(self, money):
        if money >= 0:
            self.__money = money
            self.__coinNumber.setText(str(self.__money))

    #获得当前金钱
    def get_money(self):
        return self.__money

    #设置药品数量
    def set_medicine_number(self, number):
        if number >= 0:
            self.__medicineNum = number
            self.__medicineNumber.setText(str(self.__medicineNum))

    #获得当前药品数量
    def get_medicine_number(self):
        return self.__medicineNum

    #换成枪支1
    def set_gun1(self):
        self.__gun.setImage(self.__imageDict["gun1"])
        self.__gun.setTransparency(TransparencyAttrib.MAlpha)

        # 涉及role_manager
        self.roleMgr.change_weapon(1)

    #换成枪支2
    def set_gun2(self):
        if self.__weapon2==1:
            print self.__imageDict

            self.__gun.setImage(self.__imageDict["gun2"])
            self.__gun.setTransparency(TransparencyAttrib.MAlpha)

            # 涉及role_manager
            self.roleMgr.change_weapon(2)

    #换成枪支3
    def set_gun3(self):
        if self.__weapon3 == 1:
            self.__gun.setImage(self.__imageDict["gun3"])
            self.__gun.setTransparency(TransparencyAttrib.MAlpha)

            #涉及role_manager
            self.roleMgr.change_weapon(3)

    #设置血量
    def set_blood(self, blood):
        self.__blood = blood
        self.__hpBar['value'] = self.__blood

    # 设置怪物血量
    def set_monster_blood(self, blood):
        if self.__destroyMonsterHpBar==True:
            self.__monsterBlood = blood
            print "========================,hp:",blood
            self.__monsterHpBar['value'] = self.__monsterBlood/10.0

    #获得当前血量
    def get_blood(self):
        return self.__blood

    def get_monster_blood(self):
        return self.__monsterBlood

    """""""""""""""
    存档界面函数
    """""""""""""""
    def archive(self):
        archiveList = self.__rm.show_archives()
        self.archive_menu(self, False, archiveList)

    def archive_menu(self,base,operate,archiveList):
        if self.__destroyArchive == False:

            self.__imageDict = dict()
            self.__imageDict["bg"] = self.__imagePath + "archive/bg.png"
            self.__imageDict["abg"] = self.__imagePath + "archive/archive_bg5.png"
            self.__imageDict["cube"] = self.__imagePath + "archive/archive_cube.png"
            self.__imageDict["slider"] = self.__imagePath + "archive/slider1.png"
            self.__imageDict["close"] = self.__imagePath + "archive/close.png"

            self.__archiveContentList = list()
            self.__archiveGuiList = list()

            # 加载：False
            # 存储：True
            self.__loadOrSave = operate

            #加载存档中的记录
            self.set_archive_list(archiveList)

            #界面背景
            self.__archiveBg = OnscreenImage(image=self.__imageDict["bg"], pos=(0, 0, 0), scale=1)
            self.__archiveBg.setSx(base.getAspectRatio())
            self.__archiveBg.setTransparency(TransparencyAttrib.MAlpha)

            # myframe = DirectScrolledFrame(canvasSize=(-1.4, 1.4, -1.5, 1.5), frameSize=(-1.5, 1.5, -0.9,0.9),frameColor=(0, 0, 0, 0),
            #                               incButton_frameColor=(0,0,0,0),
            #                               verticalScroll_image=self.__imageDict["slider"],verticalScroll_frameSize=(1.4, 1.5, -0.9,0.9))
            #存档界面滑动条
            self.__archiveSlider = DirectScrollBar(range=(0, 12), value=0, pageSize=2, orientation=DGG.VERTICAL,
                                            pos=(1.4, 0.0, 0.0),
                                            frameColor=(0, 0, 0, 0), thumb_frameColor=(0, 0, 0, 0), command=self.move,
                                            thumb_image=self.__imageDict["slider"], thumb_image_scale=(0.03, 0, 0.5),
                                            incButton_frameColor=(0, 0, 0, 0), decButton_frameColor=(0, 0, 0, 0))
            self.__archiveSlider.setTransparency(TransparencyAttrib.MAlpha)

            #第一条存档
            self.__archive1 = DirectButton(pos=(0.0, 0.0, 0.6), scale=(1.2, 0, 0.3),
                                           command=self.clickArchive, extraArgs=[1],
                                           image=self.__imageDict["abg"],
                                           frameColor=(0, 0, 0, 0))
            self.__archive1.setTransparency(TransparencyAttrib.MAlpha)
            self.__archive1Name = OnscreenText(str("Archive 1"), pos=(-0.75, 0.6), scale=0.1, fg=(1, 1, 1, 1),
                                               shadow=(0, 0, 0, 1),
                                               mayChange=True)
            self.__archive1Progress = OnscreenText(str("Progress:" + "50%"), pos=(-0.1, 0.6), scale=0.1,
                                                   fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
                                                   mayChange=True)
            self.__archive1Time = OnscreenText(str("2016/07/05 09:49"), pos=(0.65, 0.6), scale=0.09, fg=(1, 1, 1, 1),
                                               shadow=(0, 0, 0, 1),
                                               mayChange=True)
            self.__archiveGuiList.append(dict())
            self.__archiveGuiList[0]["button"] = self.__archive1
            self.__archiveGuiList[0]["name"] = self.__archive1Name
            self.__archiveGuiList[0]["progress"] = self.__archive1Progress
            self.__archiveGuiList[0]["time"] = self.__archive1Time
            # self.__archiveGuiList[0]["name"].setText(self.__archiveContentList[0]["name"])
            self.__archiveGuiList[0]["progress"].setText(self.__archiveContentList[0]["progress"])
            self.__archiveGuiList[0]["time"].setText(self.__archiveContentList[0]["time"])

            # 第二条存档
            self.__archive2 = DirectButton(pos=(0.0, 0.0, 0.0), scale=(1.2, 0, 0.3),
                                           command=self.clickArchive, extraArgs=[2],
                                           image=self.__imageDict["abg"],
                                           frameColor=(0, 0, 0, 0))

            self.__archive2.setTransparency(TransparencyAttrib.MAlpha)
            self.__archive2Name = OnscreenText(str("Archive 2"), pos=(-0.75, 0.0), scale=0.1, fg=(1, 1, 1, 1),
                                               shadow=(0, 0, 0, 1),
                                               mayChange=True)
            self.__archive2Progress = OnscreenText(str("Progress:" + "50%"), pos=(-0.1, 0.0), scale=0.1,
                                                   fg=(1, 1, 1, 1),
                                                   shadow=(0, 0, 0, 1),
                                                   mayChange=True)
            self.__archive2Time = OnscreenText(str("2016/07/05 09:49"), pos=(0.65, 0.0), scale=0.09, fg=(1, 1, 1, 1),
                                               shadow=(0, 0, 0, 1),
                                               mayChange=True)
            self.__archiveGuiList.append(dict())
            self.__archiveGuiList[1]["button"] = self.__archive2
            self.__archiveGuiList[1]["name"] = self.__archive2Name
            self.__archiveGuiList[1]["progress"] = self.__archive2Progress
            self.__archiveGuiList[1]["time"] = self.__archive2Time
            # self.__archiveGuiList[1]["name"].setText(self.__archiveContentList[1]["name"])
            self.__archiveGuiList[1]["progress"].setText(self.__archiveContentList[1]["progress"])
            self.__archiveGuiList[1]["time"].setText(self.__archiveContentList[1]["time"])

            # 第三条存档
            self.__archive3 = DirectButton(pos=(0.0, 0.0, -0.6), scale=(1.2, 0, 0.3),
                                           command=self.clickArchive, extraArgs=[3],
                                           image=self.__imageDict["abg"],
                                           frameColor=(0, 0, 0, 0))
            self.__archive3.setTransparency(TransparencyAttrib.MAlpha)
            self.__archive3Name = OnscreenText(str("Archive 3"), pos=(-0.75, 0.6), scale=0.1, fg=(1, 1, 1, 1),
                                               shadow=(0, 0, 0, 1),
                                               mayChange=True)
            self.__archive3Progress = OnscreenText(str("Progress:" + "50%"), pos=(-0.1, -0.6), scale=0.1,
                                                   fg=(1, 1, 1, 1),
                                                   shadow=(0, 0, 0, 1),
                                                   mayChange=True)
            self.__archive3Time = OnscreenText(str("2016/07/05 09:49"), pos=(0.65, -0.6), scale=0.09, fg=(1, 1, 1, 1),
                                               shadow=(0, 0, 0, 1),
                                               mayChange=True)
            self.__archiveGuiList.append(dict())
            self.__archiveGuiList[2]["button"] = self.__archive3
            self.__archiveGuiList[2]["name"] = self.__archive3Name
            self.__archiveGuiList[2]["progress"] = self.__archive3Progress
            self.__archiveGuiList[2]["time"] = self.__archive3Time
            # self.__archiveGuiList[2]["name"].setText(self.__archiveContentList[2]["name"])
            self.__archiveGuiList[2]["progress"].setText(self.__archiveContentList[2]["progress"])
            self.__archiveGuiList[2]["time"].setText(self.__archiveContentList[2]["time"])

            # 第四条存档
            self.__archive4 = DirectButton(pos=(0.0, 0.0, -1.2), scale=(1.2, 0, 0.3),
                                           command=self.clickArchive, extraArgs=[4],
                                           image=self.__imageDict["abg"],
                                           frameColor=(0, 0, 0, 0))
            self.__archive4.setTransparency(TransparencyAttrib.MAlpha)
            self.__archive4Name = OnscreenText(str("Archive 4"), pos=(-0.75, 0.6), scale=0.1, fg=(1, 1, 1, 1),
                                               shadow=(0, 0, 0, 1),
                                               mayChange=True)
            self.__archive4Progress = OnscreenText(str("Progress:" + "50%"), pos=(-0.1, -1.2), scale=0.1,
                                                   fg=(1, 1, 1, 1),
                                                   shadow=(0, 0, 0, 1),
                                                   mayChange=True)
            self.__archive4Time = OnscreenText(str("2016/07/05 09:49"), pos=(0.65, -1.2), scale=0.09, fg=(1, 1, 1, 1),
                                               shadow=(0, 0, 0, 1),
                                               mayChange=True)
            self.__archiveGuiList.append(dict())
            self.__archiveGuiList[3]["button"] = self.__archive4
            self.__archiveGuiList[3]["name"] = self.__archive4Name
            self.__archiveGuiList[3]["progress"] = self.__archive4Progress
            self.__archiveGuiList[3]["time"] = self.__archive4Time
            # self.__archiveGuiList[3]["name"].setText(self.__archiveContentList[3]["name"])
            self.__archiveGuiList[3]["progress"].setText(self.__archiveContentList[3]["progress"])
            self.__archiveGuiList[3]["time"].setText(self.__archiveContentList[3]["time"])

            # 第五条存档
            self.__archive5 = DirectButton(pos=(0.0, 0.0, -1.8), scale=(1.2, 0, 0.3),
                                           command=self.clickArchive, extraArgs=[5],
                                           image=self.__imageDict["abg"],
                                           frameColor=(0, 0, 0, 0))
            self.__archive5.setTransparency(TransparencyAttrib.MAlpha)
            self.__archive5Name = OnscreenText(str("Archive 5"), pos=(-0.75, -1.8), scale=0.1, fg=(1, 1, 1, 1),
                                               shadow=(0, 0, 0, 1),
                                               mayChange=True)
            self.__archive5Progress = OnscreenText(str("Progress:" + "50%"), pos=(-0.1, -1.8), scale=0.1,
                                                   fg=(1, 1, 1, 1),
                                                   shadow=(0, 0, 0, 1),
                                                   mayChange=True)
            self.__archive5Time = OnscreenText(str("2016/07/05 09:49"), pos=(0.65, -1.8), scale=0.09, fg=(1, 1, 1, 1),
                                               shadow=(0, 0, 0, 1),
                                               mayChange=True)
            self.__archiveGuiList.append(dict())
            self.__archiveGuiList[4]["button"] = self.__archive5
            self.__archiveGuiList[4]["name"] = self.__archive5Name
            self.__archiveGuiList[4]["progress"] = self.__archive5Progress
            self.__archiveGuiList[4]["time"] = self.__archive5Time
            # self.__archiveGuiList[4]["name"].setText(self.__archiveContentList[4]["name"])
            self.__archiveGuiList[4]["progress"].setText(self.__archiveContentList[4]["progress"])
            self.__archiveGuiList[4]["time"].setText(self.__archiveContentList[4]["time"])

            self.__closeArchiveBtn = DirectButton(pos=(1.7, 0, 0.9), text="", scale=(0.05, 0, 0.05),
                                                  command=self.destroy_archive, extraArgs=[True],
                                                  image=self.__imageDict["close"],
                                                  frameColor=(0, 0, 0, 0))
            self.__closeArchiveBtn.setTransparency(TransparencyAttrib.MAlpha)

            self.taskMgr.add(self.adapt_archive, 'adaptArchiveTask')

            self.destroy_trade()
            self.destroy_main_game()
            self.setting_destroy()

            self.__destroyArchive = True

    def adapt_archive(self, Task):
        self.__archiveBg.setSx(self.getAspectRatio())

        return Task.cont

    #设置存档记录
    def set_archive_list(self, archiveList):
        self.__archiveContentList = list()
        for index in range(len(archiveList)):
            self.__archiveContentList.append(dict())
            self.__archiveContentList[index]["name"] = archiveList[index]["name"]
            self.__archiveContentList[index]["progress"] = "Progress:" + archiveList[index]["progress"]
            self.__archiveContentList[index]["time"] = archiveList[index]["time"]
            self.__archiveContentList[index]["id"] = archiveList[index]["id"]
        if len(archiveList) < 5:
            for index in range(5 - len(archiveList)):
                self.__archiveContentList.append(dict())
                self.__archiveContentList[index + len(archiveList)]["name"] = ""
                self.__archiveContentList[index + len(archiveList)]["progress"] = ""
                self.__archiveContentList[index + len(archiveList)]["time"] = ""
                self.__archiveContentList[index + len(archiveList)]["id"] = -1

    #移除存档界面控件
    def destroy_archive(self, tf):
        self.__loadOrSave = tf
        self.__rm.play_sound(7)
        if self.__destroyArchive == True:
            for index in range(len(self.__archiveGuiList)):
                self.__archiveGuiList[index]["button"].destroy()
                self.__archiveGuiList[index]["name"].destroy()
                self.__archiveGuiList[index]["progress"].destroy()
                self.__archiveGuiList[index]["time"].destroy()

            self.__archiveSlider.destroy()
            self.__archiveBg.destroy()
            self.__closeArchiveBtn.destroy()
            self.__destroyArchive = False

            taskMgr.remove('adaptArchiveTask')

            if self.__loadOrSave == True:
                self.start()

    #滑动滑动条
    def move(self):
        value = self.__archiveSlider.getValue()
        posY = value / 10.0 + 0.6
        for index in range(len(self.__archiveGuiList)):
            self.__archiveGuiList[index]["button"].setZ(posY - index * 0.6)
            self.__archiveGuiList[index]["name"].setY(posY - index * 0.6)
            self.__archiveGuiList[index]["progress"].setY(posY - index * 0.6)
            self.__archiveGuiList[index]["time"].setY(posY - index * 0.6)

    #点击存档条
    def clickArchive(self, id):
        if self.__loadOrSave == False:#读档
            print self.__archiveContentList[id - 1]["id"]
            roleArchive=self.__rm.select_archives(int(self.__archiveContentList[id - 1]["id"]))
            #archive函数
            self.room_scene()
            self.roleMgr.import_arcPkg(roleArchive)
            # resource_manager,读档,id=id
            self.destroy_archive(False)
        else:#存档
            print self.__archiveContentList[id - 1]["id"]
            #sceneArchive,roleArchive
            roleArchive=self.roleMgr.export_arcPkg()
            self.__rm.save_archives(roleArchive,int(self.__archiveContentList[id - 1]["id"]))
            # resource_manager,存档,id=0
            self.destroy_archive(True)

    """""""""""""""
    游戏说明界面函数
    """""""""""""""

    def help_menu(self, ft):
        # False:help
        # True:description
        self.__helpOrDescription = ft
        if self.__destroyHelp == False:
            self.__helpBg = OnscreenImage(image=self.__imagePath + "helpMenu.png", pos=(0, 0, 0), scale=1)
            self.__helpBg.setSx(self.getAspectRatio())
            self.__helpBg.setTransparency(TransparencyAttrib.MAlpha)

            self.__closeHlepBtn = DirectButton(pos=(1.7, 0, 0.9), text="", scale=(0.05, 0, 0.05),
                                               command=self.destroy_help,
                                               image=self.__imagePath + 'archive/close.png',
                                               frameColor=(0, 0, 0, 0))
            self.__closeHlepBtn.setTransparency(TransparencyAttrib.MAlpha)

            self.taskMgr.add(self.adapt_help, 'adaptTask')

            self.destroy_main_game()

            self.__destroyHelp = True

    #移除帮助界面控件
    def destroy_help(self):
        if self.__destroyHelp == True:
            self.__destroyHelp = False
            self.__helpBg.destroy()
            self.__closeHlepBtn.destroy()

            taskMgr.remove('adaptTask')
            # False:help
            # True:description
            if self.__helpOrDescription == True:
                self.start()
            else:
                self.main_game()


    #更新画面大小，自适应
    def adapt_help(self,Task):
        self.__helpBg.setSx(self.getAspectRatio())

        return Task.cont

    """""""""""""""
    游戏界面函数
    """""""""""""""
    def game_window(self):
        self.game_begin()

    def game_begin(self):
        self.__rm.play_media(self, 1)
        self.accept("movie_over1",self.outer_scene)
        self.accept("trade_menu", self.trade_menu)
        self.accept("1", self.set_gun1)
        self.accept("2", self.set_gun2)
        self.accept("3", self.set_gun3)
        self.accept("q", self.take_medicine)

    def village_scene(self,pos=Point3(-30,30,0)):
        # reset
        self.sceneMgr.reset()
        self.roleMgr.reset()
        self.sceneMgr.build_on(self)
        # print "village当前所有NPC：", self.roleMgr.get_one_kind_of_roles("NPCRole")
        # #.sceneMgr.get_ActorMgr().set_storyLine(2)
        # print "village storyLine : ", self.sceneMgr.get_ActorMgr().get_storyLine()
        self.current_scene = None
        self.current_scene = SeriousGameScene(self,self.sceneMgr,self.roleMgr,self.__rm)
        self.current_scene_name = "village"
        self.accept("space",self.debug_current_scene)
        box = BoxWorld(Point3(0, -400, 0),Point3(0, 450, 0),Point3(-360, 0, 0),Point3(380, 0, 0))
        self.current_scene.load_game_scene(VILLAGE,5,box)
        # 为房屋建立碰撞体
        # self.village.add_rigid_box(Point3(-290,-93,0),Vec3(20,40,10),Vec3(-45,0,0),1)
        self.current_scene.add_rigid_box(Point3(-350, -143, 0), Vec3(70, 130, 10), Vec3(-48, 0, 0), 1)
        self.current_scene.add_rigid_box(Point3(-344.367, 225.982, 0), Vec3(84, 34, 10), Vec3(-135, 0, 0), 2)
        self.current_scene.add_rigid_box(Point3(-10.4909, 445.62, 0), Vec3(34, 27, 10), Vec3(-180, 0, 0), 3)
        self.current_scene.add_rigid_box(Point3(342.876, -178.818, 0), Vec3(106, 27, 10), Vec3(66, 0, 0), 4)
        self.current_scene.add_rigid_box(Point3(183.335, -338.465, 0), Vec3(40, 30, 10), Vec3(20, 0, 0), 5)
        self.current_scene.add_rigid_box(Point3(205.281, 36.0989, 0), Vec3(65, 20, 10), Vec3(78, 0, 0), 6)
        self.current_scene.add_rigid_box(Point3(32.2944, 236, 0), Vec3(25, 50, 10), Vec3(-92, 0, 0), 7)
        self.current_scene.add_rigid_box(Point3(-78.9699, 109.141, 0), Vec3(64, 21, 10), Vec3(-95, 0, 0), 8)
        self.current_scene.add_rigid_box(Point3(161.117, -92.7849, 0), Vec3(5, 49, 10), Vec3(38, 0, 0), 9)
        self.current_scene.add_rigid_box(Point3(18.7286, -137.477, 0), Vec3(83, 34, 10), Vec3(3, 0, 0), 10)
        self.current_scene.add_rigid_box(Point3(120.282, 429.443, 0), Vec3(87, 28, 10), Vec3(-185, 0, 0), 11)
        self.current_scene.add_rigid_box(Point3(136.794, -101.288, 0), Vec3(5, 50, 10), Vec3(3, 0, 0), 12)

        # 人物
        self.current_scene.add_player_role(pos,Vec3(0,0,0),HUNTER_PATH,HUNTER_ACTION_PATH)
        self.current_scene.add_enemy_role(Point3(0,10,0),3,ZOMBIE,ZOMBIE_ACTION_PATH)
        self.current_scene.add_enemy_role(Point3(20,0,0),3,HOOK_ZOMBIE,HOOK_ZOMBIE_ACTION_PATH)
        # self.current_scene.add_enemy_role(Point3(40,0,0),3,ZOMBIE,ZOMBIE_ACTION_PATH)
        # self.current_scene.add_enemy_role(Point3(80,10,0),3,HOOK_ZOMBIE,HOOK_ZOMBIE_ACTION_PATH)
        # self.current_scene.add_enemy_role(Point3(10,90,0),3,ZOMBIE,ZOMBIE_ACTION_PATH)
        # self.current_scene.add_enemy_role(Point3(100,00,0),3,HOOK_ZOMBIE,HOOK_ZOMBIE_ACTION_PATH)
        self.current_scene.cam_control(False)

        # 场景切换点
        self.ring1 = self.sceneMgr.add_model_scene(RING, self.render)
        self.ring1.setPos(-250,-50,0)
        self.ring1.setScale(3)
        self.ring2 = self.sceneMgr.add_model_scene(RING, self.render)
        self.ring2.setPos(140, -306, 0)
        self.ring2.setScale(3)
        self.sceneMgr.add_CheckCircle([(-250, -50, 0), "room"])
        self.sceneMgr.add_CheckCircle([(140, -306, 0), "home"])

        if self.sceneMgr.get_ActorMgr().get_storyLine() == 6:
            self.ring3 = self.sceneMgr.add_model_scene(RING, self.render)
            self.ring3.setPos(-225, -290, 2)
            self.ring3.setScale(3)
            self.sceneMgr.add_CheckCircle([(-225, -290, 0), "outer"])
            self.accept("change_to_scene_outer",self.change_to_outer_with_media)

        self.main_game()
        # self.show_monster_hp()
        self.current_scene.task_update()

        # 声音
        self.__rm.play_sound(1)

    def home_scene(self,pos=Point3(-30,30,0)):
        # reset
        self.sceneMgr.reset()
        self.roleMgr.reset()
        self.sceneMgr.build_on(self)

        self.ignore("mouse1")
        self.current_scene = None
        self.current_scene = SeriousGameScene(self,self.sceneMgr,self.roleMgr,self.__rm)
        self.current_scene_name = "home"
        self.accept("space", self.debug_current_scene)
        box = BoxWorld(Point3(0, -35, 0),Point3(0, 36, 0),Point3(-20, 0, 0),Point3(24, 0, 0))
        self.current_scene.load_game_scene(HOME,5.0,box)
        # 人物
        self.current_scene.add_player_role(Point3(0,0,10),Vec3(0,0,0),HUNTER_QUIET,HUNTER_QUIET_ACTION_PATH)
        self.current_scene.add_NPC_role("girl",Point3(18,-5,0),1.4,Vec3(200,0,0))

        # 场景传送点
        self.ring = self.sceneMgr.add_model_scene(RING, self.render)
        self.ring.setPos(-18, -18, 0)
        self.sceneMgr.add_CheckCircle([(-18, -18, 0), "village"])

        self.main_game()
        self.current_scene.cam_control(True,Point3(12,35,36),Vec3(0,0,0),Point3(5,0,10))
        # self.disableMouse()
        self.current_scene.task_update()

    def outer_scene(self,pos=Point3(-30,30,0)):
        # reset
        self.sceneMgr.reset()
        self.roleMgr.reset()
        self.sceneMgr.build_on(self)

        self.current_scene = None
        self.current_scene = SeriousGameScene(self, self.sceneMgr, self.roleMgr,self.__rm)
        self.current_scene_name = "outer"
        self.accept("space", self.debug_current_scene)
        box = BoxWorld(Point3(0, -400, 0),Point3(0, 390, 0),Point3(-300, 0, 0),Point3(450, 0, 0))
        self.current_scene.load_game_scene(OUTER,5,box)
        # 碰撞体
        self.current_scene.add_rigid_box(Point3(-107.136, -316.692, 9.96), Vec3(10, 10, 10), Vec3(-48, 0, 0), 1)
        self.current_scene.add_rigid_box(Point3(-296.11, 161.937, 9.96), Vec3(10, 10, 10), Vec3(-48, 0, 0), 2)
        self.current_scene.add_rigid_box(Point3(49.8745, 332.188, 9.96), Vec3(10, 10, 10), Vec3(-48, 0, 0), 3)
        self.current_scene.add_rigid_box(Point3(282.176, 315.785, 9.96), Vec3(10, 10, 10), Vec3(-48, 0, 0), 4)
        self.current_scene.add_rigid_box(Point3(252.245, 151.372, 9.96), Vec3(10, 10, 10), Vec3(-48, 0, 0), 5)
        self.current_scene.add_rigid_box(Point3(299.826, -150.148, 9.96), Vec3(10, 10, 10), Vec3(-48, 0, 0), 6)
        self.current_scene.add_rigid_box(Point3(250.284, -233.053, 9.96), Vec3(10, 10, 10), Vec3(-48, 0, 0), 7)
        self.current_scene.add_rigid_box(Point3(107.56, -311.737, 9.96), Vec3(10, 10, 10), Vec3(-48, 0, 0), 8)
        self.current_scene.add_rigid_box(Point3(-50.9728, 25.3249, 9.96), Vec3(10, 10, 10), Vec3(-48, 0, 0), 9)
        self.current_scene.add_rigid_box(Point3(154.491, 0.735287, 9.96), Vec3(10, 10, 10), Vec3(-48, 0, 0), 10)
        self.current_scene.add_rigid_box(Point3(-290.218, -257.439, 9.96), Vec3(10, 10, 10), Vec3(-48, 0, 0), 11)
        self.current_scene.add_rigid_box(Point3(-73.0873, -115.129, 9.96), Vec3(10, 10, 10), Vec3(-48, 0, 0), 12)
        # 人物
        self.current_scene.add_player_role()
        self.current_scene.add_enemy_role(Point3(50, 20, 0), 1.3, WIFE_ZOMBIE_PATH, WIFE_ZOMBIE_ACTION_PATH)
        self.current_scene.add_enemy_role(Point3(10, 160, 0), 3, HOOK_ZOMBIE,HOOK_ZOMBIE_ACTION_PATH)
        self.current_scene.add_enemy_role(Point3(40, 30, 0), 3, ZOMBIE,ZOMBIE_ACTION_PATH)
        self.current_scene.add_enemy_role(Point3(200, 110, 0), 3, HOOK_ZOMBIE,HOOK_ZOMBIE_ACTION_PATH)
        self.current_scene.add_enemy_role(Point3(120, 10, 0), 3, ZOMBIE,ZOMBIE_ACTION_PATH)
        self.current_scene.add_enemy_role(Point3(10, 120, 0), 3, HOOK_ZOMBIE,HOOK_ZOMBIE_ACTION_PATH)
        self.current_scene.add_enemy_role(Point3(10, 10, 0), 3, ZOMBIE,ZOMBIE_ACTION_PATH)

        # 场景传送点
        self.sceneMgr.add_CheckCircle([(446, -40, 0), "mountain"])
        self.ring = self.sceneMgr.add_model_scene(RING, self.render)
        self.ring.setPos(446, -40, 0)
        self.ring3.setScale(3)
        self.sceneMgr.add_CheckCircle([(446, -40, 0), "mountain"])
        self.accept("change_to_scene_mountain", self.change_to_mountain_with_media)

        self.current_scene.cam_control(False)
        self.main_game()
        self.show_monster_hp()
        self.current_scene.task_update()

    def room_scene(self,pos=Point3(-30,30,0)):
        # reset
        self.sceneMgr.reset()
        self.roleMgr.reset()
        self.sceneMgr.build_on(self)

        self.current_scene = None
        print "sceneMgr reset 结束"
        self.current_scene = SeriousGameScene(self,self.sceneMgr,self.roleMgr,self.__rm)
        self.current_scene_name = "room"
        self.accept("space", self.debug_current_scene)
        box = BoxWorld(Point3(0, -130, 0),Point3(0, 47, 0),Point3(-43, 0, 0),Point3(38, 0, 0))
        self.current_scene.load_game_scene(ROOM,5.0,box,-5)
        # 为场景建立碰撞体
        self.current_scene.add_rigid_box(Point3(-32.0762, -71.9935, 0), Vec3(10, 20, 10), Vec3(-90, 0, 0), 1)
        self.current_scene.add_rigid_box(Point3(-31.4281, -27.7879, 0), Vec3(10, 20, 10), Vec3(-90, 0, 0), 2)
        self.current_scene.add_rigid_box(Point3(-29.1829, 8.12416, 0), Vec3(10, 20, 10), Vec3(-90, 0, 0), 3)
        self.current_scene.add_rigid_box(Point3(43.4811, -18.5947, 0), Vec3(19, 15, 10), Vec3(90, 0, 0), 4)
        # 人物
        self.current_scene.add_player_role(Point3(0,0,10),Vec3(0,0,0),HUNTER_QUIET,HUNTER_QUIET_ACTION_PATH)
        self.current_scene.add_NPC_role("nun",Point3(34,22,2),3.0,Vec3(240,0,0))
        self.current_scene.add_NPC_role("stealer",Point3(-38,43,2),1.5,Vec3(100,0,0))
        # 场景传送点
        self.ring = self.sceneMgr.add_model_scene(RING, self.render)
        self.ring.setPos(5, -85, 3)
        self.sceneMgr.add_CheckCircle([(5, -85, 3), "village"])

        self.current_scene.cam_control(True, Point3(-35, -195, 65), Vec3(10, 10, 0), Point3(-10, 20, 0))
        self.disableMouse()
        self.main_game()

        print "事件重新开启"
        self.current_scene.task_update()


    # 场景切换
    def change_to_village(self):
        if(self.current_scene_name == "outer"):
            self.destory_scene(self.current_scene)
            self.village_scene()
        elif(self.current_scene_name == "home"):
            self.destory_scene(self.current_scene)
            self.village_scene()
        if(self.current_scene_name == "room"):
            self.destory_scene(self.current_scene)
            self.village_scene()

    def change_to_home(self):
        self.destory_scene(self.current_scene)
        self.home_scene()

    def change_to_room(self):
        self.destory_scene(self.current_scene)
        self.room_scene()

    def change_to_outer(self):
        self.outer_scene()

    def debug_current_scene(self):
        print "当前的场景是：",self.current_scene_name
        print self.current_scene

    def destory_scene(self,serious_scene):
        if self.current_scene != None:
            serious_scene.destroy()
        # 确定是否 destory main_game
        self.destroy_main_game()

    def change_to_outer_with_media(self):
        self.destory_scene(self.current_scene)
        self.destroy_main_game()
        self.__rm.play_media(self,2)
        self.accept("movie_over2", self.change_to_outer)

    def change_to_mountain_with_media(self):
        self.destory_scene(self.current_scene)
        self.destroy_main_game()
        self.__rm.play_media(self,3)
        self.accept("movie_over2", self.start)