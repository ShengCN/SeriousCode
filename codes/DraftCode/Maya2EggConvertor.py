
import wx

class Maya2EggConvertor(wx.Frame):

    def __init__(self, parent, title):

        wx.Frame.__init__(self,
                          parent,
                          title = title,
                          size = (400, 300))


app = wx.App(False)

frame = Maya2EggConvertor(None, "Maya2Egg Convertor")

app.MainLoop()

