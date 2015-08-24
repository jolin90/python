import wx
import mystr
import myserial
import time

from mystr import hex2

class TPFrame(wx.Frame):

	def __init__(self, parent, id, frame):
		wx.Frame.__init__(self, parent, id, 'TP test', pos=(500, 260),
				size=(520, 480))

		self.frame = frame
		self.panel = wx.Panel(self)

		self.CreateLayoutBox()
		self.CreateButton()
		self.TextCtrlList = self.CreateTextCtrl()
		self.CreateStaticText()
		self.CreateComboBox()

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

	def GetTextCtrlByIndex(self, index):

		for x, y, z in self.TextCtrlList:
			if x == index:
				return z

		return None

	def GetTextCtrlByLabel(self, label):

		for x, y, z in self.TextCtrlList:
			if y == label:
				return z

		return None

	def CreateTextCtrl(self):
		TextCtrlList = []

		for eachTextCtrl in self.TextCtrlData():
			index = eachTextCtrl[0]
			x, y = eachTextCtrl[1]
			w, h = eachTextCtrl[2]
			label = eachTextCtrl[3]

			TextCtrlList = TextCtrlList + [(index, label, wx.TextCtrl(self.panel, -1,
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

	def CreateComboBox(self):
		readlenlist = ["1", "2", "3","4","5", "6","7", 
				"8", "9", "10","11","12", "13","14",
				"15", "16"]

		for eachCombobox in self.ComboBoxData():
			index = eachCombobox[0]
			x, y = eachCombobox[1]
			w, h = eachCombobox[2]
			label = eachCombobox[3]

			self.readlenComboBox = wx.ComboBox(self.panel, -1, "1",	(x,y), wx.DefaultSize, readlenlist, wx.CB_SIMPLE)

		return

	def OnReadid(self, event):
		return
	
	def OnReadRegisters(self, event):
		if not self.frame:
			return

		buf1 = "05410100"
		buf2 = self.GetTextCtrlByLabel("regread").GetValue()

		if not buf2:
			return

		if len(buf2) == 1:
			return

		buf2 = buf2[0:2]
		self.GetTextCtrlByLabel("regread").SetValue(buf2)

		readlen = int(self.readlenComboBox.GetValue())
		buf2 = buf2 + hex2(readlen)

		recvlist = self.frame.ProcessBuffData(buf1, buf2)

		if not recvlist:
			return

		if recvlist[6] == 1:
			read_from_tm = ""
			for i in range(0, readlen, 1):
				read_from_tm = read_from_tm + " " + hex2(recvlist[10 + i])

			self.GetTextCtrlByLabel("readdata").SetValue(read_from_tm)

		return

	def setTextValue(self, buf):

		if not buf:
			return None

		buf  = buf.strip(" ").replace(" ", "")

		if len(buf) < 2:
			return None

		buf_t = ""
		for i in range(0, len(buf) / 2, 1):
			buf_t = buf_t + " " + buf[0:2]
			buf = buf[2:]

		return buf_t

	def OnWriteRegisters(self, event):

		if not self.frame:
			return

		buf1 = "05410200"
		buf2 = self.GetTextCtrlByLabel("regwrite").GetValue()

		if not buf2 or len(buf2) == 1:
			return

		buf2 = buf2[0:2]
		self.GetTextCtrlByLabel("regwrite").SetValue(buf2)

		textCtrl = self.GetTextCtrlByLabel("writedata")

		buf_t = textCtrl.GetValue()
		buf_t = self.setTextValue(buf_t)
		if not buf_t:
			return

		buf_t = buf_t.strip(" ")
		textCtrl.SetValue(buf_t)
		buf_t = buf_t.replace(" ", "")

		buf2 = buf2 + hex2(len(buf_t)/2) + buf_t
		
		self.frame.ProcessBuffData(buf1, buf2)

		return

	def GroupBoxData(self):
		return	(
				(0, (30, 10), (460, 80), ""),
				(1, (30, 100), (460, 150), "read register"),
				(1, (30, 270), (460, 150), "wtite register"),
				)

	def ButtonData(self):
		return	(
				(1, (50, 40), (150, 30), "Read device id", self.OnReadid),
				(2, (50, 200), (150, 30), "send", self.OnReadRegisters),
				(3, (50, 370), (150, 30), "send", self.OnWriteRegisters),
				)

	def TextCtrlData(self):
		return	(
				(1, (250, 40), (150, 30), "deviceid"),
				(2, (50, 150), (150, 30), "regread"),
				(3, (250, 200), (190, 30), "readdata"),

				(4, (50, 320), (150, 30), "regwrite"),
				(5, (250, 320), (190, 30), "writedata"),
				)

	def StaticTextData(self):
		return	(
				(1, (50, 130), (100, 30), "reg command"),
				(1, (250, 130), (100, 30), "read length"),

				(1, (50, 300), (100, 30), "reg command"),
				(1, (250, 300), (100, 30), "write data"),
				)

	def ComboBoxData(self):
		return	(
				(1, (250, 150), (60, 30), "read_len"),
				)


if __name__ == '__main__':
	app = wx.App(redirect=False)
	frame = TPFrame(parent=None, id=-1, frame=None)
	frame.Show(True)
	app.MainLoop()
