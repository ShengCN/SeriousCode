# -*- coding:utf-8 -*-

import SeriousTools.SeriousTools as SeriousTools

class ArchivePackage(object):

    def __init__(self, arcPkgName, itemsName):

        self.__metaData = dict()
        self.__metaData["ArchivePackageName"] = arcPkgName

        self.__itemsName = itemsName
        self.__itemsData = list()

    #####################

    # 获取存档数据包名
    def get_ArchivePackageName(self):

        return self.__metaData["ArchivePackageName"]

    #####################

    # 给数据包添加元数据
    def append_metaData(self, key, value = None):

        if key not in self.__metaData.keys():

            self.__metaData[key] = value

    def set_metaData(self, key, value):

        if key is not "ArchivePackageName" and \
            key in self.__metaData.keys():

            self.__metaData[key] = value

    #####################

    def get_metaData(self, key):

        return SeriousTools.find_value_in_dict(key, self.__metaData)

    def get_all_metaData(self):

        return self.__metaData

    #####################

    def print_metaData(self):

        print "----- '%s' MetaData -----" % self.__metaData["ArchivePackageName"]

        for k, v in self.__metaData.iteritems():

            print "%s : %s" % (k, v)

        print "--------------------"

    #####################

    def get_itemsName(self):

        return self.__itemsName

    #####################

    def add_item(self, item):

        self.__itemsData.append(item)

    #####################

    def get_itemsData(self):

        return self.__itemsData

    #####################

    def print_itemsData(self):

        print "----- '%s' ItemsData -----" % self.__metaData["ArchivePackageName"]

        print "  ", self.__itemsName

        for i in range(len(self.__itemsData)):

            print (i + 1), ". ", self.__itemsData[0]

        print "--------------------"

