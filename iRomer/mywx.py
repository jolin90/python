import wx

def CreateTextCtrl(self, TextCtrlData):
    if not self.panel:
        return
    if not TextCtrlData:
        return

    TextCtrlList = []

    for eachTextCtrl in TextCtrlData:
        index = eachTextCtrl[0]
        x, y = eachTextCtrl[1]
        w, h = eachTextCtrl[2]
        label = eachTextCtrl[3]

        TextCtrlList = TextCtrlList + [(index, label, wx.TextCtrl(self.panel, -1, \
                "", (x,y), (w, h)))]

    return TextCtrlList

def GetTextCtrlByIndex(List, index):
   for x, y, z in List:
       if x == index:
           return z
   return None

def GetTextCtrlByLabel(List, label):
    for x, y, z in List:
        if y == label:
            return z
    return None

def CreateStaticText(self, StaticText):
    if not self.panel:
        return
    if not StaticText:
        return

    for each in StaticText:
        index = each[0]
        x, y  = each[1]
        w, h  = each[2]
        label = each[3]
        wx.StaticText(self.panel, -1, label, (x,y), (w,h))

def CreateButton(this, Button):
    if not this:
        return
    if not Button:
        return

    for each in Button:
        index = Button.index(each)
        x, y = each[1]
        w, h = each[2]
        label = each[3]
        this.Bind(wx.EVT_BUTTON, each[4], \
                wx.Button(this.panel, -1, label, (x, y), (w, h)))

def CreateComboBox(this, ComboBox, List):
    if not this.panel:
        return
    if not ComboBox:
        return

    ComboBoxList = []

    for each in ComboBox:
        index = each[0]
        x, y = each[1]
        w, h = each[2]
        label = each[3]

        ComboBoxList = ComboBoxList + [(index, label, wx.ComboBox(this.panel, \
                -1, List[0], (x, y), (w, h), List, wx.CB_DROPDOWN)),]

    return ComboBoxList

def GetComboBoxByIndex(List, index):
   for x, y, z in List:
       if x == index:
           return z
   return None

def GetComboBoxByLabel(List, label):
    for x, y, z in List:
        if y == label:
            return z
    return None
