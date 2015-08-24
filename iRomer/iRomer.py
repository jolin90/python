#!/usr/bin/python

import sys
import wx
import graphic
import ipod
import pmic
import mystr
import myserial
import tp
import target
import option

from myserial import *
from mywx import *


class MySendData():
    def __init__(self, buf1, buf2):
        " head | cmd | data | check_sum "

        self.buf1 = buf1.strip(" ").replace(" ", "")
        self.buf2 = buf2.strip(" ").replace(" ", "")

        self.list_header = [0x3b, 0x0]
        self.list_cmd = [0,0,0,0]
        self.list_payload = []
        self.list_check_sum = [0]

        self.set_list_cmd()
        self.set_list_payload()
        self.set_list_header()
        self.set_list_check_sum()

    def set_list_cmd(self):
        buf = self.buf1

        for i in range(4):
            if not buf[0:2]:
                break
            if len(buf) < 2:
                break
            self.list_cmd[i] = int(buf[0:2], 16)
            buf = buf[2:]
        "done"
        return 

    def set_list_payload(self):
        buf = self.buf2

        if not buf:
            return
        if len(buf) < 2:
            return

        buf_t = ""
        for i in range(len(buf)/2):
            buf_t = buf_t + ("%s " % buf[0:2])
            buf   = buf[2:]

        self.list_payload = buf_t.strip(" ").split(" ")

        for i in range(len(self.list_payload)):
            self.list_payload[i] = int(self.list_payload[i], 16)
        return

    def set_list_header(self):
        self.list_header[1] = len(self.list_cmd) + len(self.list_payload)

    def set_list_check_sum(self):
        self.list_check_sum[0] = checksum(self.list_header + self.list_cmd + \
                self.list_payload)

    def get_list_cmd(self):
        return self.list_cmd

    def get_list_payload(self):
        return self.list_payload

    def get_list_all(self):
        return self.list_header + self.list_cmd + \
                self.list_payload + self.list_check_sum


