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
slow_forward = MAX_SPEED//2
try:
    motors_4.disable()
    motors_4.setSpeeds(0, 0) 
    motors_2.disable()
    motors_2.setSpeeds(0, 0)
    motors_3.disable()
    motors_3.setSpeeds(0, 0)
    # setup motors
    motors_1.enable()
    motors_1.motor2.disable()
    motors_1.setSpeeds(0,0)
    motors_1.motor1.enable()
    motors_1.motor1.setSpeed(0)
    encoder_m2 = 2
    encoder_m1 = 14
    # Setup GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(encoder_m1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(encoder_m2, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    key = ''
    while key == '' or ord(key) != ord('q'):
        key = getch()
        if ord(key) == ord('a'):
	    encoder = 0
            motors_1.motor1.enable()
            motors_1.motor1.setSpeed(slow_forward)
    	    while True:
                GPIO.wait_for_edge(encoder_m1, GPIO.RISING)
                encoder = encoder + 1
	        if encoder == 10:
    	    	    encoder = 0
	            break
        elif ord(key) == ord('d'):
            encoder = 0
     	    motors_1.motor1.enable()
            motors_1.motor1.setSpeed(slow_reverse)
    	    while True:
		GPIO.wait_for_edge(encoder_m1, GPIO.RISING)
                encoder = encoder + 1
	        if encoder == 10:
    	    	    encoder = 0
	            break
        elif ord(key) == ord('z'):
            encoder = 0
     	    motors_1.motor2.enable()
            motors_1.motor2.setSpeed(slow_reverse)
    	    while True:
		GPIO.wait_for_edge(encoder_m2, GPIO.RISING)
                encoder = encoder + 1
	        if encoder == 10:
    	    	    encoder = 0
	            break
        elif ord(key) == ord('c'):
            encoder = 0
     	    motors_1.motor2.enable()
            motors_1.motor2.setSpeed(slow_forward)
    	    while True:
		GPIO.wait_for_edge(encoder_m2, GPIO.RISING)
                encoder = encoder + 1
	        if encoder == 10:
    	    	    encoder = 0
	            break
        motors_1.motor1.disable();
        motors_1.motor2.disable();
    GPIO.cleanup()
    motors_1.setSpeeds(0,0)
    motors_1.disable()
finally:
  # Stop the motors, even if there is an exception
  # or the user presses Ctrl+C to kill the process.
  GPIO.cleanup()
  motors_1.setSpeeds(0, 0)
  motors_1.disable()
