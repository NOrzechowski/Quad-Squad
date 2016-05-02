from __future__ import print_function
import time
import curses
import RPi.GPIO as GPIO
from board_four import motors as motors_4, MAX_SPEED
from board_three import motors as motors_3
from board_two import motors as motors_2
from board_one import motors as motors_1

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
	    stdscr.refresh()
   	    encoder = 0
            motors_4.motor2.enable()
            motors_4.motor2.setSpeed(slow_forward)
    	    while True:
                GPIO.wait_for_edge(encoder_m1, GPIO.RISING)	
                encoder = encoder + 1
	        if encoder == 10:
    	    	    encoder = 0
	            break
        elif key == curses.KEY_DOWN:
            stdscr.addstr(3,20, "backward")
	    stdscr.refresh()
   	    encoder = 0
     	    motors_4.motor2.enable()
            motors_4.motor2.setSpeed(slow_reverse)
    	    while True:
                GPIO.wait_for_edge(encoder_m2, GPIO.RISING)	
                encoder = encoder + 1
	        if encoder == 10:
    	    	    encoder = 0
	            break
    	motors_4.setSpeeds(0,0)
        motors_4.disable()
    curses.endwin()
    motors_4.setSpeeds(0,0)
    motors_4.disable()
finally:
  # Stop the motors, even if there is an exception
  # or the user presses Ctrl+C to kill the process.
  curses.endwin()
  motors_4.setSpeeds(0, 0)
  motors_4.disable()
