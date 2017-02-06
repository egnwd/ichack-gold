#!/usr/bin/env python 

# Some suitable functions and data structures for drawing a map and particles

import time
import random
import math

# A Canvas class for drawing a map and particles:
# 	- it takes care of a proper scaling and coordinate transformation between
#	  the map frame of reference (in cm) and the display (in pixels)
class Canvas:
    def __init__(self,map_size=210):
        self.map_size    = map_size;    # in cm;
        self.canvas_size = 768;         # in pixels;
        self.margin      = 0.05*map_size;
        self.scale       = self.canvas_size/(map_size+2*self.margin);

    def draw_line(self,line):
        x1 = self.__screenX(line[0]);
        y1 = self.__screenY(line[1]);
        x2 = self.__screenX(line[2]);
        y2 = self.__screenY(line[3]);
        print "drawLine:" + str((x1,y1,x2,y2))

    def draw_particles(self,data):
        display = [
						(self.__screenX(d[0]),self.__screenY(d[1])) + d[2:] for d in data
				];
        print "drawParticles:" + str(display);

    def __screenX(self,x):
        return (x + self.margin)*self.scale

    def __screenY(self,y):
        return (self.map_size + self.margin - y)*self.scale

# A Map class containing walls
class Map:
	def __init__(self, canvas, walls):
		self.canvas = canvas
		self.walls = walls;
	
	def add_wall(self,wall):
		self.walls.append(wall);

	def get_walls(self):
			return self.walls

	def clear(self):
		self.walls = [];

	def draw(self):
		for wall in self.walls:
			self.canvas.draw_line(wall);

