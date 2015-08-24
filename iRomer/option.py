import wx
import mystr
import myserial
import time
import struct

from mystr import hex2
from mywx import *
from myserial import *

class OptionFrame(wx.Frame):

    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'Options', pos=(300, 260),
                size=(400, 300))

        self.parent = parent

        self.panel = wx.Panel(self)
        
        opStText   = ((0, (50, 50), (150, 30), "Command port:"),)
        opButton   = ((1, (50, 100), (150, 30), "Set", self.OnSetting),)
        opComboBox = ((1, (200, 50), (150, 30), "getports"),)

        CreateStaticText(self, opStText)
        CreateButton(self, opButton)
        self.CoList = CreateComboBox(self, opComboBox, getports())

    def OnSetting(self, event):
        "start Onsetting"
        if not self.parent:
            return

        combobox = GetComboBoxByLabel(self.CoList, "getports")
        port = combobox.GetValue()
        if self.parent.serial:
            self.parent.serial.close()
            time.sleep(1)
        self.parent.serial = MySerial(port, 115200, 1)

        self.Destroy()

        "end OnSetting"

if  __name__ == '__main__':
    app = wx.App(redirect=False)
    frame = OptionFrame(parent=None, id=-1)
    frame.Show(True)
    app.MainLoop()
