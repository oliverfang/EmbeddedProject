from threading import Thread
import time
import serial

receivedSerial = ''
def receiveSerial(ser):
    global receivedSerial
    buffer = ''
    time.sleep(0.05);
    while True:
        buffer = buffer + ser.read(ser.inWaiting())
        if '\n' in buffer:
            lines = buffer.split('\n') # Guaranteed to have at least 2 entries
            receivedSerial = lines[-2]
            #If the Arduino sends lots of empty lines, you'll lose the
            #last filled line, so you could make the above statement conditional
            #like so: if lines[-2]: last_received = lines[-2]
            buffer = lines[-1]

class SerialData(object):
    def __init__(self, init=50):
        try:
            self.ser = ser = serial.Serial(
                port='/dev/tty.usbmodem412',
                baudrate=9600,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=0.1,                                
                xonxoff=0,
                rtscts=0,
                interCharTimeout=None
            )
        except serial.serialutil.SerialException:
            #no serial connection
            self.ser = None
        else:
            Thread(target=receiveSerial, args=(self.ser,)).start()
        
    def next(self):
        if not self.ser:
        	# return random bogus data so we can test if mbed is connected or not
            return 100 
        # try a couple times to return a float if there is actual data
        for i in range(40):
            raw_line = receivedSerial
            try:
		        return raw_line.strip()
            except ValueError:
                print 'bogus data',raw_line
                time.sleep(.005)
        return 0.

    def __del__(self):
        if self.ser:
            self.ser.close()

#if __name__=='__main__':
#    s = SerialData()
#    while True:
#        time.sleep(0.05)
#        print s.next()