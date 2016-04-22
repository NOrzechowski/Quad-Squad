from __future__ import print_function
import time
import RPi.GPIO as GPIO
from board_three import motors, MAX_SPEED


# Set up sequences of motor speeds.
test_forward_speeds = list(range(0, MAX_SPEED, 1)) + \
  [MAX_SPEED] * 200 + list(range(MAX_SPEED, 0, -1)) + [0]  

test_reverse_speeds = list(range(0, -MAX_SPEED, -1)) + \
  [-MAX_SPEED] * 200 + list(range(-MAX_SPEED, 0, 1)) + [0]  

try:
    motors.enable()
    motors.setSpeeds(0, 0)
    
    encoder_m1 = 5
    encoder_m2 = 6

   
    # MOTOR 1 TEST
    encoder = 0
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(encoder_m1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(encoder_m2, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    motors.motor1.setSpeed(MAX_SPEED//4)
    while True:
        GPIO.wait_for_edge(encoder_m1, GPIO.RISING)	
        encoder = encoder + 1
	#print(encoder)
	if encoder == 1500:
            print("motor 1 turned 1 rev forward")
    	    encoder = 0
	    break
    encoder = 0
    motors.motor1.setSpeed(-MAX_SPEED//4)
    while True:
        GPIO.wait_for_edge(encoder_m1, GPIO.RISING)	
        encoder = encoder + 1
	#print(encoder)
	if encoder == 1500:
            print("motor 1 turned 1 rev backward")
   	    encoder = 0
	    break
    motors.motor1.disable()
    time.sleep(1)    
    # MOTOR 2 TEST
    encoder = 0
    motors.motor2.setSpeed(MAX_SPEED//4)
    while True:
        GPIO.wait_for_edge(encoder_m2, GPIO.RISING)	
        encoder = encoder + 1
	#print(encoder)
	if encoder == 1500:
            print("motor 2 turned 1 rev forward")
   	    encoder = 0
	    break
    encoder = 0
    motors.motor2.setSpeed(-MAX_SPEED//4)
    while True:
        GPIO.wait_for_edge(encoder_m2, GPIO.RISING)	
        encoder = encoder + 1
	#print(encoder)
	if encoder == 1500:
            print("motor 2 turned 1 rev backward")
   	    encoder = 0
	    break



finally:
  # Stop the motors, even if there is an exception
  # or the user presses Ctrl+C to kill the process.
  motors.setSpeeds(0, 0)
  motors.disable()
