import serial

print "init arduino coms"
ser = serial.Serial()
ser.baudrate = 9600
ser.port = 2
ser.timeout = 1

try:
	ser.open()
except serial.SerialException:
	print "serial open exception"

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
		s = ser.read(1)
		return s
	except serial.SerialException:
		print "serial read exception"
		return "";

