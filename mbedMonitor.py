import serial
import wx
import time
import datetime
from mbedSerial import *
from xivelyFeed import *

class mbedMonitor(wx.Frame):

	# define global variables
	timeArray = datetime.datetime.utcnow()
	xAcc = 0.0
	yAcc = 0.0
	zAcc = 0.0
	xMag = 0.0
	yMag = 0.0
	zMag = 0.0
	xLight = 0.0
	xTouch = 0.0
	xADC = 0.0
	accEn = True
	magEn = True
	lightEn = True
	touchEn = True
	adcEn = True
	serdev = '/dev/tty.usbmodem412'

	settingList = ["Accelerometer", "Magnetometer", "Light Sensor", "Touch Sensor", "ADC Sensor"]

	def __init__(self, parent):
		wx.Frame.__init__(self, parent, wx.ID_ANY, "mbed Monitor", size=(700, 280))
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

		# Create some UI elements

		# headers
		self.dataLabel = wx.StaticText(self.mp, -1, "Data", size=(470, -1), style=wx.ALIGN_LEFT)

		self.sampLabel = wx.StaticText(self.mp, -1, "Sampling Rate", size=(150, -1), style=wx.ALIGN_LEFT)

		# Accelerometer
		self.accText = wx.StaticText(self.mp, -1, "Accelerometer: ", size=(120, -1), style=wx.ALIGN_RIGHT)
		self.xAccLabel = wx.StaticText(self.mp, -1, "X: ", size=(20, -1), style=wx.ALIGN_LEFT)
		self.xAccVal = wx.StaticText(self.mp, -1, "0.0", size=(80, -1), style=wx.ALIGN_LEFT)
		
		self.yAccLabel = wx.StaticText(self.mp, -1, "Y: ", size=(20, -1), style=wx.ALIGN_LEFT)
		self.yAccVal = wx.StaticText(self.mp, -1, "0.0", size=(80, -1), style=wx.ALIGN_LEFT)
		
		self.zAccLabel = wx.StaticText(self.mp, -1, "Z: ", size=(20, -1), style=wx.ALIGN_LEFT)
		self.zAccVal = wx.StaticText(self.mp, -1, "0.0", size=(80, -1), style=wx.ALIGN_LEFT)
		
		self.accRateVal = wx.StaticText(self.mp, -1, "0.0", size=(80, -1), style=wx.ALIGN_LEFT)
		
		self.accButton = wx.Button(self.mp, id=wx.ID_ANY, label = "Disable", size=(100,-1))
		self.accButton.Bind(wx.EVT_BUTTON, self.enableAcc)
		
		# Magnetometer
		self.magText = wx.StaticText(self.mp, -1, "Magnetometer: ", size=(120, -1), style=wx.ALIGN_RIGHT)
		self.xMagLabel = wx.StaticText(self.mp, -1, "X: ", size=(20, -1), style=wx.ALIGN_LEFT)
		self.xMagVal = wx.StaticText(self.mp, -1, "0.0", size=(80, -1), style=wx.ALIGN_LEFT)
		
		self.yMagLabel = wx.StaticText(self.mp, -1, "Y: ", size=(20, -1), style=wx.ALIGN_LEFT)
		self.yMagVal = wx.StaticText(self.mp, -1, "0.0", size=(80, -1), style=wx.ALIGN_LEFT)
		
		self.zMagLabel = wx.StaticText(self.mp, -1, "Z: ", size=(20, -1), style=wx.ALIGN_LEFT)
		self.zMagVal = wx.StaticText(self.mp, -1, "0.0", size=(80, -1), style=wx.ALIGN_LEFT)

		self.magRateVal = wx.StaticText(self.mp, -1, "0.0", size=(80, -1), style=wx.ALIGN_LEFT)
		
		self.magButton = wx.Button(self.mp, id=wx.ID_ANY, label = "Disable", size=(100,-1))
		self.magButton.Bind(wx.EVT_BUTTON, self.enableMag)
		
		# Light
		self.lightText = wx.StaticText(self.mp, -1, "Light sensor: ", size=(120, -1), style=wx.ALIGN_RIGHT)
		self.lightVal = wx.StaticText(self.mp, -1, "0.0", size=(350, -1), style=wx.ALIGN_LEFT)
		self.lightRateVal = wx.StaticText(self.mp, -1, "0.0", size=(80, -1), style=wx.ALIGN_LEFT)

		self.lightButton = wx.Button(self.mp, id=wx.ID_ANY, label = "Disable", size=(100,-1))
		self.lightButton.Bind(wx.EVT_BUTTON, self.enableLight)
		
		# Touch
		self.touchText = wx.StaticText(self.mp, -1, "Touch sensor: ", size=(120, -1), style=wx.ALIGN_RIGHT)
		self.touchVal = wx.StaticText(self.mp, -1, "0.0", size=(350, -1), style=wx.ALIGN_LEFT)
		self.touchRateVal = wx.StaticText(self.mp, -1, "0.0", size=(80, -1), style=wx.ALIGN_LEFT)
		
		self.touchButton = wx.Button(self.mp, id=wx.ID_ANY, label = "Disable", size=(100,-1))
		self.touchButton.Bind(wx.EVT_BUTTON, self.enableTouch)
		
		# ADC
		self.adcText = wx.StaticText(self.mp, -1, "ADC sensor: ", size=(120, -1), style=wx.ALIGN_RIGHT)
		self.adcVal = wx.StaticText(self.mp, -1, "0.0", size=(350, -1), style=wx.ALIGN_LEFT)
		self.adcRateVal = wx.StaticText(self.mp, -1, "0.0", size=(80, -1), style=wx.ALIGN_LEFT)
		
		self.adcButton = wx.Button(self.mp, id=wx.ID_ANY, label = "Disable", size=(100,-1))
		self.adcButton.Bind(wx.EVT_BUTTON, self.enableADC)
		
		# Send settings
		self.cmdLabel = wx.StaticText(self.mp, -1, "Change Sampling Period: ", size=(170, -1), style=wx.ALIGN_RIGHT)
		self.cmdList = wx.Choice(self.mp, -1, size=(230, -1), choices=self.settingList)
		self.cmdVal = wx.TextCtrl(self.mp, value="0.0", size=(150,-1))
		self.cmdButton = wx.Button(self.mp, id=wx.ID_ANY, label = "Send", size=(100,-1))
		self.cmdButton.Bind(wx.EVT_BUTTON, self.onButton)

		# Configure mbed serial port (thread runs in background)
		self.mbedSerial = SerialData()

		# Create Xively Feed (thread runs in background)
		self.xively = XivelyFeed()
		
		# Define Sizers
		self.defineSizers()

		# Start sampling
		self.timer.Start(50)
		self.statusBar.SetStatusText("Sampling...")

	def assignData(self, parsedData):
		# skip first entry

		# collect data from parsedData and keep track of time it was collected
		self.xTime = datetime.datetime.utcnow()
		self.xAcc = parsedData[1]
		self.yAcc = parsedData[2]
		self.zAcc = parsedData[3]
		self.xMag = parsedData[4]
		self.yMag = parsedData[5]
		self.zMag = parsedData[6]
		self.xLight = parsedData[7]
		self.xTouch = parsedData[8]
		self.xADC = parsedData[9]

		# create data point for xivelyfeed
		self.xively.collectData([self.xTime, self.xAcc, self.yAcc, self.zAcc,
			self.xMag, self.yMag, self.zMag, self.xLight, self.xTouch, self.xADC])

		# update disable/enable buttons
		if parsedData[15] == "1":
			self.accEn = True
			self.accButton.SetLabel("Disable")
		else:
			self.accEn = False
			self.accButton.SetLabel("Enable")
		if parsedData[16] == "1":
			self.magEn = True
			self.magButton.SetLabel("Disable")
		else:
			self.magEn = False
			self.magButton.SetLabel("Enable")
		if parsedData[17] == "1":
			self.lightEn = True
			self.lightButton.SetLabel("Disable")
		else:
			self.lightEn = False
			self.lightButton.SetLabel("Enable")
		if parsedData[18] == "1":
			self.touchEn = True
			self.touchButton.SetLabel("Disable")
		else:
			self.touchEn = False
			self.touchButton.SetLabel("Enable")	
		if parsedData[19] == "1":
			self.adcEn = True
			self.adcButton.SetLabel("Disable")
		else:
			self.adcEn = False
			self.adcButton.SetLabel("Enable")	

		
	def updateData(self, event):
		dataLine = self.mbedSerial.next()
		#print dataLine
		parsedData = dataLine.split("/")
		self.assignData(parsedData)
		if len(parsedData) == 21:
			#self.assignData(parsedData)
			self.xAccVal.SetLabel(parsedData[1])
			self.yAccVal.SetLabel(parsedData[2])
			self.zAccVal.SetLabel(parsedData[3])
			self.xMagVal.SetLabel(parsedData[4])
			self.yMagVal.SetLabel(parsedData[5])
			self.zMagVal.SetLabel(parsedData[6])
			self.lightVal.SetLabel(parsedData[7])
			self.touchVal.SetLabel(parsedData[8])
			self.adcVal.SetLabel(parsedData[9])
			self.accRateVal.SetLabel(parsedData[10])
			self.magRateVal.SetLabel(parsedData[11])
			self.lightRateVal.SetLabel(parsedData[12])
			self.touchRateVal.SetLabel(parsedData[13])
			self.adcRateVal.SetLabel(parsedData[14])
		
	def onButton(self, event):
		# convert identifier
		serialStr = "@x" + str(self.cmdList.GetCurrentSelection()+1) + "x"
		# convert new sampling rate but make sure it is a float
		try:
			temp = float(self.cmdVal.GetValue())
			# make sure that the sampling rate is at least 0.05 (otherwise too low)
			if temp > 0.06 and temp <= 999:
				# "#" is the end of line character
				if temp < 0.1:
					# print an extra 0
					serialStr = serialStr + "0" + str(int(temp*1000)) + "x#"
				else:
					serialStr = serialStr + str(int(temp*1000)) + "x#"
				print serialStr
				# try a couple times
				for i in range(20):
					self.mbedSerial.ser.write(serialStr)
					time.sleep(0.005)
				self.statusBar.SetStatusText("Sampling...")
			else:
				self.statusBar.SetStatusText("Error: sampling period must be between 0.06 and 999.")
		except ValueError:
			self.statusBar.SetStatusText("Error: sampling period must be a float.")

	def enableAcc(self, event):
		if self.accEn:
			# if enabled, then disable
			serialStr = "@x1xdddx#"
		else:
			# otherwise, enable
			serialStr = "@x1xeeex#"
		print serialStr
		for i in range(20):
			self.mbedSerial.ser.write(serialStr)
			time.sleep(0.005)

	def enableMag(self, event):
		if self.magEn:
			# if enabled, then disable
			serialStr = "@x2xdddx#"
		else:
			# otherwise, enable
			serialStr = "@x2xeeex#"
		print serialStr
		for i in range(20):
			self.mbedSerial.ser.write(serialStr)
			time.sleep(0.005)

	def enableLight(self, event):
		if self.lightEn:
			# if enabled, then disable
			serialStr = "@x3xdddx#"
		else:
			# otherwise, enable
			serialStr = "@x3xeeex#"
		print serialStr	
		for i in range(20):
			self.mbedSerial.ser.write(serialStr)
			time.sleep(0.005)

	def enableTouch(self, event):
		if self.touchEn:
			# if enabled, then disable
			serialStr = "@x4xdddx#"
		else:
			# otherwise, enable
			serialStr = "@x4xeeex#"
		print serialStr		
		for i in range(20):
			self.mbedSerial.ser.write(serialStr)
			time.sleep(0.005)

	def enableADC(self, event):
		if self.touchEn:
			# if enabled, then disable
			serialStr = "@x5xdddx#"
		else:
			# otherwise, enable
			serialStr = "@x5xeeex#"
		print serialStr		
		for i in range(20):
			self.mbedSerial.ser.write(serialStr)
			time.sleep(0.005)
		
	def defineSizers(self):
		self.headSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.headSizer.Add(self.dataLabel, 0, wx.ALL, 5)
		self.headSizer.Add(self.sampLabel, 0, wx.ALL, 5)

		self.accSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.accSizer.Add(self.accText, 0, wx.ALL, 5)
		self.accSizer.Add(self.xAccLabel, 0, wx.ALL, 5)
		self.accSizer.Add(self.xAccVal, 0, wx.ALL, 5)
		self.accSizer.Add(self.yAccLabel, 0, wx.ALL, 5)
		self.accSizer.Add(self.yAccVal, 0, wx.ALL, 5)
		self.accSizer.Add(self.zAccLabel, 0, wx.ALL, 5)
		self.accSizer.Add(self.zAccVal, 0, wx.ALL, 5)
		self.accSizer.Add(self.accRateVal, 0, wx.ALL, 5)
		self.accSizer.Add(self.accButton, 0, wx.ALL, 5)

		self.magSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.magSizer.Add(self.magText, 0, wx.ALL, 5)
		self.magSizer.Add(self.xMagLabel, 0, wx.ALL, 5)
		self.magSizer.Add(self.xMagVal, 0, wx.ALL, 5)
		self.magSizer.Add(self.yMagLabel, 0, wx.ALL, 5)
		self.magSizer.Add(self.yMagVal, 0, wx.ALL, 5)
		self.magSizer.Add(self.zMagLabel, 0, wx.ALL, 5)
		self.magSizer.Add(self.zMagVal, 0, wx.ALL, 5)
		self.magSizer.Add(self.magRateVal, 0, wx.ALL, 5)
		self.magSizer.Add(self.magButton, 0, wx.ALL, 5)

		self.lightSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.lightSizer.Add(self.lightText, 0, wx.ALL, 5)
		self.lightSizer.Add(self.lightVal, 0, wx.ALL, 5)
		self.lightSizer.Add(self.lightRateVal, 0, wx.ALL, 5)
		self.lightSizer.Add(self.lightButton, 0, wx.ALL, 5)
		
		self.touchSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.touchSizer.Add(self.touchText, 0, wx.ALL, 5)
		self.touchSizer.Add(self.touchVal, 0, wx.ALL, 5)
		self.touchSizer.Add(self.touchRateVal, 0, wx.ALL, 5)
		self.touchSizer.Add(self.touchButton, 0, wx.ALL, 5)

		self.adcSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.adcSizer.Add(self.adcText, 0, wx.ALL, 5)
		self.adcSizer.Add(self.adcVal, 0, wx.ALL, 5)
		self.adcSizer.Add(self.adcRateVal, 0, wx.ALL, 5)
		self.adcSizer.Add(self.adcButton, 0, wx.ALL, 5)

		self.cmdSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.cmdSizer.Add(self.cmdLabel, 0, wx.ALL, 5)
		self.cmdSizer.Add(self.cmdList, 0, wx.ALL, 5)
		self.cmdSizer.Add(self.cmdVal, 0, wx.ALL, 5)
		self.cmdSizer.Add(self.cmdButton, 0, wx.ALL, 5)

		self.topSizer = wx.BoxSizer(wx.VERTICAL)
		self.topSizer.Add(self.headSizer)
		self.topSizer.Add(self.accSizer)
		self.topSizer.Add(self.magSizer)
		self.topSizer.Add(self.lightSizer)
		self.topSizer.Add(self.touchSizer)
		self.topSizer.Add(self.adcSizer)
		self.topSizer.Add(self.cmdSizer)

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



