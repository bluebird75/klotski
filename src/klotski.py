#!/usr/bin/env python

##############################################################################
#                                klotski.py
#
# This is the main file providing the application, the main window and a few
# widget.
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

import sys

import have_pyqt

from enum import *
from map import Map, load_maps
from board import Board

def reverse_move( d ):
	return ( -d[0], -d[1] )


class BoardChooser (QDialog) :

	def __init__(self, level_dict, mini_maps_dict, parent):
		QDialog.__init__( self, parent , "board_chooser_dialog", 1)

		assert len(mini_maps_dict) > 0, "minimap board dict is empty!"
		assert len(level_dict) > 0, "level dict is empty!"

		ly = QVBoxLayout( self )
		self.iv = QIconView( self )
		ly.addWidget( self.iv, 1 )

		self.iv.setArrangement( QIconView.LeftToRight )
		self.iv.setResizeMode( QIconView.Adjust )
		self.iv.setAutoArrange( 1 )
		self.iv.setSorting( 1 )

		id_list = level_dict.keys()
		id_list.sort()
		for id in id_list:
			m = level_dict[id]
			if (m.name == "Splash"): continue
			item = QIconViewItem( self.iv, m.name, mini_maps_dict[id] )
			item.setKey( "%04d" % id )
		
		QObject.connect( self.iv, SIGNAL("clicked(QIconViewItem*)"), self.mini_map_selected )
		self.resize( 500, 500  )

	def mini_map_selected(self, item):
		if not item: return
		id = int(str(item.key()))
		self.done( id + 1)


