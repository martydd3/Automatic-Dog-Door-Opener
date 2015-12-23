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
		print "serial write: " + bytes(msg)
		ser.write(bytes(msg))
		ser.flush()
		print "serial written"
	except serial.SerialException:
		print "serial write exception"
		return False

	return True

def read():
	try:
		print "serial read"
		s = ser.read()
		print "read: " + s
		return s
	except serial.SerialException:
		print "serial read exception"
		return "";