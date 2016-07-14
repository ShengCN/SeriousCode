# -*-coding:utf-8 -*-

#!/usr/bin/env python

# Author: Yang chenjing
# Last Updated: 2016-06-28
#
# This tutorial save or select archives

import sys
sys.path.append('../')

from ArchiveModule.archive_package import ArchivePackage

import json
import time

class Archives(object):
    def __init__(self):
        self.__archiveFilePath="../../resources/files/archives.txt"#存档文件路径
        self.__initArchiveFilePath="../../resources/files/initArchive.txt"

        self.__archives=list()#存档内容。数组多条

        self.__showArchives=list()#存档界面展示内容

        self.__loadRoleArchive=dict()#需要加载的角色存档
        self.__loadPath=""#需要加载的剧情路径

        self.read_from_file()
        # self.init_archive()

    #读初始存档
    def init_archive(self):
        with open(self.__initArchiveFilePath, 'r') as f:
            self.__initArchives = json.loads(f.read())
            self.__initArchives = self.byteify(self.__initArchives)

    #存档界面展示存档
    def show_archives(self):
        self.__showArchives=list()
        for i in range(len(self.__archives)):
            self.__showArchives.append(dict())
            self.__showArchives[i]["id"]=self.__archives[i]["id"]
            self.__showArchives[i]["name"] = self.__archives[i]["name"]
            self.__showArchives[i]["time"] = self.__archives[i]["time"]
            # self.__showArchives[i]["progress"] = "50%"
            self.__showArchives[i]["progress"] = self.__archives[i]["progress"]

        return self.__showArchives

    #存档
    def save_archive(self,roleArchive,id,path):
        #新存档
        if id==-1 :
            id = len(self.__archives)+1
            self.new_archive(roleArchive,id,path)
            self.__archives.append(self.__archive)
            return True
        #覆盖之前的存档
        else:
            for i in range(len(self.__archives)):
                if (self.__archives[i]["id"] == id):
                    self.new_archive(roleArchive,id,path)
                    self.__archives[i]=self.__archive
                    return True
        return False

        # self.write_to_file()

    #新建存档
    def new_archive(self,roleArchive,id,path):

        # 一条存档
        self.__archive = dict()
        self.__archive["id"] = id
        self.__archive["time"] = time.strftime('%Y/%m/%d %H:%M', time.localtime(time.time()))
        self.__archive["name"] = "Archive" + str(id)
        #path/10
        self.__archive["progress"]=str(len(path)*100/7)+"%"
        self.__archive["path"] = path
        self.__archive["content"] = roleArchive

        self.write_to_file()

    #选择存档
    def select_archive(self,id):
        flag=False
        if id == 0 :#开始新的游戏，读取初始档
            flag = True
            self.init_archive()
            self.__loadRoleArchive = self.__initArchives["content"]
            self.__loadPath = self.__initArchives["path"]

        else:
            for i in range(len(self.__archives)):
                if(self.__archives[i]["id"]==id):
                    flag=True
                    print self.__archives[i]["id"]
                    self.__loadRoleArchive = self.__archives[i]["content"]
                    self.__loadPath = self.__archives[i]["path"]
                    break

        if flag==False:
            return False
        else:
            # self.read_archive()
            return [self.__loadRoleArchive,self.__loadPath]

    #将所有unicode转为string
    def byteify(self,input):
        if isinstance(input, dict):
            return {self.byteify(key): self.byteify(value) for key, value in input.iteritems()}
        elif isinstance(input, list):
            return [self.byteify(element) for element in input]
        elif isinstance(input, unicode):
            return input.encode('utf-8')
        else:
            return input

    #将存档记录写入文件
    def write_to_file(self):
        encodedjson = json.dumps(self.__archives, indent=4)
        with open(self.__archiveFilePath, 'w') as f:
            f.write(encodedjson)

        # f = open("../../resources/files/archives.txt", "w")
        # f.write(encodedjson)
        # f.close()

    #从文件中读取存档记录
    def read_from_file(self):
        with open(self.__archiveFilePath , 'r') as f:
            self.__archives=json.loads(f.read())
            self.__archives = self.byteify(self.__archives)

    def get_id(self):
        pass