import serial

print "init arduino coms"
ser = serial.Serial()
ser.baudrate = 9600
ser.port = 2
ser.timeout = 1

ser.open()

door_open = False

def write(msg):
	try:
		ser.write(bytes(msg))
		ser.flush()
	except serial.SerialException:
		print "serial write exception"
		return False

	return True

def read():
	try:
		s = ser.read()
		return s
	except serial.SerialException:
		print "serial read exception"
		return "";