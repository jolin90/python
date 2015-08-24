def hex2(value):
	list = [ (0, "00"),
	(0x01, "01"), (0x02, "02"), (0x03, "03"), (0x04, "04"), (0x05, "05"), (0x06, "06"), (0x07, "07"),
	(0x08, "08"), (0x09, "09"), (0x0a, "0a"), (0x0b, "0b"), (0x0c, "0c"), (0x0d, "0d"), (0x0e, "0e"), 
	(0x0f, "0f"), (0x10, "10"), 
	(0x11, "11"), (0x12, "12"), (0x13, "13"), (0x14, "14"), (0x15, "15"), (0x16, "16"), (0x17, "17"),
	(0x18, "18"), (0x19, "19"), (0x1a, "1a"), (0x1b, "1b"), (0x1c, "1c"), (0x1d, "1d"), (0x1e, "1e"),
	(0x1f, "1f"), (0x20, "20"), (0x21, "21"), (0x22, "22"), (0x23, "23"), (0x24, "24"), (0x25, "25"),
	(0x26, "26"), (0x27, "27"), (0x28, "28"), (0x29, "29"), (0x2a, "2a"), (0x2b, "2b"), (0x2c, "2c"),
	(0x2d, "2d"), (0x2e, "2e"), (0x2f, "2f"), (0x30, "30"), (0x31, "31"), (0x32, "32"), (0x33, "33"),
	(0x34, "34"), (0x35, "35"), (0x36, "36"), (0x37, "37"), (0x38, "38"), (0x39, "39"), (0x3a, "3a"),
	(0x3b, "3b"), (0x3c, "3c"), (0x3d, "3d"), (0x3e, "3e"), (0x3f, "3f"), (0x40, "40"), (0x41, "41"),
	(0x42, "42"), (0x43, "43"), (0x44, "44"), (0x45, "45"), (0x46, "46"), (0x47, "47"), (0x48, "48"),
	(0x49, "49"), (0x4a, "4a"), (0x4b, "4b"), (0x4c, "4c"), (0x4d, "4d"), (0x4e, "4e"), (0x4f, "4f"),
	(0x50, "50"), (0x51, "51"), (0x52, "52"), (0x53, "53"), (0x54, "54"), (0x55, "55"), (0x56, "56"),
	(0x57, "57"), (0x58, "58"), (0x59, "59"), (0x5a, "5a"), (0x5b, "5b"), (0x5c, "5c"), (0x5d, "5d"),
	(0x5e, "5e"), (0x5f, "5f"), (0x60, "60"), (0x61, "61"), (0x62, "62"), (0x63, "63"), (0x64, "64"),
	(0x65, "65"), (0x66, "66"), (0x67, "67"), (0x68, "68"), (0x69, "69"), (0x6a, "6a"), (0x6b, "6b"),
	(0x6c, "6c"), (0x6d, "6d"), (0x6e, "6e"), (0x6f, "6f"), (0x70, "70"), (0x71, "71"), (0x72, "72"),
	(0x73, "73"), (0x74, "74"), (0x75, "75"), (0x76, "76"), (0x77, "77"), (0x78, "78"), (0x79, "79"),
	(0x7a, "7a"), (0x7b, "7b"), (0x7c, "7c"), (0x7d, "7d"), (0x7e, "7e"), (0x7f, "7f"), (0x80, "80"),
	(0x81, "81"), (0x82, "82"), (0x83, "83"), (0x84, "84"), (0x85, "85"), (0x86, "86"), (0x87, "87"),
	(0x88, "88"), (0x89, "89"), (0x8a, "8a"), (0x8b, "8b"), (0x8c, "8c"), (0x8d, "8d"), (0x8e, "8e"),
	(0x8f, "8f"), (0x90, "90"), (0x91, "91"), (0x92, "92"), (0x93, "93"), (0x94, "94"), (0x95, "95"),
	(0x96, "96"), (0x97, "97"), (0x98, "98"), (0x99, "99"), (0x9a, "9a"), (0x9b, "9b"), (0x9c, "9c"),
	(0x9d, "9d"), (0x9e, "9e"), (0x9f, "9f"), (0xa0, "a0"), (0xa1, "a1"), (0xa2, "a2"), (0xa3, "a3"),
	(0xa4, "a4"), (0xa5, "a5"), (0xa6, "a6"), (0xa7, "a7"), (0xa8, "a8"), (0xa9, "a9"), (0xaa, "aa"),
	(0xab, "ab"), (0xac, "ac"), (0xad, "ad"), (0xae, "ae"), (0xaf, "af"), (0xb0, "b0"), (0xb1, "b1"),
	(0xb2, "b2"), (0xb3, "b3"), (0xb4, "b4"), (0xb5, "b5"), (0xb6, "b6"), (0xb7, "b7"), (0xb8, "b8"),
	(0xb9, "b9"), (0xba, "ba"), (0xbb, "bb"), (0xbc, "bc"), (0xbd, "bd"), (0xbe, "be"), (0xbf, "bf"),
	(0xc0, "c0"), (0xc1, "c1"), (0xc2, "c2"), (0xc3, "c3"), (0xc4, "c4"), (0xc5, "c5"), (0xc6, "c6"),
	(0xc7, "c7"), (0xc8, "c8"), (0xc9, "c9"), (0xca, "ca"), (0xcb, "cb"), (0xcc, "cc"), (0xcd, "cd"),
	(0xce, "ce"), (0xcf, "cf"), (0xd0, "d0"), (0xd1, "d1"), (0xd2, "d2"), (0xd3, "d3"), (0xd4, "d4"),
	(0xd5, "d5"), (0xd6, "d6"), (0xd7, "d7"), (0xd8, "d8"), (0xd9, "d9"), (0xda, "da"), (0xdb, "db"),
	(0xdc, "dc"), (0xdd, "dd"), (0xde, "de"), (0xdf, "df"), (0xe0, "e0"), (0xe1, "e1"), (0xe2, "e2"),
	(0xe3, "e3"), (0xe4, "e4"), (0xe5, "e5"), (0xe6, "e6"), (0xe7, "e7"), (0xe8, "e8"), (0xe9, "e9"),
	(0xea, "ea"), (0xeb, "eb"), (0xec, "ec"), (0xed, "ed"), (0xee, "ee"), (0xef, "ef"), (0xf0, "f0"),
	(0xf1, "f1"), (0xf2, "f2"), (0xf3, "f3"), (0xf4, "f4"), (0xf5, "f5"), (0xf6, "f6"), (0xf7, "f7"),
	(0xf8, "f8"), (0xf9, "f9"), (0xfa, "fa"), (0xfb, "fb"), (0xfc, "fc"), (0xfd, "fd"), (0xfe, "fe"),
	(0xff, "ff") 
	]

	for list1, list2 in list:
		if list1 == value:
			return list2

	return None

