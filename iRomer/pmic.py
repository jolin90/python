import wx
import mystr
import myserial
import time

class PmicFrame(wx.Frame):

	def __init__(self, parent, id, frame):
		wx.Frame.__init__(self, parent, id, 'PMIC test', pos=(500, 260),
				size=(520, 650))

		self.frame = frame
		self.panel = wx.Panel(self)

		self.CreateLayoutBox()
		self.CreateButton()
		self.TextCtrlList = self.CreateTextCtrl()
		self.CreateStaticText()

	def CreateLayoutBox(self):

		for eachGroupBox in self.GroupBoxData():
			x, y = eachGroupBox[1]
			w, h = eachGroupBox[2]
			label = eachGroupBox[3]
			wx.RadioBox(self.panel, -1, label, (x, y), (w, h), [], 0, wx.RA_SPECIFY_COLS)

	def CreateButton(self):
		ButtonList = []

		for eachButton in self.ButtonData():
			index = self.ButtonData().index(eachButton)
			x, y = eachButton[1]
			w, h = eachButton[2]
			label = eachButton[3]
			ButtonList = ButtonList + [wx.Button(self.panel, -1, label, (x, y), (w, h))]
			self.Bind(wx.EVT_BUTTON, eachButton[4], ButtonList[index])

		return ButtonList

	def SetTextCtrlValue(self, TextList, index, value):

		for x, y in TextList:
			if x == index:
				y.SetValue(value)
				return y

		return None

	def GetTextCtrl(self, index):

		for x, y in self.TextCtrlList:
			if x == index:
				return y

		return None

	def CreateTextCtrl(self):
		TextCtrlList = []

		for eachTextCtrl in self.TextCtrlData():
			index = eachTextCtrl[0]
			x, y = eachTextCtrl[1]
			w, h = eachTextCtrl[2]

			TextCtrlList = TextCtrlList + [(index, wx.TextCtrl(self.panel, -1,
				"", (x,y), (w, h)))]

		return TextCtrlList

	def CreateStaticText(self):

		for eachStaticText in self.StaticTextData():
			index = eachStaticText[0]
			x, y = eachStaticText[1]
			w, h = eachStaticText[2]
			label = eachStaticText[3]

			if not label:
				return

			wx.StaticText(self.panel, -1, label, (x,y), (w,h))


	def OnCheckLdo(self, event):
		if not self.frame:
			return

		buf2 = ""

		for eachLdo in self.Da9063Info():
			index = eachLdo[0]
			name = eachLdo[1]
			buf1 = eachLdo[2]
			v_min, v_max = eachLdo[3]
			v_start, v_step = eachLdo[4]

			recvlist = self.frame.ProcessBuffData(buf1, buf2)
			if not recvlist:
				return

			enable = recvlist[10]
			voltage_t = recvlist[11]
			is_limit = recvlist[12]
			oc_limit = recvlist[13]

			if enable == 1:
				self.GetTextCtrl(index + 1).SetValue("1")
			else:
				self.GetTextCtrl(index + 1).SetValue("0")
				self.GetTextCtrl(index + 1).Enable(False)
				self.GetTextCtrl(index + 12).Enable(False)
				self.GetTextCtrl(index + 23).Enable(False)

			voltage = 0
			if voltage_t < v_start:
				voltage = v_min
			else:
				voltage = v_min + (voltage_t - v_start) * v_step

			if voltage > v_max:
				voltage = v_max

			self.GetTextCtrl(index + 12).SetValue("%d mV" % voltage)

			if is_limit == 0:
				self.GetTextCtrl(index + 23).SetValue("-")
			if is_limit == 1:
				self.GetTextCtrl(index + 23).SetValue("%d" % oc_limit)

	def OnReadid(self, event):
		if not self.frame:
			return

		buf1 = "05 40 01 00"
		buf2 = ""

		recvlist = self.frame.ProcessBuffData(buf1, buf2)
		if not recvlist:
			return

		self.GetTextCtrl(1).SetValue("%s" % hex(recvlist[10]))

	def GroupBoxData(self):
		return	(
				(0, (30, 10), (460, 80), ""),
				(1, (30, 100), (460, 520), ""),
				)

	def ButtonData(self):
		return	(
				(0, (50, 40), (150, 30), "Read device id", self.OnReadid),
				(1, (50, 570), (150, 30), "check ldo sattus", self.OnCheckLdo),
				)

	def TextCtrlData(self):
		return	(
				(1, (250, 40), (150, 30), ""),

				(2, (160, 130 - 5), (30, 30), "enable"),
				(3, (160, 170 - 5), (30, 30), "enable"),
				(4, (160, 210 - 5), (30, 30), "enable"),
				(5, (160, 250 - 5), (30, 30), "enable"),
				(6, (160, 290 - 5), (30, 30), "enable"),
				(7, (160, 330 - 5), (30, 30), "enable"),
				(8, (160, 370 - 5), (30, 30), "enable"),
				(9, (160, 410 - 5), (30, 30), "enable"),
				(10, (160, 450 - 5), (30, 30), "enable"),
				(11, (160, 490 - 5), (30, 30), "enable"),
				(12, (160, 530 - 5), (30, 30), "enable"),

				(13, (260, 130 - 5), (80, 30), "voltage"),
				(14, (260, 170 - 5), (80, 30), "voltage"),
				(15, (260, 210 - 5), (80, 30), "voltage"),
				(16, (260, 250 - 5), (80, 30), "voltage"),
				(17, (260, 290 - 5), (80, 30), "voltage"),
				(18, (260, 330 - 5), (80, 30), "voltage"),
				(19, (260, 370 - 5), (80, 30), "voltage"),
				(20, (260, 410 - 5), (80, 30), "voltage"),
				(21, (260, 450 - 5), (80, 30), "voltage"),
				(22, (260, 490 - 5), (80, 30), "voltage"),
				(23, (260, 530 - 5), (80, 30), "voltage"),

				(24, (440, 130 - 5), (30, 30), "limit"),
				(25, (440, 170 - 5), (30, 30), "limit"),
				(26, (440, 210 - 5), (30, 30), "limit"),
				(27, (440, 250 - 5), (30, 30), "limit"),
				(28, (440, 290 - 5), (30, 30), "limit"),
				(29, (440, 330 - 5), (30, 30), "limit"),
				(30, (440, 370 - 5), (30, 30), "limit"),
				(31, (440, 410 - 5), (30, 30), "limit"),
				(32, (440, 450 - 5), (30, 30), "limit"),
				(33, (440, 490 - 5), (30, 30), "limit"),
				(34, (440, 530 - 5), (30, 30), "limit"),
				)

	def StaticTextData(self):
		return	(
				(1, (50, 130), (150, 30), "LDO1:"),
				(2, (50, 170), (150, 30), "LDO2:"),
				(2, (50, 210), (150, 30), "LDO3:"),
				(2, (50, 250), (150, 30), "LDO4:"),
				(2, (50, 290), (150, 30), "LDO5:"),
				(2, (50, 330), (150, 30), "LDO6:"),
				(2, (50, 370), (150, 30), "LDO7:"),
				(2, (50, 410), (150, 30), "LDO8:"),
				(2, (50, 450), (150, 30), "LDO9:"),
				(2, (50, 490), (150, 30), "LDO10:"),
				(2, (50, 530), (150, 30), "LDO11:"),

				(1, (110, 130), (150, 30), "enable"),
				(2, (110, 170), (150, 30), "enable"),
				(2, (110, 210), (150, 30), "enable"),
				(2, (110, 250), (150, 30), "enable"),
				(2, (110, 290), (150, 30), "enable"),
				(2, (110, 330), (150, 30), "enable"),
				(2, (110, 370), (150, 30), "enable"),
				(2, (110, 410), (150, 30), "enable"),
				(2, (110, 450), (150, 30), "enable"),
				(2, (110, 490), (150, 30), "enable"),
				(2, (110, 530), (150, 30), "enable"),

				(1, (200, 130), (150, 30), "voltage"),
				(2, (200, 170), (150, 30), "voltage"),
				(2, (200, 210), (150, 30), "voltage"),
				(2, (200, 250), (150, 30), "voltage"),
				(2, (200, 290), (150, 30), "voltage"),
				(2, (200, 330), (150, 30), "voltage"),
				(2, (200, 370), (150, 30), "voltage"),
				(2, (200, 410), (150, 30), "voltage"),
				(2, (200, 450), (150, 30), "voltage"),
				(2, (200, 490), (150, 30), "voltage"),
				(2, (200, 530), (150, 30), "voltage"),

				(1, (350, 130), (150, 30), "over current"),
				(2, (350, 170), (150, 30), "over current"),
				(2, (350, 210), (150, 30), "over current"),
				(2, (350, 250), (150, 30), "over current"),
				(2, (350, 290), (150, 30), "over current"),
				(2, (350, 330), (150, 30), "over current"),
				(2, (350, 370), (150, 30), "over current"),
				(2, (350, 410), (150, 30), "over current"),
				(2, (350, 450), (150, 30), "over current"),
				(2, (350, 490), (150, 30), "over current"),
				(2, (350, 530), (150, 30), "over current"),
				)

	def Da9063Info(self):
		return	(
				(1, "ldo1", ("05400200"), (600, 1860), (0x0, 20)),
				(2, "ldo2", ("05400201"), (600, 1860), (0x0, 20)),
				(3, "ldo3", ("05400202"), (900, 3440), (0x0, 20)),
				(4, "ldo4", ("05400203"), (900, 3440), (0x0, 20)),
				(5, "ldo5", ("05400204"), (900, 3600), (0x2, 50)),
				(6, "ldo6", ("05400205"), (900, 3600), (0x2, 50)),
				(7, "ldo7", ("05400206"), (900, 3600), (0x2, 50)),
				(8, "ldo8", ("05400207"), (900, 3600), (0x2, 50)),
				(9, "ldo9", ("05400208"), (950, 3600), (0x2, 50)),
				(10, "ldo10", ("05400209"), (900, 3600), (0x2, 50)),
				(11, "ldo11", ("0540020A"), (900, 3600), (0x2, 50)),
				)


if __name__ == '__main__':
	app = wx.App(redirect=False)
	frame = PmicFrame(parent=None, id=-1, frame=None)
	frame.Show(True)
	app.MainLoop()
