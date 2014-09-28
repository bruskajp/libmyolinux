#!/usr/bin/env python

#Example game using input from Thalmic Myo

import pygame
import random
import sys
import os
import tempfile
import subprocess
import thread
import socket
import struct

from sys import stdin

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)
BLUE = (0, 0, 255)

PI = 3.1415

#---Main Program Loop---
def game():
    POSES = {
    0 : "rest",
    1 : "fist",
    2 : "waveIn",
    3 : "waveOut",
    4 : "fingersSpread",
    5 : "reserved1",
    6 : "thumbToPinky",
    }

    # initialize socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 6970))
    sock.listen(1)
    conn, addr = sock.accept()



    global last_pose
    pygame.init()

    size = (700, 500)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Myo Linux Driver Demo")


    x_coord = 0
    y_coord = 0
    height = 50
    width = 50

    x_speed = 0
    y_speed = 0
    out_speed = 0
    
    done = False
    pressed = False

    clock = pygame.time.Clock()

    while not done:
        try:
            while 1:
                data = struct.unpack("fffffffBB", conn.recv(30))
                motion = POSES.get(data[7], 'unknown')
                if not data: break
                print motion
                if motion == "rest":
                    print "!!!"
		
		for event in pygame.event.get():
		    if event.type == pygame.QUIT:
			done = True
		    # User pressed down on a key
		    if event.type == pygame.KEYDOWN:
			# Change Position
			if event.key == pygame.K_LEFT:
			    x_speed = -3
			if event.key == pygame.K_RIGHT:
			    x_speed = 3
			if event.key == pygame.K_UP:
			    y_speed = -3
			if event.key == pygame.K_DOWN:
			    y_speed = 3
			# Change Size
			if event.key == pygame.K_1:
			    out_speed = 3
			if event.key == pygame.K_2:
			    out_speed = -3
		    # User let up on a key
		    if event.type == pygame.KEYUP:
			# If it is an arrow key, reset vector back to zero
			if event.key == pygame.K_LEFT:
			    x_speed = 0
			if event.key == pygame.K_RIGHT:
			    x_speed = 0
			if event.key == pygame.K_UP:
			    y_speed = 0
			if event.key == pygame.K_DOWN:
			    y_speed = 0
			if event.key == pygame.K_1:
			    out_speed = 0
			if event.key == pygame.K_2:
			    out_speed = 0
			    
		#---Drawing code should go here---
	  
		#last_pose = myo.getPose()
		#Clear Screen
		screen.fill(WHITE)
	    
		# Move the object according to the speed vector.
		x_coord += x_speed
		y_coord += y_speed
		height += out_speed
		width += out_speed
		
		pygame.draw.rect(screen, BLUE, [x_coord, y_coord, width, height])
		#update screen
		pygame.display.flip()

		#limit to 60 frames per second
		clock.tick(60)
        except Exception, e:
            pass
        finally:
            conn.close()
            sock.close()




    pygame.quit()

def printstdin():
    POSES = {
    0 : "rest",
    1 : "fist",
    2 : "waveIn",
    3 : "waveOut",
    4 : "fingersSpread",
    5 : "reserved1",
    6 : "thumbToPinky",
    }

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 6970))
    sock.listen(1)
    conn, addr = sock.accept()

    try:
        while 1:
            data = struct.unpack("fffffffBB", conn.recv(30))
            motion = POSES.get(data[7], 'unknown')
            if not data: break
            print motion
    except Exception, e:
        pass
    finally:
        conn.close()
        sock.close()

def main():
    game() 

if __name__ == "__main__":
    main()
