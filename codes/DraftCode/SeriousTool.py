# -*- coding:utf-8 -*-

import wx
import os
import subprocess
import Image
from panda3d.core import Filename

versions = [
    "2015",
    "2016",
    "2014",
    "2013",
    "2012"
]

types = [
    "model",
    "chan",
    "both"
]

class Maya2EggConvertor(wx.Frame):

    def __init__(self, parent, title):

        wx.Frame.__init__(self,
                          parent,
                          title = title,
                          size = (480, 600))

        self.version = "2015"
        self.type = "model"
        self.mbFile = ""
        self.eggFile = ""

        self.cmd = ""

        self.dirname = ""

        self.execResult = None
        self.resultFile = None

        self.versionList = wx.ListBox(parent = self,
                                      size = (160, 40))
        for i in range(len(versions)):

            self.versionList.Insert(versions[i], pos = i)
        self.versionList.Select(0)

        self.typeList = wx.ListBox(parent = self,
                                   size = (160, 40))
        for i in range(len(types)):

            self.typeList.Insert(types[i], pos = i)
        self.typeList.Select(0)

        self.button = wx.Button(parent = self,
                                label = "Open mb File",
                                size = (160, 40))

        self.button2 = wx.Button(parent = self,
                                label = "Convert jpg/tga to png",
                                size = (480, 40))

        self.button3 = wx.Button(parent = self,
                                 label = "Replace .jpg/.tga/.rgb in egg with .png",
                                 size = (480, 40))

        self.control = wx.TextCtrl(self,
                                   style = wx.TE_MULTILINE,
                                   size = (480, 480))

        self.box = wx.BoxSizer(wx.VERTICAL)

        self.box1 = wx.BoxSizer(wx.HORIZONTAL)
        self.box1.Add(self.versionList)
        self.box1.Add(self.typeList)
        self.box1.Add(self.button)

        self.box2 = wx.BoxSizer(wx.VERTICAL)
        self.box2.Add(self.control)

        self.box3 = wx.BoxSizer(wx.VERTICAL)
        self.box3.Add(self.button2)
        self.box3.Add(self.button3)

        self.box.Add(self.box1)
        self.box.Add(self.box3)
        self.box.Add(self.box2)

        self.Bind(wx.EVT_BUTTON, self.convert_mb_file, self.button)
        self.Bind(wx.EVT_BUTTON, self.convert_to_png_file, self.button2)
        self.Bind(wx.EVT_BUTTON, self.convert_to_png_format, self.button3)

        self.SetAutoLayout(True)
        self.SetSizer(self.box)
        self.Layout()
        self.Show(True)

    def convert_to_png_format(self, event):

        fileDlg = wx.FileDialog(self,
                                "choose a egg file, which its textures is in jpg/tga/rgb format",
                                self.dirname,
                                "",
                                "*.egg",
                                wx.OPEN | wx.MULTIPLE)

        if fileDlg.ShowModal() == wx.ID_OK:

            paths = fileDlg.GetPaths()

            self.control.AppendText("##############################\n")
            self.control.AppendText("Transform the textures file format in egg:\n")

            for path in paths:

                png = ""

                eggToRead = open(path, "r")

                lines = eggToRead.readlines()
                _lines = []
                for i in range(len(lines)):

                    line = lines[i]

                    line = line.replace(".jpg", ".png")
                    line = line.replace(".tga", ".png")
                    line = line.replace(".rgb", ".png")

                    _lines.append(line)

                eggToRead.close()

                eggToWrite = open(path, "w")

                eggToWrite.writelines(_lines)

                eggToWrite.close()

                self.control.AppendText(path + "\n")

            self.control.AppendText("####### Transform End #############\n")

    def convert_to_png_file(self, event):

        fileDlg = wx.FileDialog(self,
                                "choose jpg/tga File",
                                self.dirname,
                                "",
                                "*.jpg;*.tga",
                                wx.OPEN | wx.MULTIPLE)

        if fileDlg.ShowModal() == wx.ID_OK:

            paths = fileDlg.GetPaths()

            for path in paths:

                image = Image.open(path)

                png = path[:(len(path)-4)] + ".png"

                image.save(png)

            self.control.AppendText("##############################\n")
            self.control.AppendText("Convert the files:\n")
            for path in paths:
                self.control.AppendText(path + "\n")
            self.control.AppendText("from jpg/tga to png\n")
            self.control.AppendText("####### Convert End #############\n")

    def convert_mb_file(self, event):

        fileDlg = wx.FileDialog(self,
                                "choose a mb File",
                                self.dirname,
                                "",
                                "*.mb",
                                wx.OPEN | wx.MULTIPLE)

        if fileDlg.ShowModal() == wx.ID_OK:

            #self.dirname = fileDlg.GetDirectory()

            paths = fileDlg.GetPaths()

            for path in paths:

                self.mbFile = path
                self.eggFile = self.mbFile[:(len(self.mbFile)-2)] + "egg"

                self.mbFile = os.path.join(self.dirname, self.mbFile)
                self.eggFile = os.path.join(self.dirname, self.eggFile)

                self.mbFile = Filename.fromOsSpecific(self.mbFile)
                self.eggFile = Filename.fromOsSpecific(self.eggFile)

                self.version = self.versionList.GetStringSelection()
                self.type = self.typeList.GetStringSelection()

                self.fill_cmd()

                self.control.AppendText("##############################\n")
                self.control.AppendText("Executing cmd : \n")
                self.control.AppendText(self.cmd + "\n")
                self.control.AppendText("########## Please Wait ##########\n")

                self.control.AppendText("If you can't find the egg file...check your file path and your maya version\n")
                self.control.AppendText("It's not available if the file path includes Chinese ( : 3 )\n")

                self.exec_cmd()

            self.control.AppendText("OK!! Convert Successfull ( ^ _ ^ )> ")

    def fill_cmd(self):

        #self.resultFile = os.path.join(self.dirname, "result2.txt")

        self.cmd = "maya2egg%s -a %s -o %s %s > %s" % (self.version, self.type, self.eggFile, self.mbFile, self.resultFile)

    def exec_cmd(self):

        self.execResult = subprocess.Popen(self.cmd,
                                           shell = True,
                                           stdout = subprocess.PIPE)



app = wx.App(False)

frame = Maya2EggConvertor(None, "SeriousTool")

app.MainLoop()