class Klotski (QMainWindow):
	def __init__(self, maps):
		QMainWindow.__init__(self, None, "Klotski")
		self.map = None
		self.moves = 0
		self.move_list = []
		self.move_index = -1 
		self.mini_maps_dict = {}
		self.levels_by_id = maps
			

		# construcst self.board
		self.init_misc_gui()

		self.board.load_tiles()
		QObject.connect( self.board, PYSIGNAL("move()"), self.move_tile )

		# should be run _ater_ creation of board object
		self.generate_mini_maps()

		self.board_chooser = BoardChooser( self.levels_by_id, self.mini_maps_dict, self )
		#self.board_chooser.hide()

		# needs self.board
		self.init_menu()

		self.new_level( self.levels_by_id[0] )
		self.setCaption( "Klotski" )
		self.setIcon( QPixmap( "klotski-icon.png" ) ) 
		self.title_label.setText( "Klotski" )
		self.move_enabled = 0

	### needs board object to be already created
	def init_misc_gui(self):
		self.setCaption( "Klotski" )
		w = QWidget( self )
		self.setCentralWidget( w )

		self.title_label = QLabel( "Klotski", w )
		ft = self.title_label.font()
		ft.setPointSize( 20 )
		self.title_label.setFont( ft )
		self.title_label.adjustSize()
		self.title_label.setAlignment( Qt.AlignCenter )

		self.board = Board(None, w)

		ml = QLabel("Moves : ", w)
		ml.setFont( ft )
		ml.setAlignment( Qt.AlignRight )
		ml.adjustSize()

		self.move_lcd_nb = QLCDNumber(4, w )
		self.move_lcd_nb.adjustSize()
		self.move_lcd_nb.setFixedSize( self.move_lcd_nb.width(), 30 )

		#self.setCentralWidget( self.board )
		ly = QVBoxLayout( w )
		ly.addSpacing( 10 )
		ly.addWidget( self.title_label, 2 )
		ly.addSpacing( 10 )
		ly.addWidget( self.board, 10 )
		ly.addSpacing( 10 )
		ly.addStretch( 1 )

		hly = QHBoxLayout()
		ly.addLayout( hly, 1 )
		hly.addStretch( 10 );
		hly.addWidget( ml )
		hly.addWidget( self.move_lcd_nb )
		hly.addSpacing( 30 )
		
		ly.addSpacing( 10 )
		ly.activate()

	def generate_mini_maps(self):
		self.mini_maps_dict = {}
		for i in self.levels_by_id.keys():
			self.mini_maps_dict[i] = self.board.generate_mini_map( self.levels_by_id[i] )
		


	def choose_board(self):
		self.board_chooser.show()
		id = self.board_chooser.result() - 1
		if id < 0: return

		if self.levels_by_id.has_key(id):
			self.new_level( self.levels_by_id[id] )

	def init_menu(self):
		file_menu = QPopupMenu(self)
		file_menu.insertItem( "Boards", self.choose_board, Qt.CTRL + Qt.Key_B )
		file_menu.insertItem( "Quit", self.quit, Qt.CTRL + Qt.Key_X )

		help_menu = QPopupMenu(self)
		help_menu.insertItem( "About Klotski", self.about)
		help_menu.insertItem( "About Python", self.aboutPython)
		help_menu.insertItem( "About Qt", self.aboutQt)

		move_menu = QPopupMenu(self)
		move_menu.insertItem( "Reset", self.reset )
		move_menu.insertItem( "Undo", self.undo, Qt.CTRL + Qt.Key_U )
		move_menu.insertItem( "Redo", self.redo, Qt.CTRL + Qt.Key_R )

		main_menu = QMenuBar(self, "Menubar")
		main_menu.insertItem( "Game", file_menu )
		main_menu.insertItem( "Moves", move_menu )
		main_menu.insertItem( "About", help_menu )
                                       
	def set_move_nb(self, m):
		self.move_lcd_nb.display( m )
		self.moves = m

	def new_level(self, m):
		self.setCaption( "Klotski - " + m.name )
		self.title_label.setText( m.name )

		self.map = m
		w = max( m.w*TILE_SIZE+10 + 40, self.title_label.sizeHint().width() + 20 )
		h = m.h*TILE_SIZE+10 + 80 + self.title_label.sizeHint().height() + max( self.move_lcd_nb.sizeHint().height(), self.title_label.sizeHint().height())

		center = self.frameGeometry().center()
		#print
		#print "old size : ", self.width(), self.height()
		self.resize( w, h )
		#print "new size : ", self.width(), self.height()
		#print "new size : ", w, h

		r = self.frameGeometry()
		#print "coords frame geom: ", r.x(), " x ", r.y(), r.width(), " x ", r.height()
		#print "coords geom : ", self.geometry().x(), " x ", self.geometry().y(),
		#print self.geometry().width(), " x ", self.geometry().height()
		#print "coords frame : ", self.frameSize().width(), self.frameSize().height()
		r.moveCenter( center )
		#print "after moving : coords frame geom: ", r.x(), " x ", r.y(), r.width(), " x ", r.height()

		desktop = qApp.desktop()
		if (r.x() + w > desktop.width() 
			or r.x() < 0
		    or r.y() + h > desktop.height() 
		    or r.y() < 0):

			r.moveCenter( desktop.rect().center() )

		if (r.x() < 0): r.setX( 0 )
		if (r.y() < 0): r.setY( 0 )
		if (r.x() + w > desktop.width()):  
			r.setX( 0 )
			w = desktop.width()-20 - r.x()
		if (r.y() + h > desktop.height()): 
			r.setY( 0 )
			h = desktop.height()-20 - r.y()

		self.move( r.topLeft() )
		self.resize( w, h )

		self.reset()

	def move_tile(self, pid, d):
		if not self.move_enabled: return

		self.map.move( pid, d )
		self.board.move( pid, d )

		if self.move_index < 0:
			self.move_list = [ (pid, (0,0)) ]
			self.move_index = 0
			self.set_move_nb( self.moves + 1 )

		last_move_pid, last_move = self.move_list[ self.move_index ]

		if (pid != last_move_pid):
			self.move_index = self.move_index + 1
			self.move_list[ self.move_index: ] = [(pid, d)]
			self.set_move_nb( self.moves + 1 )
		else :
			self.move_list[self.move_index:] = [ (pid, ( last_move[0] + d[0], last_move[1] + d[1]) )]

		if self.map.game_over():
			QMessageBox.information( self, "Congratulation",
			"Congratulations!!!\nYou completed this level in %d moves" % self.moves )
			self.move_enabled = 0
			self.map.reset()

	def reset(self):
		self.map.reset()
		self.board.set_map( self.map )
		self.set_move_nb(0) 
		self.move_enabled = 1
		self.move_list = []
		self.move_index = -1

	def undo(self):
		if self.move_index < 0: return
		if not self.move_enabled: return

		pid = self.move_list[ self.move_index ][0]
		d = reverse_move( self.move_list[self.move_index][1] )
		self.map.move( pid, d )
		self.board.move( pid, d )
		self.set_move_nb( self.moves - 1 )

		self.move_index = self.move_index - 1

	def redo( self ):
		if self.move_index+1 >= len( self.move_list ):
			return
		if not self.move_enabled: return

		self.move_index = self.move_index + 1
		pid, d = self.move_list[ self.move_index ] 
		self.map.move( pid, d )
		self.board.move( pid, d )
		self.set_move_nb( self.moves + 1 )
		

	def quit(self): qApp.quit()

	def about(self):
	    QMessageBox.about(self, 'About Klotski',
		"""Klotski	     by Philippe Fremy <pfremy@chez.com>
Graphics by Ben Adler <benadler@bigfoot.de

Klotski is the computer superseed of a small game known (in french) 
as 'Ane rouge'. This game did also exist under Windows 3.1 under the name
of Klotski.

Klotski has been written in Python with PyQt. See 'About Python' for details.
""")

	def aboutPython(self):
		mb = QMessageBox(self)
		mb.setCaption('About Python')
		#mb.setTextFormat( Qt.RichText )
		mb.setText( \
"""Klotski is written in Python, a nice and powerful programming language. 
See <a href="http://www.python.org">www.python.org</a> for more information about Python.

This game uses PyQt, the Python bindings for Qt, developed by Phil Thompson. 
For more information about PyQt, see <a href="http://www.thekompany.com/projects/pykde">www.thekompany.com/projects/pykde</a> .
""")
		mb.show()


	def aboutQt(self):
		QMessageBox.aboutQt(self, 'About Qt')

	def print_state( self ):
		print self.map
		print "Move list : ", self.move_list
		print "move list index : ", self.move_index
 

def main():
	print "Building qapp..."
	a = QApplication( sys.argv )
	print "done."

	print "loading maps...",
	try:
		maps = load_maps( "boards.kts" )
	except:
		#raise
		# oops, something went wrong
		QMessageBox.critical( None , "Klotski - error", "An error occured while loading the maps:\n\n" + str(sys.exc_info()[1]) )
		print "failed!"
		sys.exit(1)
	print "done."

	print "Building Klotski...",
	klotski = Klotski(maps)
	print "done."

	a.setMainWidget( klotski )
	a.connect(a, SIGNAL('lastWindowClosed()'), a, SLOT('quit()'))
	klotski.show()
	a.exec_loop()
	del klotski


if __name__ == '__main__': main()

# vi:set ts=4 sts=0 sw=4:
