import RPi.GPIO as GPIO
import time
import subprocess
import sys
import select

ERROR = 0
GOOD = 1
NOT_DONE = 2

print('Starting up moment-ble-trigger-programmer')
GPIO.setmode(GPIO.BCM)

#Set up the listener pins so that they have pull-ups. To trigger the fixture we just need to disconnect the pin from Ground and then connect it again
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)

last1 = False
loading_to_fixture = "global"
loading_to_fixture = False

load_cmd1 = ("sudo openocd -f nrf51-ocd.cfg").split()
num_program_tries = 0
openocd1 = "global"

debug1 = open("debug1.log","w+")

def isFixtureDone(fixtureNum):
	file = ""
	rtn = NOT_DONE
	if fixtureNum == 1:
		file = debug1
	elif fixtureNum ==2:
		file = debug2
	else:
		file = debug3
	debug1.seek(0)#This brings us to the start of the file when we read it. Very important!
	lines = debug1.readlines()#read the lines from the first fixture pin. This needs to be made smarter if we want extra programmer lines
        
        #print("printing lines")
        #print(lines)
	for i, line in enumerate(lines):
                #print(line)
		if "Error" in line:
			print("got an error in debug file")
			rtn= ERROR
		elif "Verified OK" in line:
			print("Process Succeeded!")
			rtn =  GOOD
##	if rtn == NOT_DONE:
##		print("Didn't find success or error, so probably still chugging")
	return rtn

#listens for an enter key press
def heardEnter():
        i,o,e = select.select([sys.stdin],[],[],0.0001)
        for s in i:
                if s==sys.stdin:
                        input = sys.stdin.readline()
                        return True
        return False
#load that code
def loadCode():
        print('Loading To Fixture 1')
        debug1.truncate(0)#clear out the log file
        openocd1 = subprocess.Popen(load_cmd1, stdout = debug1, stderr = debug1)
        time.sleep(2)#let the programmer run for a while  before we try to read the log
        loading_to_fixture = True
        num_program_tries = 0
        
while True:
	pin1 = GPIO.input(18)
	pin2 = GPIO.input(19)
	pin3 = GPIO.input(20)

	if loading_to_fixture == True:
                time.sleep(.5) #Check the file only periodically
                result =  isFixtureDone(1)
                if result == GOOD: #if we loaded successfully then we're G2G
                        print("\n ******  fixture is GOOD!   ****")
                        loading_to_fixture = False
                elif result == ERROR: #If we got an error, then try again
                        print("Attempt failed, will try again")
                        if num_program_tries < 2:
                                num_program_tries = num_program_tries +1
                                loadCode()
                        else: #if we just keep failing, abort the load for this DUT
                                num_program_tries = 0
                                loading_to_fixture = False
                                print("\n ***** THIS UNIT CANNOT BE PROGRAMMED :(  *****")
        # Check if the status on the programmer pin has changed. If so then start the programming
        #an enter key press can also trigger it now
	if (pin1 == False and last1 == True) or heardEnter() :
		loadCode()
		loading_to_fixture = True
	last1 = pin1
	last2 = pin2
	last3 = pin3
