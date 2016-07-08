# -*-coding:utf-8 -*-
import sys
sys.path.append('../')

from SceneModule.scene_manager import SceneManager
from archives import Archives

archive=Archives()
archive.read_from_file()