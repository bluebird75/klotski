# vi:set ts=4 sts=0 sw=4:

##############################################################################
#                                map.py
#
# Map is the internal structure used to store the info on the boards.
#
# Version   : $Id$
# Copyright : (C) 2000 by Philippe Fremy <pfremy@chez.com>
# License   : Gnu GPL (see file LICENSE)
#
#  This program is free software; you can redistribute it and/or modify 
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
##############################################################################

import string, copy
from enum import *
#from qt import *

class Map:
	def __init__(self): 
		self.map=[]
		self.goal = []
		self.s_wall = []

		self.name=""
		self.w = -1
		self.h = -1
		self.menu_name = ""
		self.pid_size = 1
		self.orig_map = None

	def __repr__(self):
		return self.print_map( self.map )

	def print_map(self, m):
		r = "Map %s : %d x %d\n" % (self.name, self.w, self.h)
		for row in m:
			r = r + Piece.border
			for i in row:
				r = r + (' '*self.pid_size + i)[-self.pid_size:]
			r = r + Piece.border + '\n'
		return r
		
	def reset( self ):
		self.map = copy.deepcopy( self.orig_map )		

	def pid(self, x,y): 
		if x < 0 or y < 0 : return -1
		if x >= self.w or y >= self.h : return -1
		return self.map[y][x]

	def canMove(self, pid, dx, dy):
		if (abs(dx)+abs(dy) != 1):
			raise Exception("test of illegal move")

		if not (pid == Piece.main or is_piece( pid )):
			return 0

		for x in range(self.w):
			for y in range(self.h):
				if (self.pid(x,y) != pid): continue
				move_id = self.pid(x+dx, y+dy)
				if (move_id == -1): 
					return 0
				if (move_id  == Piece.s_wall 
				    and pid == Piece.main): 
					continue

				if (move_id  == pid or move_id == Piece.space
				    or move_id == Piece.goal):
					continue
				return 0
		return 1

	def move(self, pid, d = None ):
		if not (pid == Piece.main or is_piece( pid )):
			raise Exception(str(pid) + " is not a piece, can not move it")

		if d == None:
			pm = self.possibleMove(pid)
			if (len(pm) == 0):
				raise Exception("No possible move")
			if (len(pm) > 1):
				raise Exception("Too many possible move")
			(dx, dy) = pm[0]
		else :
			dx, dy = d

		#if (abs(dx)+abs(dy) != 1):
		#	raise "illegal move"

		move_map = copy.deepcopy( self.map )
		pid_pos = []
		for x in range(self.w):
			for y in range(self.h):
				if (self.map[y][x] == pid):
					move_map[y][x] = Piece.space 
					pid_pos.append( (x,y) )

		for p in pid_pos:
			move_map[ p[1]+dy ][ p[0]+dx ] = pid
		for p in self.goal:
			if move_map[ p[1] ][ p[0] ] == Piece.space:
				move_map[ p[1] ][ p[0] ] = Piece.goal
		for p in self.s_wall:
			if move_map[ p[1] ][ p[0] ] == Piece.space:
				move_map[ p[1] ][ p[0] ] = Piece.s_wall
					
		self.map = move_map


	def possibleMove(self, pid):
		m = []
		for move in ((1,0),(0,1),(-1,0),(0,-1)):
			if (self.canMove(pid, move[0],move[1])):
				m.append( move )
		return m

	# returns all the tiles belonging to the piece in x,y
	def whole_tile(self, x, y):
		pid = self.pid(x, y)
		to_be_tested = [ (x,y) ]
		tested = {}
		while( len(to_be_tested) ):
			x,y = to_be_tested[-1]
			tested[(x,y)] = 0
			to_be_tested[-1:] = []

			# find adjacent tile of the same piece
			adj = []
			for d in [ (0,1), (1,0), (-1,0), (0,-1) ]:
				if self.pid(x+d[0], y+d[1]) == pid: 
					adj.append( (x+d[0], y+d[1] ) )

			for d in adj:	
				# Add d to to_be_tested list if d is not in tested
				# and if d is not in to_be_tested
				if not tested.has_key( d ):
					try:
						to_be_tested.index( d )
					except:
						to_be_tested.append( d )
		return tested.keys()

		

	def remove_doublon(self):
		def generate_new_pid( pid, pid_dict):
			while(1):
				if pid_dict.has_key( pid ):
					pid = pid + pid[0]
				else: 
					return pid

		self.pid_size = 1
		pid_dict = {}
		new_map = copy.deepcopy( self.map )

		for y in range(self.h):
			for x in range(self.w):
				pid = self.pid(x,y)
				if not is_piece(pid): continue

				if pid_dict.has_key( pid ):
					new_pid = generate_new_pid( pid, pid_dict ) 
					self.pid_size = max( self.pid_size, len( new_pid ))
				else:
					# pid_dict does not already contain pid
					new_pid = pid

				pid_dict[ new_pid ] = 0
				l = self.whole_tile(x,y)
				for t in l:
					tx, ty = t
					new_map[ty][tx] = new_pid
					self.map[ty][tx] = Piece.s_wall

		self.map = new_map
				
		

	def check(self, line):
		try:
			if (len(self.name) == 0):
				raise Exception("No name for level")

			if (len(self.map) != self.h):
				raise Exception("Map '%s' (line %d) has an inconsistent height %d." % (self.name, line, len(self.map) ))
			for row in self.map:
				if (len(row) != self.w):
					raise Exception( "Map '%s' (line %d) has a line with inconsistent width %d.\nMap was supposed to be of width %d" % (self.name, line, len(row), self.w ) )

			s = reduce( lambda x,y:x+y, self.map )
			s = reduce( lambda x,y:x+y, s )
			if -1 == string.find( s, Piece.main ) and self.name != "Icon":
				raise Exception( "Map %s has no main piece" % self.name )

			if -1 == string.find( s, Piece.goal ) and self.name != "Icon":
				raise Exception( "Map %s has no goal" % self.name )
		except:
			# XXX remove when dialog ok
			print self
			raise

	def game_over(self):
		for p in self.goal:
			if self.pid(p[0], p[1]) != Piece.main:
				return 0
		return 1

	def load(self, line, name):
		self.h = len( self.map )
		self.w = len( self.map[0] )
		self.name = name
		self.check(line)
		self.remove_doublon()

		self.goal = []
		self.s_wall = []
		for y in range(self.h):
			for x in range(self.w):
				if self.map[y][x] == Piece.goal : 
					self.goal.append( (x,y) )
				if self.map[y][x] == Piece.s_wall: 
					self.s_wall.append( (x,y) )

		self.orig_map = copy.deepcopy( self.map )

	


# returns a dict of map
def load_maps( file ):
	f = open(file)

	level_by_id = {}
	intro = 0
	map = Map()
	filling_map=0
	map_nb = -1
	line = 0
	map_line = 0
	map_name = ''
	

	for l in f.readlines():
		line = line + 1
		l = string.strip( l[:-1] )
		if (not len(l)): continue

		if (l[0] == Piece.border and (string.rfind(l,Piece.border) != string.find(l,Piece.border))):
			if (intro == 0): continue
			filling_map = 1
			map.map.append( list(l[1:string.rfind(l,Piece.border)]))
			continue

		if (intro and filling_map):
			map_nb = map_nb + 1
			map.load( map_line, map_name )
			level_by_id[map_nb] = map
			map = Map()
			filling_map=0
			intro = 0
			map_name = ''

		if (l[0] == '<' and l[-1] == '>'):
			intro = 1
			map_name = l[1:-1]
			filling_map=0
			map_line = line
			continue
		
	if (filling_map and intro):
		map_nb = map_nb + 1
		map.load( map_line, map_name)
		level_by_id[map_nb] = map
		
	f.close()
	return level_by_id



