# -*-coding:utf-8 -*-

#!/usr/bin/env python

# Author: Yang chenjing
# Last Updated: 2016-06-26
#
# This tutorial shows load plot and display

from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import TransparencyAttrib
import codecs

#读取对话文件
class LoadPlot(DirectObject):
    def __init__(self):

        self.__plotFilePath="../../resources/files/dialogue.txt"

        self.__imagePath="../../resources/images/dialogue/"

        #0：对话框背景图
        #1：对话框cube
        #2：全透明图
        #3：猎人头像
        #4：修女头像
        #5：女儿头像
        #6：村民头像
        #7：小偷头像
        self.__imageList=list()
        self.__images=self.__imagePath+"npc_chat_frame.png"
        self.__imageList.append(self.__images)
        self.__images = self.__imagePath + "npc_name_cube.png"
        self.__imageList.append(self.__images)
        self.__images = self.__imagePath + "bg.jpg"
        self.__imageList.append(self.__images)
        self.__images = self.__imagePath + "HunterFace.png"
        self.__imageList.append(self.__images)
        self.__images = self.__imagePath + "NunFace.png"
        self.__imageList.append(self.__images)
        self.__images = self.__imagePath + "GirlFace.png"
        self.__imageList.append(self.__images)
        self.__images = self.__imagePath + "black.png"
        self.__imageList.append(self.__images)
        self.__images = self.__imagePath + "StealerFace.png"
        self.__imageList.append(self.__images)

        #打开对话文件
        # self.__file = open("../../resources/files/dialogue.txt", 'r')
        with open(self.__plotFilePath, 'r') as f:
            # 对话内容
            self.__content = f.readlines()

        # #对话内容
        # self.__content = self.__file.readlines()

        # 对话数组,id唯一标识
        self.__dialogueList = []

        #对话part
        self.__part = 1
        #对话第几句
        self.__index = 0

        #当前选择对话id
        self.__id=1

        #读取对话文件，存成数组
        self.dialogue_list()

        #初始化剧情树
        self.init_tree()

        #能否移除控件
        self.__destroy=False

        #能否移除提示框
        self.__destroyPrompt=False

        #剧情路径
        self.__path=""

        self.__pathTrade="18"

        # 设置对话part,默认为1
        # self.selectPart(1)


    #初始化对话与人物头像
    def init_interface(self,part):
        if self.__destroy == False :
            self.__id=part
            if self.init_dialogue(part):
                self.init_head_portrait()
                self.dialogue_next()
                self.__destroy = True
            else:
                self.__destroy=False


    # 初始化对话框
    def init_dialogue(self,part):
        # 显示对话内容
        if self.__destroy == False:
            if self.selectPart():
                print "第",part,"成功"
                self.__dialogueBackground = OnscreenImage(image=self.__imageList[0], pos=(0, 0, -0.7),
                                                          scale=(1.85, 0, 0.3))
                self.__dialogueBackground.setTransparency(TransparencyAttrib.MAlpha)
                self.__dialogueNameCube = OnscreenImage(image=self.__imageList[1], pos=(-0.7, 0, -0.58),
                                                        scale=(0.03, 0, 0.03))
                self.__dialogueNameCube.setTransparency(TransparencyAttrib.MAlpha)
                self.__dialogue = OnscreenText("", pos=(-0, -0.76), scale=0.1, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
                                               mayChange=True)
                self.__name = OnscreenText("", pos=(-0.55, -0.6), scale=0.1, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
                                           mayChange=True)
                return True
            else:
                print "第",part,"失败"
                # self.__destroy = False
                return False


    # 初始化人物头像
    def init_head_portrait(self):
        # 人物头像
        if self.__destroy == False:
            self.__image1 = OnscreenImage(image=self.__imageList[3], pos=(-1.2, 0, -0.55), scale=(0.7,0,0.45))
            self.__image1.setTransparency(TransparencyAttrib.MAlpha)
            self.__image2 = OnscreenImage(image=self.__imageList[2],pos=(1.2, 0, -0.55), scale=(0.7, 0, 0.45))
            self.__image2.setTransparency(TransparencyAttrib.MAlpha)
            # self.__destroy = True

    #初始化提示框
    def init_prompt(self,content):
        if self.__destroyPrompt==False:
            self.__promptBackground = OnscreenImage(image=self.__imageList[0], pos=(0, 0, -0.6),
                                                      scale=(0.5, 0, 0.1))
            self.__promptBackground.setTransparency(TransparencyAttrib.MAlpha)

            self.__prompt = OnscreenText(content, pos=(0, -0.63), scale=0.07, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
                                           mayChange=True)
            self.__destroyPrompt=True

    #移除控件
    def destroy(self):
        if self.__destroy == True:
            self.destroy_dialogue()
            self.destroy_image()
            self.__destroy = False

    # 移除对话框
    def destroy_dialogue(self):
        if self.__destroy == True:
            self.__dialogue.destroy()
            self.__dialogueBackground.destroy()
            self.__dialogueNameCube.destroy()
            self.__name.destroy()
            # self.__destroy = False

    #移除头像
    def destroy_image(self):
        if self.__destroy == True:
            self.__image1.destroy()
            self.__image2.destroy()
            # self.__destroy = False

    #移除提示框
    def destroy_prompt(self):
        if self.__destroyPrompt== True:
            self.__prompt.destroy()
            self.__promptBackground.destroy()
            self.__destroyPrompt = False


    #读取对话文件，存成数组，按part形成结构如下的数组
    # [{id:,dialogue:[]},{},{}]
    def dialogue_list(self):

        # 按行读取文件内容
        part = -1
        index = 0
        for line in self.__content:
            # 去掉首三个字符
            if line[:3] == codecs.BOM_UTF8:
                line = line[3:]

            #如果行中包含Part，则扩充数组
            if (line[4] == "1" or line[4] == "2" or line[4] == "3" or line[4] == "4" or line[4] == "5"
                or line[4] == "6" or line[4] == "7" or line[4] == "8"):
                part=part+1
                self.__dialogueList.append({"id":part+1,"dialogue":[]})
                index = 0
                continue

            line = line.strip('\n')

            self.__dialogueList[part]["dialogue"].append(line)
            index=index+1

    #选择第几部分对话
    def selectPart(self):
        if self.__id==7:
            self.__part = self.__id
            self.__index = 1
            return True
        else:
            self.__path = self.__path+str(self.__id)
            if self.__dialogueTree.search(self.__path,self.__id)[0] ==True:
                self.__part = self.__id
                self.__index = 1
                return True
            else:
                self.__path=self.__path[:-1]
                return False

    #读取下一句对话
    def dialogue_next(self):
        length=len(self.__dialogueList[self.__part-1]["dialogue"])
        #判断是否读到part最后一句对话
        if self.__index-1>=length:#将对应part标记，增加剧情树路径
            self.__dialogueTree.search(self.__path,self.__id)[1].set_flag(True)
            # self.__destroy()
            return False

        else:#继续显示对话与对应头像
            line=self.__dialogueList[self.__part-1]["dialogue"][self.__index-1]
            char=0

            #分离角色名与对话内容
            char = line.find(":")
            # for f in line:
            #     char = char + 1
            #     if (f == ":"):
            #         break
            role = line[:char]
            dia = line[char+1:]

            # # 判断角色
            # if role.decode('gb2312').encode('utf-8') == "猎人":
            #     self.__image.setImage("../../resources/images/1.jpg")
            # elif role.decode('gb2312').encode('utf-8') == "修女":
            #     self.__image.setImage("../../resources/images/2.jpg")
            # else:
            #     self.__image.setImage("../../resources/images/3.jpg")

            # 显示人物头像
            self.showRole(role)

            self.__dialogue.setText(dia.decode('gb2312'))

            self.__index = self.__index+1

            return True

    #根据人物对象显示头像
    def showRole(self,role):

        # 判断角色
        if role.decode('gb2312').encode('utf-8') == "猎人":
            self.__name.setText(role.decode('gb2312'))
            self.__image1.setImage(self.__imageList[3])
            self.__image1.setTransparency(TransparencyAttrib.MAlpha)
            self.__image2.setImage(self.__imageList[2])
            self.__image2.setTransparency(TransparencyAttrib.MAlpha)
        else:
            self.__image1.setImage(self.__imageList[2])
            self.__image1.setTransparency(TransparencyAttrib.MAlpha)
            self.__name.setText(role.decode('gb2312'))
            if role.decode('gb2312').encode('utf-8') == "修女":
                self.__image2.setImage(self.__imageList[4])
            elif role.decode('gb2312').encode('utf-8') == "女儿":
                self.__image2.setImage(self.__imageList[5])
            elif role.decode('gb2312').encode('utf-8') == "村民":
                self.__image2.setImage(self.__imageList[6])
            else:
                self.__image2.setImage(self.__imageList[7])
            self.__image2.setTransparency(TransparencyAttrib.MAlpha)


    #初始化剧情树
    def init_tree(self):
        #剧情树路径
        self.__path=""

        dialoguePart=[]
        for part in self.__dialogueList:
            dialoguePart.append(Node(part["id"],False))

        # print dialoguePart[1].get_data()

        index = 0
        for node in dialoguePart:
            if(index<len(dialoguePart)-2):
                node.add(dialoguePart[index+1])
                index=index+1
        # dialoguePart[0].add(dialoguePart[1])
        # dialoguePart[1].add(dialoguePart[2])
        # dialoguePart[2].add(dialoguePart[3])
        # dialoguePart[3].add(dialoguePart[4])
        # dialoguePart[4].add(dialoguePart[5])
        # dialoguePart[5].add(dialoguePart[6])
        # dialoguePart[6].add(dialoguePart[7])
        dialoguePart[0].add(dialoguePart[6])

        self.__dialogueTree = Tree()
        self.__dialogueTree.link_to_head(dialoguePart[0])

        # print 'Node', self.__dialogueTree.search("123").get_data()
        # print 'Node', self.__dialogueTree.search("1234").get_data()
        # print 'Node', self.__dialogueTree.search("19").get_data()

    #返回剧情树路径
    def get_path(self):
        return self.__path

    def set_path(self,path):
        self.__path=path
        for i in range(len(self.__path)):
            self.__id=int(self.__path[i])
            # self.__path=self.__path[:i+1]
            # self.selectPart()
            self.__dialogueTree.search(self.__path[:i+1], self.__id)[1].set_flag(True)
        if self.__destroy==True:
            self.__destroy=False

#节点类
class Node(object):
    #data：id
    #flag：是否有过标记
    def __init__(self,data,flag):
        self.__flag=flag
        self.__data=data
        self.__children=[]

    def get_data(self):
        return self.__data

    def set_data(self, data):
        self.__data = data

    def get_flag(self):
        return self.__flag

    def set_flag(self, flag):
        self.__flag = flag

    def get_children(self):
        return self.__children

    def add(self,node):
        if len(self.__children)==4:
            return False
        else:
            self.__children.append(node)

    def go(self,data,id):
        for child in self.__children:
            if child.get_data()==int(data) :
                if child.get_data()!=id and child.get_flag()==True:
                    return child
                if child.get_data()==id :
                    return child
        return None

#树类
class Tree:
    def __init__(self):
        self.__head=Node('header',False)

    def link_to_head(self,node):
        self.__head.add(node)

    def insert(self,path,data):
        cur=self.__head
        for step in path:
            if cur.go(step)==None:
                return False
            else:
                cur=cur.go(step)
        cur.add(Node(data))
        return True

    def search(self,path,id):
        cur = self.__head
        for step in path:
            if cur.go(step,id) == None:
                return [False , None]
            else:
                cur = cur.go(step,id)
        return [True , cur]





