# -*-coding:utf-8 -*-

#!/usr/bin/env python

# Author: Yang chenjing
# Last Updated: 2016-06-28
#
# This tutorial shows resource module interface,

from load_plot import LoadPlot
from media_player import MediaPlayer
from sound import MySound
from archives import Archives

class ResourcesManager(object):

    #初始化
    def __init__(self):

        self.__sound = MySound()

        self.__dialogueFile = LoadPlot()

        self.__media=MediaPlayer()

        self.__archive=Archives()

        self.__id=1


    """""""""""
    音乐播放函数
    """""""""""
    #播放音乐
    # id：音乐id
    def play_sound(self,id):
        self.__id=id
        self.__sound.play_music(id)

    #停止音乐
    #id：音乐id
    def stop_sound(self, id):
        self.__sound.stop_music(id)

    def set_volume(self,volume):
        self.__sound.set_volume(volume)

    def get_volume(self):
        return self.__sound.get_volume()

    # #初始化暂停设置界面控件
    # def show_volume_sliderbar(self,base):
    #     self.__sound.init_setting(base)
    #
    # #移除滑动条等有关声音的控件
    # def destroy_volume_sliderbar(self):
    #     self.__sound.destroy()

    # #开关背景音乐
    # def play_background_music(self):
    #
    #     self.__sound.toggleMusicBox()

    """""""""""
    视频函数
    """""""""""

    #播放视频文件
    #fileName:视频文件路径
    def play_media(self,base,id):
        self.__media.playMedia(base,id)
        self.stop_sound(self.__id)


    #移除视频控件
    def destroy_media(self):
        self.__media.destroy()
        self.play_sound(self.__id)

    """""""""""
    对话,提示框函数
    """""""""""

    #加载对话框，选择对话id
    #part:剧情对话id
    def show_dialog(self,part):
        self.__dialogueFile.init_interface(part)

    # 加载提示框
    def show_prompt_box(self,content):
        self.__dialogueFile.init_prompt(content)

    #读取下一句对话
    def dialog_next(self):
        #判断能否继续读下一句话，不能则返回False，结束对话
        if self.__dialogueFile.dialogue_next():
            return True
        else:
            self.__dialogueFile.destroy()
            return False

    #移除对话框等控件
    def destroy_dialog(self):
        self.__dialogueFile.destroy()

    #移除提示框控件
    def destroy_prompt(self):
        self.__dialogueFile.destroy_prompt()

    #设置剧情树路径
    def set_path(self,path):
        self.__dialogueFile.set_path(path)

    # 获取剧情树路径
    def get_path(self):
        return self.get_path()

    """""""""""
    游戏存档读档函数
    """""""""""

    # 存档界面展示存档
    def show_archives(self):
        self.__archive.show_archives()

    #存档
    #sceneArchive:场景存档
    #roleArchive:角色存档
    #id：档id，唯一标识，-1代表新的存档，0代表初始存档（开始新的游戏），>=1代表已经存在的存档
    def save_archives(self,sceneArchive,roleArchive,id,archiveName):
        if self.__archive.save_archive(sceneArchive,roleArchive,id,archiveName):
            print "存档成功"
        else:
            print "存档失败"

    #读档
    #id：档id，唯一标识，-1代表新的存档，0代表初始存档（开始新的游戏），>=1代表已经存在的存档
    def select_archives(self,id):
        if self.__archive.select_archive(id)!=False:
            print "读档成功"
            return self.__archive.select_archive(id)
        else:
            print "读档失败"

    #结束游戏,将存档内容写进文件
    def write_to_file(self):
        self.__archive.write_to_file()


