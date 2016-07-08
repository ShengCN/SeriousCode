#
# # import wx
# #
# # # create a new app, don't redirect stdout/stderr to a window
# # app = wx.App(False)
# #
# # # a frame is a top-level window
# # frame = wx.Frame(None, wx.ID_ANY, "Hello World")
# # # show the frame
# # frame.Show(True)
# #
# # app.MainLoop()
#
import wx
import os

class MyFrame(wx.Frame):

    def __init__(self, parent, title):

        wx.Frame.__init__(self,
                         parent,
                         title = title,
                         size = (200, 100))

        self.control = wx.TextCtrl(self,
                                   style = wx.TE_MULTILINE)

        self.CreateStatusBar()

        fileMenu = wx.Menu()

        menuFile = fileMenu.Append(wx.ID_OPEN,
                                   "Open File",
                                   "Open The File")

        menuAbout = fileMenu.Append(wx.ID_ABOUT,
                                    "&About",
                                    "Information about this program")

        menuExit = fileMenu.Append(wx.ID_EXIT,
                                   "&Exit",
                                   "Terminate the program")


        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")

        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OpenFile, menuFile)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

        self.Show(True)

    def OpenFile(self, event):

        self.dirname = ""

        dlg = wx.FileDialog(self,
                            "Choose a File",
                            self.dirname,
                            "",
                            "*.mb",
                            wx.OPEN)

        if dlg.ShowModal() == wx.ID_OK:

            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()

            print os.path.join(self.dirname, self.filename)


        dlg.Destroy()

    def OnAbout(self, event):

        dlg = wx.MessageDialog(self,
                               "A small text editor",
                               "About Sample Editor",
                               wx.OK)

        dlg.ShowModal()

        dlg.Destroy()

    def OnExit(self, event):

        self.Close(True)

app = wx.App(False)
frame = MyFrame(None, "Sample Editor")
app.MainLoop()

#-*- coding:utf-8 -*-
# order = "maya2egg2016"
#
# import subprocess
# import os
# import commands
#
# s = os.popen(order).read()
#
# print s
#
# p = subprocess.Popen(order, shell=True, stdout=subprocess.PIPE)
# if p is None: print "None"
# out = p.communicate()
# print out
# print "...."
