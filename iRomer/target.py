import wx

from mywx import *

class TargetFrame(wx.Frame):

    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'Target test', pos=(300, 260),
                size=(800, 480))

        self.parent = parent
        self.panel = wx.Panel(self)

        self.CreateButton()
        self.CreateTextCtrl()
        self.CreateStaticText()
        self.CreateComboBox()

        wx.StaticLine(self.panel, -1, (50, 100), (700, -1), wx.LI_HORIZONTAL)

    def CreateButton(self):
        CreateButton(self, self.ButtonData())

    def CreateStaticText(self):
        CreateStaticText(self, self.StaticTextData())

    def CreateTextCtrl(self):
        self.TextCtrlList = CreateTextCtrl(self, self.TextCtrlData())

    def CreateComboBox(self):
        list_target = []
        for a, b in self.TargetData():
            list_target = list_target + [a]

        self.ComboBoxList = CreateComboBox(self, self.ComboBoxData(), list_target)

    def OnSetBootId(self, event):
        comboBox = GetComboBoxByIndex(self.ComboBoxList, 1)

        buf1 = "02020100"
        buf2 = None

        target_buf = comboBox.GetValue()

        for a, b in self.TargetData():
            if a == target_buf:
                buf2 = b
        print "%s %s" % (target_buf, buf2)

        if not self.parent:
            return 

        recvlist = self.parent.ProcessBuffData(buf1, buf2)
        if not recvlist:
            return

        if 1 != recvlist[6]:
            print "Target receive result err"
            return

        """ end OnSetBootId """

    def OnGetBootID(self, event):
        textCtrl = GetTextCtrlByIndex(self.TextCtrlList, 2)
        comboBox = GetComboBoxByIndex(self.ComboBoxList, 1)

        buf1 = "02020200"
        buf2 = None

        target_buf = comboBox.GetValue()

        for a, b in self.TargetData():
            if a == target_buf:
                buf2 = b
        print "%s %s" % (target_buf, buf2)

        if not self.parent:
            return 

        recvlist = self.parent.ProcessBuffData(buf1, buf2)
        if not recvlist:
            return

        if 1 != recvlist[6]:
            print "Target receive result err"
            return

        bootId = recvlist[10] | recvlist[11] << 8 | \
                recvlist[12] << 16 | recvlist[13] << 24

        bootIDBuff = "Target BootID: 0x%x" % bootId
        textCtrl.SetValue(bootIDBuff)

        """ end OnGetBootID """

    def OnGetTMVersion(self, event):
        textCtrl = GetTextCtrlByIndex(self.TextCtrlList, 3)

        buf1 = "02030000"
        buf2 = ""

        if not self.parent:
            return

        recvlist = self.parent.ProcessBuffData(buf1, buf2)

        if 1 != recvlist[6]:
            print "Target receive result err"
            return

        buf = ""
        for i in range(0, recvlist[1] - 8, 1):
            buf = buf + struct.pack('B', recvlist[10 + i])

        textCtrl.SetValue(buf)

        return

    def OnGetCpuID(self, event):
        textCtrl = GetTextCtrlByIndex(self.TextCtrlList, 5)

        buf1 = "02050000"
        buf2 = ""

        if not self.parent:
            return

        recvlist = self.parent.ProcessBuffData(buf1, buf2)

        if 1 != recvlist[6]:
            print "OnGetCpuID: Target receive result err"
            return

        chip_id = recvlist[10] | recvlist[11] << 8 | \
                recvlist[12] << 16 | recvlist[13] << 24

        textCtrl.SetValue("Target Cpu ID: 0x%x" % chip_id)

        return

    def OnGetTMApp(self, event):
        textCtrl = GetTextCtrlByIndex(self.TextCtrlList, 4)

        buf1 = "02060000"
        buf2 = ""

        if not self.parent:
            return

        recvlist = self.parent.ProcessBuffData(buf1, buf2)

        if 1 != recvlist[6]:
            print "Target receive result err"
            return

        buf = ""
        for i in range(0, recvlist[1] - 9, 1):
            buf = buf + struct.pack('B', recvlist[11 + i])

        textCtrl.SetValue(buf)

        return

    def GroupBoxData(self):
        return (
                (0, (30, 10), (740, 120), "Tm-Settings"),
                (1, (30, 150), (740, 250), "Target Read"),
                )

    def ButtonData(self):
        return (
                (1, (350, 50-5), (190, 30), "Set Board", self.OnSetBootId),
                (1, (50, 190), (190, 30), "Read BootId", self.OnGetBootID),
                (1, (50, 240), (190, 30), "Read TM Version", self.OnGetTMVersion),
                (1, (50, 290), (190, 30), "Read TM APP", self.OnGetTMApp),
                (1, (50, 340), (190, 30), "Read CPU ID", self.OnGetCpuID),
               )

    def TextCtrlData(self):
        return (
                (2, (250, 190), (500, 30), "Read BootId"),
                (3, (250, 240), (500, 30), "Read TM Version"),
                (4, (250, 290), (500, 30), "Read TM APP"),
                (5, (250, 340), (500, 30), "Read CPU ID"),
               )

    def StaticTextData(self):
        return (
                (1, (50, 50), (100, 30), "Target:"),
               )

    def ComboBoxData(self):
        return (
                (1, (150, 50-5), (160, 30), "BootId"),
               )

    def TargetData(self):
        return (
                ("Auto",                    "ffff0000"),
                ("myspinup_a_sample",       "ffff0000"),
                ("csr_evb",                 "00100000"),
               )

if  __name__ == '__main__':
    app = wx.App(redirect=False)
    frame = TargetFrame(parent=None, id=-1)
    frame.Show(True)
    app.MainLoop()