class MainFrame(wx.Frame):
    def __init__(self, parent, id):
        self.serial = None

        wx.Frame.__init__(self, parent, id, 'iRomer for testmanager',
                pos=(400, 100), size=(700, 600))

        self.panel = wx.Panel(self)

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.createMenuBar()

        ButtonListdata = (
                            (1, (50, 20), (80, 30), "send", self.OnSend2),
                            (2, (50, 60), (80, 30), "Receive", self.OnReceive2),
                         )
        CreateButton(self, ButtonListdata)

        TextCtrlListData = (
                            (1, (150, 20), (100, 30), ""),
                            (2, (280, 20), (350, 30), ""),
                            (3, (150, 60), (480, 30), ""),
                           )
        self.TextCtrlList = CreateTextCtrl(self, TextCtrlListData)

    def set_text_ctrl(self, textCtrl, lists):

        if not lists:
            return

        buf = ""
        for i in lists:
            buf_hex = "%s" % hex(i)[2:]
            if len(buf_hex) < 2:
                buf_hex = "0"+ buf_hex
            buf = buf + ("%s  " % buf_hex)

        textCtrl.SetValue(buf)

    def set_send_list(self, buf1, buf2):
        text1 = GetTextCtrlByIndex(self.TextCtrlList, 1);
        text2 = GetTextCtrlByIndex(self.TextCtrlList, 2);

        data = MySendData(buf1, buf2)

        self.set_text_ctrl(text1, data.get_list_cmd())
        self.set_text_ctrl(text2, data.get_list_payload())
        
        return data.get_list_all()

    def process_send(self):
        "get TextCtrl data and send"
        text1 = GetTextCtrlByIndex(self.TextCtrlList, 1);
        text2 = GetTextCtrlByIndex(self.TextCtrlList, 2);

        buf1 = text1.GetValue()
        buf2 = text2.GetValue()

        send_list = self.set_send_list(buf1, buf2)

        print "Send\t: ",
        self.PrintList(send_list)

        if not self.serial:
            return None

        self.serial.write(send_list)

    def process_read(self):
        text3 = GetTextCtrlByIndex(self.TextCtrlList, 3);

        if not self.serial:
            return None

        recvlist = self.serial.read()

        if type(recvlist) == type(1):
            print "ProcessData err code : %d" % recvlist
            text3.SetValue("")
            return None

        self.set_text_ctrl(text3, recvlist)

        print "Recv\t: ",
        self.PrintList(recvlist)

        if check_sum(recvlist):
            return recvlist
        else:
            print "ProcessData : check_sum err"

        return None

    def ProcessBuffData(self, buf1, buf2):
        text1 = GetTextCtrlByIndex(self.TextCtrlList, 1);
        text2 = GetTextCtrlByIndex(self.TextCtrlList, 2);

        if not buf1:
            print "ProcessBuffData : buf1 is None"
            return

        if not buf2:
            print "ProcessBuffData : buf2 is None"
            return

        text1.SetValue(buf1)
        text2.SetValue(buf2)

        self.process_send()
        self.process_read()

    def OnSend2(self, event):
        "send data to uart"
        self.process_send()
        self.process_read()
        "end"

    def OnReceive2(self, event):
        "send data to uart"
        self.process_send()
        self.process_read()
        "end"
   
    def PrintList(self, List):
        for i in List:
            print "%2x " % i,
        print

    def createMenuBar(self):
        menuBar = wx.MenuBar()
        for eachMenuData in self.menuData():
            menuLabel = eachMenuData[0]
            menuItems = eachMenuData[1:]
            menuBar.Append(self.createMenu(menuItems), menuLabel)
        self.SetMenuBar(menuBar)

    def createMenu(self, menuData):
        menu = wx.Menu()
        for eachLabel, eachStatus, eachHandler in menuData:
            if not eachLabel:
                menu.AppendSeparator()
                continue
            menuItem = menu.Append(-1, eachLabel, eachStatus)
            self.Bind(wx.EVT_MENU, eachHandler, menuItem)
        return menu

    def OnGraphic(self, event):
        self.graphic = graphic.GraphicFrame(parent=None, id=-1, frame=self)
        self.graphic.Show()

    def OnIpod(self, event):
        self.ipod = ipod.IpodFrame(parent=None, id=-1, frame=self)
        self.ipod.Show()

    def OnPmic(self, event):
        pmic.PmicFrame(parent=None, id=-1, frame=self).Show()

    def OnTP(self, event):
        tp.TPFrame(parent=None, id=-1, frame=self).Show()

    def OnTarget(self, event):
        target.TargetFrame(parent=self, id=-1).Show()
 
    def OnOptions(self, event):
        op = option.OptionFrame(parent=self, id=-1).Show()

    def OnCloseWindow(self, event):
        self.Destroy()

    def menuData(self):
        return (
                ("&Extras",
                    ("Options", "Options", self.OnOptions),
                    ("&Dbug", "Dbug", None),
                    ("&Quit", "Quit", self.OnCloseWindow)
                ),
                ("&CPU",
                    ("Target", "Target", self.OnTarget),
                    ("Gpio", "Gpio", None),
                    ("USBH", "USBH", None),
                    ("Graphic", "Graphic", self.OnGraphic),
                    ("Internal RTC", "Internal RTC", None),
                    ("I2C", "I2C", None),
                    ("I2S", "I2S", None)
                ),
                ("&Peripherals",
                    ("Bluetooth", "Bluetooth", None),
                    ("eMMC", "eMMC", None),
                    ("IPOD", "IPOD", self.OnIpod),
                    ("PMIC", "PMIC", self.OnPmic),
                    ("TP", "TP", self.OnTP),
                    ("ADR", "ADR", None),
                    ("MOST", "MOST", None)
                )
               )

if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame(parent=None, id=-1)
    frame.Show(True)
    app.MainLoop()
