from __future__ import print_function
import RPi.GPIO as GPIO
import time
from dual_mc33926_rpi import motors, MAX_SPEED

# Set up sequences of motor speeds.
test_forward_speeds = list(range(0, MAX_SPEED, 1)) + \
  [MAX_SPEED] * 200 + list(range(MAX_SPEED, 0, -1)) + [0]  

test_reverse_speeds = list(range(0, -MAX_SPEED, -1)) + \
  [-MAX_SPEED] * 200 + list(range(-MAX_SPEED, 0, 1)) + [0]  

try:
    motors.enable()
    motors.setSpeeds(0, 0)
    encoder = 0
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(2, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    motors.motor1.setSpeed(MAX_SPEED//4)
    while True:
        GPIO.wait_for_edge(2, GPIO.RISING)	
        encoder = encoder + 1
	#print(encoder)
	if encoder == 1500:
            print("turned 1 rev")
            break
            motors.motor1.setSpeed(-MAX_SPEED//4)
            encoder = 0
    	
    #print("Motor 1 forward")
    #for s in test_forward_speeds:
        #motors.motor1.setSpeed(s)
        #time.sleep(0.005)

    #print("Motor 1 reverse")
    #for s in test_reverse_speeds:
        #motors.motor1.setSpeed(s)
        #time.sleep(0.005)


finally:
  # Stop the motors, even if there is an exception
  # or the user presses Ctrl+C to kill the process.
  motors.setSpeeds(0, 0)
  motors.disable()
