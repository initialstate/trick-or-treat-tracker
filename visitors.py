import RPi.GPIO as GPIO
from time import sleep
from ISStreamer.Streamer import Streamer

# Tell the Pi we're going to use it's numbering system
GPIO.setmode(GPIO.BCM)
# Pins that D1 and LED are connected to
PIN=23
BLUE = 17
GREEN = 27
RED = 22

# Specify our motion sensor pin as input
GPIO.setup(PIN,GPIO.IN)
# Specify our LED pins as output
GPIO.setup(RED,GPIO.OUT)
GPIO.output(RED,0)
GPIO.setup(GREEN,GPIO.OUT)
GPIO.output(GREEN,0)
GPIO.setup(BLUE,GPIO.OUT)
GPIO.output(BLUE,0)

# Initial State bucket name (displayed)
BUCKET_NAME = ":jack_o_lantern: Trick or Treat Tracker" 
# Initial State bucket key (hidden)
BUCKET_KEY = "trickortreat"
# Initial State access key
ACCESS_KEY = "Your_Access_Key"

# Variables that ensure we don't stream that there was or wasn't motion twice in a row
# This saves on sent events and processing power
alreadyRecordedMotion = False
alreadyRecordedNoMotion = False
counter = 0

# Initialize the Initial State Streamer
streamer = Streamer(bucket_name=BUCKET_NAME, bucket_key=BUCKET_KEY, access_key=ACCESS_KEY)

# Turn on and set the LED to yellow
GPIO.output(RED,1)
GPIO.output(GREEN,1)

# Loop indefinitely
while True:
	# If the motion sensor pulls high (detects motion):
	if GPIO.input(PIN) == 1:
		print "Motion detected"
		# If we haven't streamed yet:
		if not alreadyRecordedMotion:
			counter = counter + 1
			# Set LED to red
			GPIO.output(RED,1)
			GPIO.output(GREEN,0)
			# Stream to Initial State
			streamer.log(":ghost: or :chocolate_bar:?",":chocolate_bar: Time For Treats!")
			streamer.log(":candy: Hungry Humans? :candy:",counter)
			streamer.flush()
			alreadyRecordedMotion = True
			alreadyRecordedNoMotion = False
		else:
			# Pause the script for 1 second
			sleep(1)
	else:
		print "No motion detected"
		# If we haven't streamed yet:
		if not alreadyRecordedNoMotion:
			# Set LED to yellow
			GPIO.output(RED,1)
			GPIO.output(GREEN,1)
			# Stream to Initial State
			streamer.log(":ghost: or :chocolate_bar:?",":no_pedestrians: No One Around")
			streamer.flush()
			alreadyRecordedNoMotion = True
			alreadyRecordedMotion = False
		else:
			# Pause the script for 1 second
			sleep(1)
