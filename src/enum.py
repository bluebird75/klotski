# vi:set ts=4 sts=0 sw=4:

##############################################################################
#                                enum.py
#
# This file provides all the constants and enums other files need to share.
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
from qt import *

TILE_SIZE = 32
TRANSP_COLOR= qRgb( 0, 0, 0 )

PIX_SIZE= TILE_SIZE / 2
MINI_TILE_SIZE = 4

tile_file_name = "klotski-tiles.png"

# Piece is used in the map structure
class Piece:
	wall 	= '#'
	main 	= '*'
	pieces 	= "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	s_wall 	= '-'
	goal 	= '.'
	border 	= '@'
	space 	= ' '

def is_piece(p):
	for i in p:
		if not i in Piece.pieces: return 0
	return 1

# Tile is use for drawing only	
class Tile:
	corner 	 	= 0
	hor_edge 	= 1
	ver_edge 	= 2
	miss_corner 	= 3
	inner 		= 4

	piece		= 0
	m_piece		= 1
	wall		= 2
	s_wall		= 3
	goal 		= 4

	space		= 5 # used only for mini tiles color

mini_tile_colors = {
		Tile.piece   : Qt.yellow,
		Tile.m_piece : Qt.red,
		Tile.wall    : Qt.gray,
		Tile.s_wall  : Qt.lightGray,
		Tile.goal    : Qt.darkRed,
		Tile.space   : Qt.black
	}



pix_list = [
		"corner",
		"hor_edge",
		"ver_edge",
		"miss_corner",
		"inner"
	   ]

tile_list = {
		"piece"   : Tile.piece,
		"m_piece" : Tile.m_piece,
		"wall"    : Tile.wall ,
		"s_wall"  : Tile.s_wall,
		"goal"    : Tile.goal
            }

# Translation between map content and tiles
piece_tile = {
		Piece.main      : Tile.m_piece,
		Piece.pieces[0] : Tile.piece,
		Piece.wall      : Tile.wall,
		Piece.s_wall    : Tile.s_wall,
		Piece.goal      : Tile.goal,
		Piece.space     : Tile.space 
	    }


