import RPi.GPIO as GPIO
import time
import subprocess

ERROR = 0
GOOD = 1
NOT_DONE = 2

print('Starting up moment-ble-trigger-programmer')
GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)

load_cmd1 = ("sudo openocd -f nrf51-ocd.cfg").split()

debug1 = open("debug.log","w")

def isFixtureDone(fixtureNum):
	file = ""
	rtn = NOT_DONE
	if fixtureNum == 1:
		file = debug1
	elif fixtureNum ==2:
		file = debug2
	else:
		file = debug3
	lines = debug1.readlines()
	for i, line in enumerate(lines):
		if "Error" in line:
			print("got an error in debug file")
			rtn= ERROR
			break
		elif "Verified OK" in line:
			print("Process Succeeded!")
			rtn =  GOOD
			break
#	if rtn == NOT_DONE:
#		print("Didn't find success or error, so probably still chugging")
	return rtn
while True:
	pin1 = GPIO.input(18)
	pin2 = GPIO.input(19)
	pin3 = GPIO.input(20)
	if pin1 == False and last1 == True:
		print('Loading To Fixture 1')
		openocd1 = subprocess.Popen(load_cmd1, stdout = debug1)
		time.sleep(.2)
	last1 = pin1
	last2 = pin2
	last3 = pin3
