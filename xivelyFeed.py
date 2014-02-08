from threading import Thread
import xively
import datetime
import sys
import time

# global variables
dataPoints = []

# Xively Keys and IDs
XIVELY_API_KEY = "HFD9auwFRR7TlTkbCQvqwUoSIZVzYaxYigY0CvDzCcSdGEAs"
XIVELY_FEED_ID = 663606315

api = xively.XivelyAPIClient(XIVELY_API_KEY)
feed = api.feeds.get(XIVELY_FEED_ID)

def sendData():
	global dataPoints
	global feed
	
	while True:
		print len(dataPoints)
		
		datastream = feed.datastreams
		xAccStream = datastream[0]
		yAccStream = datastream[4]
		zAccStream = datastream[6]
		xMagStream = datastream[2]
		yMagStream = datastream[5]
		zMagStream = datastream[7]
		xLightStream = datastream[1]
		xTouchStream = datastream[3]

		xAccData = []
		yAccData = []
		zAccData = []
		xMagData = []
		yMagData = []
		zMagData = []
		xLightData = []
		xTouchData = []

		# create data to send
		for dp in dataPoints:
			xAccData.append(xively.Datapoint(dp[0], dp[1]))
			yAccData.append(xively.Datapoint(dp[0], dp[2]))
			zAccData.append(xively.Datapoint(dp[0], dp[3]))
			xMagData.append(xively.Datapoint(dp[0], dp[4]))
			yMagData.append(xively.Datapoint(dp[0], dp[5]))
			zMagData.append(xively.Datapoint(dp[0], dp[6]))
			xLightData.append(xively.Datapoint(dp[0], dp[7]))
			xTouchData.append(xively.Datapoint(dp[0], dp[8]))
			
		xAccStream.datapoints = xAccData
		yAccStream.datapoints = yAccData
		zAccStream.datapoints = zAccData
		xMagStream.datapoints = xMagData
		yMagStream.datapoints = yMagData
		zMagStream.datapoints = zMagData
		xLightStream.datapoints = xLightData
		xTouchStream.datapoints = xTouchData

		# push data to xively feed
		feed.update()

		# reset dataPoints array
		dataPoints = []

		time.sleep(1.0)


class XivelyFeed(object):
	
	dataPoints = []
	def __init__(self):
		# start thread
		Thread(target = sendData).start()

	def collectData(self, dp):
		global dataPoints
		# dp is a list of sensor data and time from one time point
		dataPoints.append(dp)
		#print len(self.dataPoints)

