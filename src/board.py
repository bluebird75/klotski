# vi:set ts=4 sts=0 sw=4:

##############################################################################
#                                board.py
#
# This file provides all the functions and classes to handle painting
# graphics and moving things: qcanvasitem generation, minimap generation, 
# moves, ...
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


import math
from enum import *
from map import Map
from qt import *

# workaround for the fact that QCAnvasSprite doesn't store a ref to 
# the QPixmapArray
global_qcpa = []

# computes cos(angle(a,b)) = scalar(a,b) / ( abs(a) * abs(b) )
def cos( a, b ) : 
	scal = a[0]*b[0] + a[1]*b[1]
	na = math.sqrt( a[0]**2 + a[1]**2 )
	nb = math.sqrt( b[0]**2 + b[1]**2 )
	return float(scal) / ( na * nb )

#class Board (QWidget):
class Board (QCanvasView):
	def __init__(self, cnv, parent):
		#QWidget.__init__(self, parent)
		QCanvasView.__init__(self, None, parent)
		self.map = []
		#self.viewport().setBackgroundColor( Qt.darkRed)
		self.canvas_item_dict = {}
		self.m_canvas = None

		self.draging = 0
		self.clicking = 0
		self.drag_piece = 0
		self.drag_x = -1 
		self.drag_y = -1
		self.drag_timer = QTimer( self )
		QObject.connect( self.drag_timer, SIGNAL("timeout()"), self.set_draging )

	pix_tiles = None
	tiles_mask = None

	def load_tiles(self):
		img_tile = QImage( tile_file_name );
		#img_tile = img_tile.convertDepth( 16 )

		w = img_tile.width()
		h = img_tile.height()
		assert w != 0 and h != 0, "%s gives a null image" % fname 

		# Build mask
		img_mask = QImage( w, h, 1, 2, QImage.LittleEndian )
		#img_mask.fill(1)
		for x in range(w):
			for y in range(h):
				#print "pixel : ", img_tile.pixel(x,y)
				if (img_tile.pixel(x,y) == TRANSP_COLOR):
					img_mask.setPixel( x, y, 0 )
					#print "Setting transp color"
				else:
					img_mask.setPixel( x, y, 1 )

		Board.tiles_mask = QBitmap()
		if not Board.tiles_mask.convertFromImage( img_mask, QPixmap.MonoOnly | QPixmap.ThresholdDither | QPixmap.AvoidDither ) :
			print "Could not convert to Bitmap !"
			
		Board.pix_tiles = QPixmap() 
		if not Board.pix_tiles.convertFromImage( img_tile ):
			print "Could not convert to Pixmap !"
		#Board.pix_tiles.setMask( pix_mask )

		

	# Generate a QPixmap representing the map (to be used as an icon)
	def generate_mini_map(self, m):
		pm = QPixmap( MINI_TILE_SIZE * (m.w + 2)-1, MINI_TILE_SIZE * (m.h + 2)-1)
		pm.fill( mini_tile_colors[ Tile.space ] )
		p = QPainter( pm )

		# draw border
		color = QBrush(mini_tile_colors[ piece_tile[Piece.wall]] )
		p.fillRect(0,0,MINI_TILE_SIZE*(m.w+2), MINI_TILE_SIZE-1, color )
		p.fillRect(0,0,MINI_TILE_SIZE-1, MINI_TILE_SIZE*(m.h+2), color )
		p.fillRect(0,MINI_TILE_SIZE*(m.h+1),MINI_TILE_SIZE*(m.w+2), MINI_TILE_SIZE-1 , color )
		p.fillRect(MINI_TILE_SIZE*(m.w+1),0,MINI_TILE_SIZE-1,MINI_TILE_SIZE*(m.h+2), color )

		# draw content
		p.translate(MINI_TILE_SIZE, MINI_TILE_SIZE)
		for y in range( m.h ):
			for x in range( m.w ):
				pid = m.pid( x, y )
				if is_piece(pid):
					color = QColor( mini_tile_colors[ piece_tile[Piece.pieces[0]] ] )
				else:
					color = QColor( mini_tile_colors[ piece_tile[pid] ] )
				p.fillRect( x * MINI_TILE_SIZE, y * MINI_TILE_SIZE, MINI_TILE_SIZE-1 , MINI_TILE_SIZE-1 , QBrush(color) )

				rpid = m.pid( x+1, y)
				rdpid = m.pid( x+1, y+1)
				dpid = m.pid( x, y+1)

				#pid = -2
				p.setPen( color )
				if rpid == pid:
					p.drawLine( (x+1)*MINI_TILE_SIZE-1, y*MINI_TILE_SIZE, (x+1)*MINI_TILE_SIZE-1 , (y+1)*MINI_TILE_SIZE-2 )
				if dpid == pid:
					p.drawLine( x*MINI_TILE_SIZE, (y+1)*MINI_TILE_SIZE-1, (x+1)*MINI_TILE_SIZE -2 , (y+1)*MINI_TILE_SIZE-1 )
				if rdpid == pid:
					p.drawPoint( (x+1)*MINI_TILE_SIZE -1 , (y+1)*MINI_TILE_SIZE-1 )

		p.end()
		return pm
				



	# Generate a QCavas object from a map and fills up the
	# canvas_item_dict
	def generate_canvas(self, m):
		global global_qcpa

		new_canvas = QCanvas(m.w * TILE_SIZE, m.h * TILE_SIZE)	
		self.setCanvas( new_canvas )
		# Deletes the QCanvasItem
		del self.canvas_item_dict
		# Delete the old QCanvas
		del self.m_canvas	
		# Deletes the QCanvasPixmapArray
		del global_qcpa[:]
		self.m_canvas = new_canvas
		self.canvas_item_dict = {}

		# Generate a QCanvasSprite from a QPixmap object
		def pixmap_to_sprite(pix, cnv) :

			return qs

		#  set the background color <=> fill
		#self.m_canvas.setBackgroundColor( Qt.darkRed)
		self.m_canvas.setBackgroundColor( Qt.black)

		pix = QPixmap( TILE_SIZE, TILE_SIZE )
		mask = QBitmap( TILE_SIZE, TILE_SIZE )

		for x in range( m.w ):
			for y in range( m.h ):
				pid = m.pid(x, y) 
				if pid == Piece.space : continue 

				self.set_tile_pix( pix, mask, x, y )
				qcpa = QCanvasPixmapArray( [ pix ], [ QPoint(0,0) ] )
				# If we don't hold a ref to the pixmaparray, it will get
				# destroyed
				global_qcpa.append( qcpa )

				cs = QCanvasSprite( qcpa, self.m_canvas )
				cs.setX( x * TILE_SIZE )
				cs.setY( y * TILE_SIZE )

				# moving tiles are above walls, special walls
				# and goals
				if (pid == Piece.goal or pid == Piece.wall
				   or pid == Piece.s_wall):
					cs.setZ( 1 )
				else: cs.setZ( 10 )


				if not self.canvas_item_dict.has_key( pid ):
					self.canvas_item_dict[pid] = []
				self.canvas_item_dict[pid].append( cs )

				cs.show()

	def set_map(self,m): 
		self.map = m
		#self.setFixedSize( self.map.w * TILE_SIZE, self.map.h * TILE_SIZE )
		self.generate_canvas(m)
		self.setMaximumSize( self.sizeHint() )
		self.update()

	# Draw the tile located at (x,y) on the painter p	
	def set_tile_pix(self, pix, mask, x, y):

		pid = self.map.pid(x,y)
		piece_type = pid
		if is_piece( piece_type ) :
			piece_type = Piece.pieces[0]


		offset_list = [ (0,0), (PIX_SIZE, 0), (PIX_SIZE, PIX_SIZE), (0, PIX_SIZE) ]					

		# Value assiociated with each neighbour
		#
		#   2 | 1  1 | 2 
		#   -----  ----- 
		#   4 | XXXX | 4 
		#       XXXX
		#   4 | XXXX | 4 
		#   -----  ----- 
		#   2 | 1  1 | 2
		#
		# (x, y, val)
		neighbour_val_list = [ [ (0, -1, 1), (-1, -1, 2), (-1, 0, 4) ],
		                       [ (0, -1, 1), ( 1, -1, 2), ( 1, 0, 4) ],
		                       [ (0,  1, 1), ( 1,  1, 2), ( 1, 0, 4) ],
		                       [ (0,  1, 1), (-1,  1, 2), (-1, 0, 4) ] ]


		# which pixmap to choose according to the value of the
		#	neighbours
		which_quarter= { 0 : Tile.corner,
				 1 : Tile.ver_edge,
				 2 : Tile.corner,
				 3 : Tile.ver_edge,
				 4 : Tile.hor_edge,
				 5 : Tile.miss_corner,
				 6 : Tile.hor_edge,
				 7 : Tile.inner }


		p = QPainter( pix )
		pm = QPainter( mask )
		for i in range(4):
			offset = offset_list[i]
			neighbour_val = neighbour_val_list[i]

			pix_nb = 0
			for neigh in neighbour_val:
				if (pid == self.map.pid(x + neigh[0], 
						y + neigh[1])):
					pix_nb = pix_nb + neigh[2]
		
			quarter_nb = which_quarter[ pix_nb ]

			p.drawPixmap( offset[0], offset[1],
				Board.pix_tiles,
				quarter_nb * TILE_SIZE + offset[0], piece_tile[piece_type] * TILE_SIZE + offset[1],
				PIX_SIZE, PIX_SIZE )

			pm.drawPixmap( offset[0], offset[1],
				Board.tiles_mask,
				quarter_nb * TILE_SIZE + offset[0], piece_tile[piece_type] * TILE_SIZE + offset[1],
				PIX_SIZE, PIX_SIZE )

		p.end()
		pm.end()
		pix.setMask( mask )


	def move( self, pid, d ):
		dx, dy = d
		sz = len(self.canvas_item_dict[pid])
		if (sz < 3): incr = 1
		elif sz < 8: incr = 2
		elif sz < 16: incr = 4
		elif sz < 32: incr = 8
		else : incr = 16
		
		for i in range( TILE_SIZE/incr ):
			for cs in self.canvas_item_dict[pid]:
				cs.moveBy( float( dx*incr ), float( dy*incr ) )
			self.m_canvas.update()

		incr = TILE_SIZE % incr
		if incr :
			for cs in self.canvas_item_dict[pid]:
				cs.moveBy( float( dx*incr ), float( dy*incr ) )
			self.m_canvas.update()
			

	def contentsMousePressEvent(self, e):
		pid = self.map.pid( e.x() / TILE_SIZE, e.y() / TILE_SIZE )
		if len( self.map.possibleMove( pid ) ) == 0:
			return


		self.clicking = 1
		self.draging = 0
		self.drag_pid = pid
		self.drag_x = e.x() / TILE_SIZE
		self.drag_y = e.y() / TILE_SIZE
		self.drag_timer.start( 500, 1)

	def set_draging(self):
		assert self.clicking, "timer expired while not clicking!!!"
		self.draging = 1

	def contentsMouseReleaseEvent(self, e):
		if not self.clicking: return
	
		pm = self.map.possibleMove(self.drag_pid)
		if len(pm) == 0: 
			self.drag_timer.stop()
			self.clicking = 0
			return

		# tile was clicked
		if not self.draging:
			self.drag_timer.stop()
			if len(pm) == 1:
				self.emit( PYSIGNAL("move()"), (self.drag_pid, pm[0]) )
			self.clicking = 0
			return

		# tile was dragged
		self.drag_timer.stop()
		self.clicking = 0
		self.draging = 0

	def contentsMouseMoveEvent(self, e):
		if not self.clicking : 
			
			return

		dx = e.x() / TILE_SIZE - self.drag_x
		dy = e.y() / TILE_SIZE - self.drag_y
		d = dx, dy
		if d == (0,0): return

		pm = self.map.possibleMove(self.drag_pid)

		# computes the cos of the angle between d and the possible move
		l = map( lambda d,m : (cos(d,m), m), [d] * len(pm), pm )

		# keeps only moves in almost the same direction (cos > 0)
		l = filter( lambda x : x[0] > 0, l )
		l.sort()
		l.reverse()
		rpm = map( lambda x : x[1], l )

		if len(rpm) > 0:
			self.emit( PYSIGNAL("move()"), (self.drag_pid, rpm[0]) )
			self.draging = 1
			self.drag_x = self.drag_x + rpm[0][0]
			self.drag_y = self.drag_y + rpm[0][1]


