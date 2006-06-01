#!/usr/bin/env python

##############################################################################
#                                generate_pix.py
#
# This small script is used to generate a big pixmap from all the tiles in the
# subdirs
#
# Version   : $Id$
# Copyright : (C) 2006 by Philippe Fremy <phil@freehackers.org>
# License   : Gnu GPL (see file LICENSE)
#
#  This program is free software; you can redistribute it and/or modify 
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
##############################################################################


from qt import *
import sys

sys.path.append("../src")
from enum import *

def generate_pix( image, name ):
	pix = QImage();
	xoffset = 0
	yoffset = tile_list[name] * TILE_SIZE
	for p in pix_list:
		pname = name + "/" + p + ".xpm"
		if not pix.load(pname): raise "Unable to load ", pname

		for i in range( TILE_SIZE ):
			for j in range( TILE_SIZE ):
				image.setPixel( xoffset + i,  yoffset + j, pix.pixel( i, j ))

		xoffset = xoffset + TILE_SIZE

	    
result = QImage( TILE_SIZE * len(pix_list), TILE_SIZE * len( tile_list ), 32 );
for t in tile_list.keys():
	print "Generating pixmap for ", t
	generate_pix( result, t ) 

print "../src/" + tile_file_name + " generated!"
result.save( "../src/" + tile_file_name, "PNG" )
	