class MyData:
	def __init__(self):
		self.list1 = [0x3b, 0x0]
		self.list2 = [0, 0, 0, 0]
		self.list3 = []
		self.list4 = [0x0]
	
	def setlist2(self, buf1):
		list2 = ["00", "00", "00", "00"]

		buf1 = buf1.strip(" ")
		buf1 = buf1.replace(" ", "")

		for i in range(0, 4, 1):
			if buf1[0:2] == None:
				break
			if len(buf1) < 2:
				break
			list2[i] = buf1[0:2]
			buf1 = buf1[2:]
		
		for i in range(0, 4, 1):
			self.list2[i] = int(list2[i], 16)

		return self.list2

	def setlist3(self, buf2):
		if (buf2 == None): 
			return None

		buf2 = buf2.strip(" ").replace(" ", "")

		if	(len(buf2) < 2):
			return None

		buf3 = ""
		for i in range(0, len(buf2) / 2, 1):
			buf3 = buf3 + ("%s " % buf2[0:2])
			buf2 = buf2[2:]
		list3 = buf3.strip(" ").split(" ")

		for i in range(0, len(list3), 1):
			list3[i] = int(list3[i], 16)

		self.list3 = list3

		return self.list3
	
	def setlist1(self, list2, list3):
		if list3 == None:
			self.list1[1] = len(list2)
		else:
			self.list1[1] = len(list2) + len(list3)
	
	def checksum(self, listsum):
		sum = 0
		for i in range(0, len(listsum), 1):
			sum ^= listsum[i]
		return sum

	def setMsg(self, buf1, buf2):
		self.setlist2(buf1)
		self.setlist3(buf2)
		self.setlist1(self.list2, self.list3)

		if self.list3 == None:
			self.list4[0] = self.checksum(self.list1 + self.list2)
			return self.list1 + self.list2 + self.list4
		else:
			self.list4[0] = self.checksum(self.list1 + self.list2 + self.list3)
			return self.list1 + self.list2 + self.list3 + self.list4


if __name__ == '__main__':
	"""
	data = MyData()
	#print data.setMsg("05340100", buf2=None)
	print data.setlist3(buf2=None)
	print data.setlist3(buf2="1")
	print data.setlist3(buf2="12")
	print data.setlist3(buf2="123")
	"""

	for i in range(0, 0xff + 1, 1):
		print hex2(i),
