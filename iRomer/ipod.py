import wx
import mystr
import myserial
import time

class IpodFrame(wx.Frame):

	def __init__(self, parent, id, frame):
		self.frame			= frame

		self.TextCtrlList	= []
		self.ValueList		= []

		self.deviceVersin	= None
		self.firwareVersin	= None
		self.apMajor		= None
		self.apMinor		= None
		self.deviceId		= None
		self.errCode		= None

		wx.Frame.__init__(self, parent, id, 'Ipod test', pos=(500, 260), size=(480, 500))

		self.panel = wx.Panel(self)

		self.CreateStaticText()
		self.CreateTextCtrl()
		self.CreateButton()

	def CreateButton(self):
		for eachButton in self.ButtonData():
			index = eachButton[0]
			x, y = eachButton[1]
			w, h = eachButton[2]
			label = eachButton[3]
			button = wx.Button(self.panel, label=label, pos=(x, y), size=(w, h))

			if index == 1:
				self.Bind(wx.EVT_BUTTON, self.OnLoadIpod, button)

			if index == 2:
				self.Bind(wx.EVT_BUTTON, self.OnCloseWindow, button)

	def CreateStaticText(self):
		for eachStaticText in self.StaticTextData():
			index  = eachStaticText[0]
			label = self.GetTextLabel(index)
			if not label:
				return
			x, y = eachStaticText[1]
			w, h = eachStaticText[2]

			wx.StaticText(self.panel, -1, label, pos=(x,y), size=(w, h))

	def CreateTextCtrl(self):
		for eachTextCtrl in self.TextCtrlData():
			index  = eachTextCtrl[0]
			label = self.GetTextLabel(index)
			if not label:
				return
			x, y = eachTextCtrl[1]
			w, h = eachTextCtrl[2]

			textCtrl = wx.TextCtrl(self.panel, -1, "", pos=(x,y), size=(w, h))

			self.TextCtrlList = self.TextCtrlList + [(index, textCtrl)]

	def GetTextLabel(self, value):
		for x, y, z in self.TextData():
			if x == value:
				return y

		return None

	def SetValueList(self):
		for x, y, z in self.TextData():
			self.ValueList = self.ValueList + [(x, z)]

	def TextData(self):
		return (
				(1, "Device Version",				self.deviceVersin),
				(2, "Firware Version",				self.firwareVersin),
				(3, "Auth. Protocol Major Version",	self.apMajor),
				(4, "Auth. Protocol Minor Version",	self.apMinor),
				(5, "Device ID",					self.deviceId),
				(6, "Error Code",					self.errCode)
				)

	def StaticTextData(self):
		return	(
				(1, (50, 100), (150, 30)),
				(2, (50, 150), (150, 30)),
				(3, (50, 200), (150, 30)),
				(4, (50, 250), (150, 30)),
				(5, (50, 300), (150, 30)),
				(6, (50, 350), (150, 30)),
				)

	def TextCtrlData(self):
		return	(
				(1, (250, 100), (150, 30)),
				(2, (250, 150), (150, 30)),
				(3, (250, 200), (150, 30)),
				(4, (250, 250), (150, 30)),
				(5, (250, 300), (150, 30)),
				(6, (250, 350), (150, 30)),
				)

	def ButtonData(self):
		return	(
				(1,	(50, 50),	(350, 30),	"Load IPOD Companion ChipRegisters"),
				(2,	(50, 400),	(350, 30),	"Close")
				)

	def OnLoadIpod(self, event):
		if self.frame == None:
			return

		buf1 = "05 34 01 00"
		buf2 = " "

		recvlist =  self.frame.ProcessBuffData(buf1, buf2)
		if not recvlist:
			return None
		
		res = recvlist[6] | recvlist[7] << 8
		err = recvlist[8] | recvlist[9] << 8

		self.deviceVersin	= recvlist[10]
		self.firwareVersin	= recvlist[11]
		self.apMajor		= recvlist[12]
		self.apMinor 		= recvlist[13]
		self.deviceId 		= recvlist[14] | recvlist[15] << 8 | recvlist[16] << 16 | recvlist[17] << 24
		self.errCode 		= recvlist[18]

		self.SetValueList()

		for x, y in self.TextCtrlList:
			for a , b in self.ValueList:
				if a == x:
					y.SetValue(hex(b))

	def OnCloseWindow(self, event):
		self.Destroy()


if __name__ == '__main__':
	app = wx.App(redirect=False)
	frame = IpodFrame(parent=None, id=-1, frame=None)
	frame.Show(True)
	app.MainLoop()
