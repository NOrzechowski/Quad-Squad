from __future__ import print_function
import time
import curses



import RPi.GPIO as GPIO
from board_four import motors as motor_4, MAX_SPEED
from board_three import motors as motor_3
from board_two import motors as motor_2
from board_one import motors as motor_1

# Set up sequences of motor speeds.
test_forward_speeds = list(range(0, MAX_SPEED, 1)) + \
  [MAX_SPEED] * 200 + list(range(MAX_SPEED, 0, -1)) + [0]  

test_reverse_speeds = list(range(0, -MAX_SPEED, -1)) + \
  [-MAX_SPEED] * 200 + list(range(-MAX_SPEED, 0, 1)) + [0]  

# initialize curses:
stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(1)

# needed for situating leg
slow_forward = MAX_SPEED//12
slow_reverse = -slow_forward

# print prompt to user:
stdscr.addstr(0,10, "hit 'q' to exit")
stdscr.refresh()

try:
    # turn all other motors off:
    motors_1.enable()
    motors_1.setSpeeds(0, 0) 
    motors_2.enable()
    motors_2.setSpeeds(0, 0)
    motors_3.enable()
    motors_3.setSpeeds(0, 0)
    
    # setup motors
    motors_4.enable()
    motors_4.motor1.disable()

    motors_4.setSpeeds(0,0)
    
    encoder_m2 = 8
    encoder_m1 = 7

    # Setup GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(encoder_m1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(encoder_m2, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    # now loop on user input: 
    key = ''
    while key != ord('q'):
        key = stdscr.getch()
        stdscr.addch(20, 25, key)
        stdscr.refresh()
        if key == curses.KEY_UP:
	    stdscr.addstr(2,20, "forward")
   	    encoder = 0
            motor_4.motor2.enable()
            motor_4.motor2.setSpeed(slow_forward)
    	    while True:
                GPIO.wait_for_edge(encoder_m1, GPIO.RISING)	
                encoder = encoder + 1
	        if encoder == 10:
    	    	    encoder = 0
	            break
        elif key == curses.KEY_DOWN:
            stdscr.addstr(3,20, "backward")
   	    encoder = 0
     	    motor_4.motor2.enable()
            motor_4.motor2.setSpeed(slow_reverse)
    	    while True:
                GPIO.wait_for_edge(encoder_m2, GPIO.RISING)	
                encoder = encoder + 1
	        if encoder == 10:
    	    	    encoder = 0
	            break
    	motor_4.setSpeeds(0,0)
        motor_4.disable()
    motor_4.setSpeeds(0,0)
    motor_4.disable()
finally:
  # Stop the motors, even if there is an exception
  # or the user presses Ctrl+C to kill the process.
  motor_4.setSpeeds(0, 0)
  motor_4.disable()
