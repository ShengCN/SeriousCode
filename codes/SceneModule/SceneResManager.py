# # -*- coding:utf-8 -*-
#
# # Author : 戴熹
#
# # Last Updated : 2016-06-20
#
# # Description : 场景管理器，用来管理各种场景资源
#
# <<<<<<< .mine
# # from direct.showbase.Loader import Loader
# # from direct.actor.Actor import Actor
# # from direct.interval.ActorInterval import ActorInterval
# # from panda3d.core import GeoMipTerrain
# #
# # from SeriousTools import SeriousTools
# #
# # import string
# ||||||| .r100
# from direct.showbase.Loader import Loader
# from direct.actor.Actor import Actor
# from panda3d.core import GeoMipTerrain
# =======
# from direct.showbase.Loader import Loader
# from direct.actor.Actor import Actor
# from direct.interval.ActorInterval import ActorInterval
# from panda3d.core import GeoMipTerrain
# >>>>>>> .r105
#
# # class SceneResManager(object):
# #
# #     def __init__(self):
# #
# #         self.__loader = Loader(self)
# #
# #         self.__resType = ["model",    # 模型，一般没有动作
# #                           "actor",    # 人物模型，一般带有动作
# #                           "terrain"]  # 地形资源
# #
# #         self.__modelMap = dict()
# #         self.__actorMap = dict()
# #         self.__terraMap = dict()
# #
# #         self.__itvlMap = dict()
# #
# #         self.__modelCount = 0
# #         self.__actorCount = 0
# #         self.__terraCount = 0
# #
# #         self.__sceneResMap = [self.__modelMap,
# #                               self.__actorMap,
# #                               self.__terraMap]
# #
# #     def load_res(self,
# #                  resPath,
# #                  extraResPath = None
# #                  ):
# #
# #         res = None
# #         resId = ""
# #
# #         # 资源类型
# #         resType = SeriousTools.get_filepath_suffix(resPath).lower()
# #
# #         if extraResPath is None:
# #
# #             res = self.__loader.loadModel(resPath)
# #
# #             self.__modelCount += 1
# #             resId = self.__resType[0] + str(self.__modelCount)
# #
# #             self.__sceneResMap[0][resId] = res
# #
# #         else:
# #
# #             # 加载角色资源
# #             if isinstance(extraResPath, dict):
# #
# #                 res = Actor(resPath, extraResPath)
# #
# #                 self.__actorCount += 1
# #                 resId = self.__resType[1] + str(self.__actorCount)
# #
# #                 self.__sceneResMap[1][resId] = res
# #
# #                 self.__itvlMap[resId] = self.__gen_interval_for_actor(res)
# #
# #             # 加载地形资源
# #             else:
# #
# #                 if extraResPath is None:
# #                     return None
# #
# #                 self.__terraCount += 1
# #                 resId = self.__resType[2] + str(self.__terraCount)
# #
# #                 res = GeoMipTerrain(resId)
# #
# #                 res.setHeightfield(resPath)
# #                 res.setColorMap(extraResPath)
# #
# #                 self.__sceneResMap[2][resId] = res
# #
# #         return res
# #
# #     def __gen_interval_for_actor(self, actor):
# #
# #         itvlList = []
# #
# #         for actionName in actor.getAnimNames().keys():
# #             tmpItvl = ActorInterval(actor=actor,
# #                                     animName=actionName)
# #
# #             itvlList.append(tmpItvl)
# #
# #         return itvlList
# #
# #     # 获取资源ID
# #     def get_resId(self, res):
# #
# #         for resmap in self.__sceneResMap:
# #             for resId, _res in resmap.iteritems():
# #                 if _res == res:
# #                     return resId
# #
# #         return None
# #
# #     # 获取资源
# #     def get_res(self, resId):
# #
# #         typeIdx = -1
# #         resIdx = -1
# #
# #         if isinstance(resId, str) is False:
# #             return None
# #
# #         for rtl in self.__resType:
# #             typeIdx += 1
# #             if resId.startWith(rtl):
# #                 resIdx = string.atoi(resId[len(rtl):])
# #                 return self.__sceneResMap[typeIdx][resIdx]
# #
# #         return None
# #
# #     def print_resMap(self):
# #         print "-- Resource Map -- "
# #         for i in range(len(self.__resType)):
# #             print "%s. %s" % (i+1, self.__resType[i])
# #             for resId, res in self.__sceneResMap[i].iteritems():
# #                 print "    %s : %s" % (resId, res)
# #         print "--------------------"
# #
# #     # 释放资源
# #     def free_res(self, resId):
# #         pass
#
# from ActorManager import ActorManager
# from ModelManager import ModelManager
# from TerrainManager import TerrainManager
#
# ImageType = [ "jpg", "png", "bmp" ]
#
# class SceneManager(object):
#
#     def __init__(self):
#
#         self.__actorMgr = ActorManager()
#         self.__modelMgr = ModelManager()
#         self.__terraMgr = TerrainManager()
#
#     #########################################
#
#     def load_res(self, resPath, extraResPath):
#         pass
#
# <<<<<<< .mine
# ||||||| .r100
#         self.__modelCount = 0
#         self.__actorCount = 0
#         self.__terraCount = 0
# =======
#         self.__itvlMap = dict()
#
#         self.__modelCount = 0
#         self.__actorCount = 0
#         self.__terraCount = 0
# >>>>>>> .r105
#
#     #########################################
#
#
#
# <<<<<<< .mine
# ||||||| .r100
#         # 资源类型
#         resType = SeriousTools.get_filepath_suffix(resPath).lower()
#
#         if extraResPath is None:
#
#             res = self.__loader.loadModel(resPath)
#
#             self.__modelCount += 1
#             resId = self.__resType[0] + str(self.__modelCount)
#
#             self.__sceneResMap[0][resId] = res
#
#         else:
#
#             # 加载角色资源
#             if isinstance(extraResPath, dict):
#
#                 res = Actor(resPath, extraResPath)
#
#                 self.__actorCount += 1
#                 resId = self.__resType[1] + str(self.__actorCount)
#
#                 self.__sceneResMap[1][resId] = res
#
#             # 加载地形资源
#             else:
#
#                 if extraResPath is None:
#                     return None
#
#                 self.__terraCount += 1
#                 resId = self.__resType[2] + str(self.__terraCount)
#
#                 res = GeoMipTerrain(resId)
#
#                 res.setHeightfield(resPath)
#                 res.setColorMap(extraResPath)
#
#                 self.__sceneResMap[2][resId] = res
#
#
#
#         return res
#
#     # 获取资源ID
#     def get_resId(self, res):
#
#         for resmap in self.__sceneResMap:
#             for resId, _res in resmap.iteritems():
#                 if _res == res:
#                     return resId
#
#         return None
#
#     # 获取资源
#     def get_res(self, resId):
#
#         typeIdx = -1
#         resIdx = -1
#
#         if isinstance(resId, str) is False:
#             return None
#
#         for rtl in self.__resType:
#             typeIdx += 1
#             if resId.startWith(rtl):
#                 resIdx = string.atoi(resId[len(rtl):])
#                 return self.__sceneResMap[typeIdx][resIdx]
#
#         return None
#
#     def print_resMap(self):
#         print "-- Resource Map -- "
#         for i in range(len(self.__resType)):
#             print "%s. %s" % (i+1, self.__resType[i])
#             for resId, res in self.__sceneResMap[i].iteritems():
#                 print "    %s : %s" % (resId, res)
#         print "--------------------"
#
#     # 释放资源
#     def free_res(self, resId):
#         pass
#
# =======
#         # 资源类型
#         resType = SeriousTools.get_filepath_suffix(resPath).lower()
#
#         if extraResPath is None:
#
#             res = self.__loader.loadModel(resPath)
#
#             self.__modelCount += 1
#             resId = self.__resType[0] + str(self.__modelCount)
#
#             self.__sceneResMap[0][resId] = res
#
#         else:
#
#             # 加载角色资源
#             if isinstance(extraResPath, dict):
#
#                 res = Actor(resPath, extraResPath)
#
#                 self.__actorCount += 1
#                 resId = self.__resType[1] + str(self.__actorCount)
#
#                 self.__sceneResMap[1][resId] = res
#
#                 self.__itvlMap[resId] = self.__gen_interval_for_actor(res)
#
#             # 加载地形资源
#             else:
#
#                 if extraResPath is None:
#                     return None
#
#                 self.__terraCount += 1
#                 resId = self.__resType[2] + str(self.__terraCount)
#
#                 res = GeoMipTerrain(resId)
#
#                 res.setHeightfield(resPath)
#                 res.setColorMap(extraResPath)
#
#                 self.__sceneResMap[2][resId] = res
#
#         return res
#
#     def __gen_interval_for_actor(self, actor):
#
#         itvlList = []
#
#         for actionName in actor.getAnimNames():
#             tmpItvl = ActorInterval(actor=actor,
#                                     animName=actionName)
#
#             itvlList.append(tmpItvl)
#
#         return itvlList
#
#     # 获取资源ID
#     def get_resId(self, res):
#
#         for resmap in self.__sceneResMap:
#             for resId, _res in resmap.iteritems():
#                 if _res == res:
#                     return resId
#
#         return None
#
#     # 获取资源
#     def get_res(self, resId):
#
#         typeIdx = -1
#         resIdx = -1
#
#         if isinstance(resId, str) is False:
#             return None
#
#         for rtl in self.__resType:
#             typeIdx += 1
#             if resId.startWith(rtl):
#                 resIdx = string.atoi(resId[len(rtl):])
#                 return self.__sceneResMap[typeIdx][resIdx]
#
#         return None
#
#     def print_resMap(self):
#         print "-- Resource Map -- "
#         for i in range(len(self.__resType)):
#             print "%s. %s" % (i+1, self.__resType[i])
#             for resId, res in self.__sceneResMap[i].iteritems():
#                 print "    %s : %s" % (resId, res)
#         print "--------------------"
#
#     # 释放资源
#     def free_res(self, resId):
#         pass
#
# >>>>>>> .r105
