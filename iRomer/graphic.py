import wx
import mystr
import myserial
import time

from mystr import hex2

class GraphicFrame(wx.Frame):
	def __init__(self, parent, id, frame):
		self.frame = frame
		self.button = []
		self.StaticText = []
		self.ComboBox = []

		self.cmdlist = [0x07, 0x1, 0, 0]

		self.Cmd2List = []
		self.VideoOutInPatternList = []
		self.VideoInExtPatternList = []
		self.VideoInStatusList = []

		self.getCmd2List()
		self.getVideoOutInPatternList()
		self.getVideoInExtPatternList()
		self.getVideoInStatusPatternList()

		wx.Frame.__init__(self, parent, id, 'Graphic test',
				pos=(500, 260), size=(480, 400))

		self.panel = wx.Panel(self, -1) 

		self.CreateStaticText()
		self.CreateButton()
		self.CreateComboBox()
		self.CreateRadioBox()

	def DisbaleAll(self):
		for eachStaticText in self.StaticText:
			label = eachStaticText[0]
			text = eachStaticText[1]
			if label != "Cmd2:":
				text.Show(False)
		
		for eachCombobox in self.ComboBox:
			label = eachCombobox[0]
			comboBox = eachCombobox[1]
			if label != "Cmd2ComboBox":
				comboBox.Show(False)

		self.RadioBox.Show(False)
	
	def OnCmd(self, event):
		self.DisbaleAll()

		select = ""
		for eachCombobox in self.ComboBox:
			label = eachCombobox[0]
			comboBox = eachCombobox[1]
			if label == "Cmd2ComboBox":
				select = comboBox.GetValue()

		if select:
			for x, y in self.Cmd2Data():
				if x == select:
					if y == 2:
						for eachStaticText in self.StaticText:
							label = eachStaticText[0]
							text = eachStaticText[1]
							if label == "Pattern":
								text.Show(True)
								break

						for eachCombobox in self.ComboBox:
							label = eachCombobox[0]
							comboBox = eachCombobox[1]
							if label == "PatternComboBox":
								comboBox.Show(True)
								break

					if y == 5:
						for eachStaticText in self.StaticText:
							label = eachStaticText[0]
							text = eachStaticText[1]
							if label == "Pattern":
								text.Show(True)
								break

						for eachCombobox in self.ComboBox:
							label = eachCombobox[0]
							comboBox = eachCombobox[1]
							if label == "VideoInExtPattern":
								comboBox.Show(True)
								break

					if y == 6:
						for eachStaticText in self.StaticText:
							label = eachStaticText[0]
							text = eachStaticText[1]
							if label == "Status":
								text.Show(True)
								break

						for eachCombobox in self.ComboBox:
							label = eachCombobox[0]
							comboBox = eachCombobox[1]
							if label == "VideoInStatus":
								comboBox.Show(True)
								break

						self.RadioBox.Show(True)


	def getVideoOutInPatternList(self):
		for x, y in self.VideoOutInPatternData():
			self.VideoOutInPatternList = self.VideoOutInPatternList + [x]

	def getVideoInExtPatternList(self):
		for x, y in self.VideoInExtPatternData():
			self.VideoInExtPatternList = self.VideoInExtPatternList + [y]

	def getVideoInStatusPatternList(self):
		for x, y in self.VideoInStatusData():
			self.VideoInStatusList = self.VideoInStatusList + [y]

	def getCmd2List(self):
		for x, y in self.Cmd2Data():
			self.Cmd2List = self.Cmd2List + [x]

	def VideoOutSetup(self):
		self.cmdlist[2] = 0x01
		self.cmdlist[3] = 0x01

	def VideoOutIn(self):
		patternbuf = self.PatternComboBox.GetValue()

		self.cmdlist[3] = 0x0

		for x, y in self.VideoOutInPatternData():
			if x == patternbuf:
				self.cmdlist[2] = y

	def VideoInExt(self):
		patternbuf = self.VideoInExtPatternComboBox.GetValue()
		self.cmdlist[3] = 0x0

		for x, y in self.VideoInExtPatternData():
			if y == patternbuf:
				self.cmdlist[2] = x

	def VideoInStatus(self):

		patternbuf = self.VideoInStatusComboBox.GetValue()
		self.cmdlist[3] = 0x0

		for x, y in self.VideoInStatusData():
			if y == patternbuf:
				self.cmdlist[2] = x

	def OnSend(self, event):
		buf1 = "  "
		buf2 = "00"

		self.cmdlist[0] = 0x07

		cmd2buf = self.Cmd2ComboBox.GetValue()

		for x, y in self.Cmd2Data():
			if x == cmd2buf:

				self.cmdlist[1] = y

				if y == 0x01:
					self.VideoOutSetup()
				if y == 0x02:
					self.VideoOutIn()
				if y == 0x03:
					self.cmdlist[2] = 0x0
					self.cmdlist[3] = 0x0
				if y == 0x04:
					self.cmdlist[2] = 0x0
					self.cmdlist[3] = 0x0
				if y == 0x05:
					self.VideoInExt()
				if y == 0x06:
					self.VideoInStatus()

		for i in self.cmdlist:
			buf1 = buf1 + "%s " % hex2(i)

		if self.frame == None:
			return

		recvlist =  self.frame.ProcessBuffData(buf1, buf2)
		if not recvlist:
			return None

	def CreateButton(self):
		for eachButton in self.ButtonData():
			label = eachButton[0]
			x, y = eachButton[1]
			w, h = eachButton[2]
			button = wx.Button(self.panel, label=label, pos=(x, y),
					size=(w, h))
			button.Show(True)

			if label == "Send":
				self.Bind(wx.EVT_BUTTON, self.OnSend, button)

			self.button = self.button + [(label, button)]

	def CreateStaticText(self):
		for eachText in self.StaticTextData():
			label = eachText[0]
			x, y = eachText[1]
			w, h = eachText[2]

			staticText = wx.StaticText(self.panel, -1, label, pos=(x,y), size=(w, h))

			if label != "Cmd2:":
				staticText.Show(False)

			self.StaticText = self.StaticText + [(label, staticText)]

	def CreateComboBox(self):
		for eachComBox in self.ComboBoxData():

			label = eachComBox[0]
			x, y = eachComBox[1]
			w, h = eachComBox[2]

			combobox = None
			if label == "Cmd2ComboBox": 
				combobox = wx.ComboBox(self.panel, -1, self.Cmd2List[0],
						(x, y), wx.DefaultSize, self.Cmd2List, wx.CB_SIMPLE)
				self.Cmd2ComboBox = combobox
				self.Bind(wx.EVT_COMBOBOX, self.OnCmd, combobox)
				combobox.Show(True)

			if label == "PatternComboBox":
				combobox = wx.ComboBox(self.panel, -1, self.VideoOutInPatternList[0],
						(x, y), wx.DefaultSize, self.VideoOutInPatternList, wx.CB_SIMPLE)
				self.PatternComboBox = combobox
				combobox.Show(False)

			if label == "VideoInExtPattern":
				combobox = wx.ComboBox(self.panel, -1, self.VideoInExtPatternList[0],
						(x, y), wx.DefaultSize, self.VideoInExtPatternList, wx.CB_SIMPLE)
				self.VideoInExtPatternComboBox = combobox
				combobox.Show(False)

			if label == "VideoInStatus":
				combobox = wx.ComboBox(self.panel, -1, self.VideoInStatusList[0],
						(x, y), wx.DefaultSize, self.VideoInStatusList, wx.CB_SIMPLE)
				self.VideoInStatusComboBox = combobox
				combobox.Show(False)

			if combobox != None:
				self.ComboBox = self.ComboBox + [(label, combobox)]

	def CreateRadioBox(self):
		RadioBoxList = ['NTSC', 'PAL', 'LOCK']

		for eachRadioBox in self.RadioBoxData():
			label = eachRadioBox[0]
			x, y = eachRadioBox[1]
			w, h = eachRadioBox[2]

			self.RadioBox = wx.RadioBox(self.panel, -1, "", (x, y), (w, h),
				RadioBoxList, 3, wx.RA_SPECIFY_COLS)

		self.RadioBox.Enable(False)
		self.RadioBox.Show(False)

	def StaticTextData(self):
		return	(
				("Cmd2:",	(50, 50),	(150, 30)),
				("Pattern",	(50, 100),	(150, 30)),
				("Status", 	(50, 100),	(150, 30)),
				)

	def ComboBoxData(self):
		return	(
				("Cmd2ComboBox",		(180, 50 - 5), (150, 30)),
				("PatternComboBox",		(180, 100 - 5), (150, 30)),
				("VideoInExtPattern",	(180, 100 - 5), (150, 30)),
				("VideoInStatus",		(180, 100 - 5), (150, 30)),
				)

	def RadioBoxData(self):
		return	(
				("RadioBox", 			(50, 150),		(200, 50)),
				)

	def ButtonData(self):
		return	(
				("Send", (50, 280), (150, 30)),
				("Recv", (220, 280), (150, 30)),
				)

	def Cmd2Data(self):
		return	(
				("Video Out Setup", 			0x01),
				("Video Out Int Test Pattern",	0x02),
				("Video Out Ext Test Pattern",	0x03),
				("Video In Source Switch", 		0x04),
				("Video In Ext Test Pattern",	0x05),
				("Video In Ext  Status",		0x06),
				)

	def VideoOutInPatternData(self):
		return	(
				("red",							0x01),
				("green",						0x02),
				("blue", 						0x03), 
				("white", 						0x04),
				("black",						0x05),
				("Color Bars",					0x06),
				("black & white stripes",		0x07),
				("Print some chars on screen",	0x08),
				("RGB-SW",						0x09),
				("RGB-SW gradient",				0x0A),
				("EBU colors" , 				0x0b),
				("Flicker1:Gray", 				0x0c),
				("Flicker2: BW alternating", 	0x0d),
				("Flicker3: altern. grad.",		0x0e),
				("Testscreen show",				0x0f),
				("2D Dot Inversion", 			0x10),
				("1D Dot Inversion", 			0x11),
				("Invert frame",				0x12),
				("RGB565",						0x13),
				)

	def VideoInExtPatternData(self):
		return	(
				(0x01, "red"),
				(0x02, "green" ),
				(0x03, "blue", ),
				(0x04, "white" ),
				(0x05, "black"),
				(0x06, "Color Bars"),
				(0x07, "Luma Ramp"),
				)

	def VideoInStatusData(self):
		return	(
				(0x01, "Format check"),
				(0x02, "Colorbar check"),
				(0x03, "Luma check"),
				)

if __name__ == '__main__':
	app = wx.App(redirect=False)
	frame = GraphicFrame(parent=None, id=-1, frame=None)
	frame.Show(True)
	app.MainLoop()
