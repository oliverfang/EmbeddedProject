import serial
import wx
import time

class mbedMonitor(wx.Frame):

	# define global variables
	xAcc = 0.0
	yAcc = 0.0
	zAcc = 0.0
	xMag = 0.0
	yMag = 0.0
	zMag = 0.0
	lightVal = 0.0
	touchVal = 0.0
	serdev = '/dev/tty.usbmodem412'

	def __init__(self, parent):
		wx.Frame.__init__(self, parent, wx.ID_ANY, "mbed Monitor", size=(500, 200))
		# set minimum size
		self.SetMinSize(self.GetSize())
		self.SetMaxSize(self.GetSize())

		# build a panel
		self.mp = wx.Panel(self, wx.ID_ANY)

		# build a status bar 
		self.statusBar = self.CreateStatusBar()

		# create a timer
		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.updateData, self.timer)

		# create some static text

		# Accelerometer
		self.accText = wx.StaticText(self.mp, -1, "Accelerometer: ", size=(120, -1), style=wx.ALIGN_RIGHT)
		self.xAccLabel = wx.StaticText(self.mp, -1, "X: ", size=(20, -1), style=wx.ALIGN_LEFT)
		self.xAccVal = wx.StaticText(self.mp, -1, "0.0", size=(80, -1), style=wx.ALIGN_LEFT)
		
		self.yAccLabel = wx.StaticText(self.mp, -1, "Y: ", size=(20, -1), style=wx.ALIGN_LEFT)
		self.yAccVal = wx.StaticText(self.mp, -1, "0.0", size=(80, -1), style=wx.ALIGN_LEFT)
		
		self.zAccLabel = wx.StaticText(self.mp, -1, "Z: ", size=(20, -1), style=wx.ALIGN_LEFT)
		self.zAccVal = wx.StaticText(self.mp, -1, "0.0", size=(80, -1), style=wx.ALIGN_LEFT)
		
		# Accelerometer
		self.magText = wx.StaticText(self.mp, -1, "Magnetometer: ", size=(120, -1), style=wx.ALIGN_RIGHT)
		self.xMagLabel = wx.StaticText(self.mp, -1, "X: ", size=(20, -1), style=wx.ALIGN_LEFT)
		self.xMagVal = wx.StaticText(self.mp, -1, "0.0", size=(80, -1), style=wx.ALIGN_LEFT)
		
		self.yMagLabel = wx.StaticText(self.mp, -1, "Y: ", size=(20, -1), style=wx.ALIGN_LEFT)
		self.yMagVal = wx.StaticText(self.mp, -1, "0.0", size=(80, -1), style=wx.ALIGN_LEFT)
		
		self.zMagLabel = wx.StaticText(self.mp, -1, "Z: ", size=(20, -1), style=wx.ALIGN_LEFT)
		self.zMagVal = wx.StaticText(self.mp, -1, "0.0", size=(80, -1), style=wx.ALIGN_LEFT)

		# Light
		self.lightText = wx.StaticText(self.mp, -1, "Light sensor: ", size=(120, -1), style=wx.ALIGN_RIGHT)
		self.lightVal = wx.StaticText(self.mp, -1, "0.0", size=(80, -1), style=wx.ALIGN_LEFT)
		
		# Touch
		self.touchText = wx.StaticText(self.mp, -1, "Touch sensor: ", size=(120, -1), style=wx.ALIGN_RIGHT)
		self.touchVal = wx.StaticText(self.mp, -1, "0.0", size=(80, -1), style=wx.ALIGN_LEFT)
		
		# Configure mbed serial port
		self.mbed = serial.Serial(self.serdev)
		self.mbed.baudrate = 9600
		
		self.defineSizers()

		# start sampling
		self.timer.Start(100)
		print "Sampling..."

	def assignData(self, parsedData):
		# skip first entry
		self.xAcc = parsedData[1]
		self.yAcc = parsedData[2]
		self.zAcc = parsedData[3]
		self.xMag = parsedData[4]
		self.yMag = parsedData[5]
		self.zMag = parsedData[6]
		self.lightVal = parsedData[7]
		self.touchVal = parsedData[8]

	def updateData(self, event):
		dataLine = self.mbed.readline()
		parsedData = dataLine.split("/")
		if len(parsedData) == 10:
			#self.assignData(parsedData)
			self.xAccVal.SetLabel(parsedData[1])
			self.yAccVal.SetLabel(parsedData[2])
			self.zAccVal.SetLabel(parsedData[3])
			self.xMagVal.SetLabel(parsedData[4])
			self.yMagVal.SetLabel(parsedData[5])
			self.zMagVal.SetLabel(parsedData[6])
			self.lightVal.SetLabel(parsedData[7])
			self.touchVal.SetLabel(parsedData[8])


	def defineSizers(self):
		self.accSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.accSizer.Add(self.accText, 0, wx.ALL, 5)
		self.accSizer.Add(self.xAccLabel, 0, wx.ALL, 5)
		self.accSizer.Add(self.xAccVal, 0, wx.ALL, 5)
		self.accSizer.Add(self.yAccLabel, 0, wx.ALL, 5)
		self.accSizer.Add(self.yAccVal, 0, wx.ALL, 5)
		self.accSizer.Add(self.zAccLabel, 0, wx.ALL, 5)
		self.accSizer.Add(self.zAccVal, 0, wx.ALL, 5)

		self.magSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.magSizer.Add(self.magText, 0, wx.ALL, 5)
		self.magSizer.Add(self.xMagLabel, 0, wx.ALL, 5)
		self.magSizer.Add(self.xMagVal, 0, wx.ALL, 5)
		self.magSizer.Add(self.yMagLabel, 0, wx.ALL, 5)
		self.magSizer.Add(self.yMagVal, 0, wx.ALL, 5)
		self.magSizer.Add(self.zMagLabel, 0, wx.ALL, 5)
		self.magSizer.Add(self.zMagVal, 0, wx.ALL, 5)

		self.lightSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.lightSizer.Add(self.lightText, 0, wx.ALL, 5)
		self.lightSizer.Add(self.lightVal, 0, wx.ALL, 5)
		
		self.touchSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.touchSizer.Add(self.touchText, 0, wx.ALL, 5)
		self.touchSizer.Add(self.touchVal, 0, wx.ALL, 5)
		
		self.topSizer = wx.BoxSizer(wx.VERTICAL)
		self.topSizer.Add(self.accSizer)
		self.topSizer.Add(self.magSizer)
		self.topSizer.Add(self.lightSizer)
		self.topSizer.Add(self.touchSizer)

		self.mp.SetAutoLayout(True)
		self.mp.SetSizer(self.topSizer)
		self.mp.Layout()
		self.Layout()


# below is needed for all GUIs
if __name__== '__main__':
	app = wx.App(False) # application object (inner workings) 
	frame = mbedMonitor(parent = None) # frame object (what user sees)
	frame.Show() # show frame
	app.MainLoop() # run main loop	



