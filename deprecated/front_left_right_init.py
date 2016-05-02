from __future__ import print_function
import time
import curses
import RPi.GPIO as GPIO
from board_four import motors as motors_4, MAX_SPEED
from board_three import motors as motors_3
from board_two import motors as motors_2
from board_one import motors as motors_1
class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
getch = _GetchUnix()

# initialize curses:

# needed for situating leg
slow_forward = MAX_SPEED
slow_reverse = -slow_forward

# print prompt to user:

try:
   
    # turn all other motors off:
    motors_4.disable()
    motors_4.setSpeeds(0, 0) 
    motors_1.disable()
    motors_1.setSpeeds(0, 0)
    motors_3.disable()
    motors_3.setSpeeds(0, 0)
    
    # setup motors
    motors_2.enable()
    motors_2.motor1.disable()
    
    
    motors_2.setSpeeds(0,0)
    
    motors_2.motor2.enable()
    motors_2.motor2.setSpeed(0)
    
    encoder_m2 = 4
    encoder_m1 = 3

    # Setup GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(encoder_m1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(encoder_m2, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    #GPIO.add_event_detect(encoder_m2, GPIO.RISING)

    # now loop on user input: 
    key = ''
    while key == '' or ord(key) != ord('q'):
	key = getch()
        if ord(key) == ord('a'):
   	    #print("forward")
	    encoder = 0
            motors_2.motor2.enable()
            motors_2.motor2.setSpeed(slow_forward)
    	    while True:
                #print("encoder: ", encoder)
		GPIO.wait_for_edge(encoder_m2, GPIO.RISING)
                encoder = encoder + 1
	        if encoder == 10:
    	    	    encoder = 0
	            break
        elif ord(key) == ord('d'):
   	    #print("backward")
            encoder = 0
     	    motors_2.motor2.enable()
            motors_2.motor2.setSpeed(slow_reverse)
    	    while True:
		GPIO.wait_for_edge(encoder_m2, GPIO.RISING)
                encoder = encoder + 1
	        if encoder == 10:
    	    	    encoder = 0
	            break
	motors_2.motor2.disable();
    GPIO.cleanup()
    motors_2.setSpeeds(0,0)
    motors_2.disable()
finally:
  # Stop the motors, even if there is an exception
  # or the user presses Ctrl+C to kill the process.
  GPIO.cleanup()
  motors_2.setSpeeds(0, 0)
  motors_2.disable()


