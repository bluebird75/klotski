'''
This is the main file providing the application, the main window and a few
widget.

Author: Philippe Fremy
License: Gnu GPL (see fname LICENSE)
'''

from typing import Optional, Dict, List, Tuple
import sys

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QLCDNumber, QApplication, \
							QMessageBox, QMenu, QHBoxLayout, QWidget, QSizePolicy
from PyQt5.QtGui import QIcon, QPixmap

from kl_enum import *
from kl_map import load_maps
from kl_board import KLMap, KLBoard
from kl_board_chooser import KLBoardChooser, KlMinimapProvider

def reverse_move( d: Tuple[int, int] ) -> Tuple[int, int]:
	return ( -d[0], -d[1] )

class Klotski (QMainWindow):
	def __init__(self, maps: Dict[int, KLMap], firstBoard: Optional[int] = None) -> None:
		QMainWindow.__init__(self)
		self.klmap = None	# type: Optional[KLMap]
		self.moves = 0
		self.move_list = []	# type: List[ Tuple[str, Tuple[int, int]]]
		self.move_index = -1 
		self.mini_maps_dict = {} # type: Dict[int, QPixmap]
		self.levels_by_id = maps
			
		self.init_misc_gui()

		self.board.load_tiles()
		self.board.sig_move.connect( self.move_tile )

		self.generate_mini_maps()

		self.board_chooser = KLBoardChooser(KlMinimapProvider(self.levels_by_id, self.mini_maps_dict), self)
		self.board_chooser.hide()

		# needs self.board
		self.init_menu()

		self.setWindowTitle( "Klotski" )
		self.setWindowIcon( QIcon(QPixmap( "klotski-icon.png" ) ))
		self.title_label.setText( "Klotski" )
		if firstBoard:
			self.new_level( self.levels_by_id[int(firstBoard)] )
			self.move_enabled = True
		else:
			self.new_level( self.levels_by_id[ID_SPLASH_SCREEN] )
			self.move_enabled = False

	def init_misc_gui(self) -> None:
		w = QWidget( self )
		self.setCentralWidget(w)
		ly = QVBoxLayout()
		w.setLayout( ly )
		ly.setSpacing( 10 )

		self.title_label = QLabel( "Klotski", w )
		ft = self.title_label.font()
		ft.setPointSize( 20 )
		self.title_label.setFont( ft )
		self.title_label.setAlignment( Qt.AlignCenter )
		self.title_label.setSizePolicy( QSizePolicy( QSizePolicy.Expanding,
			QSizePolicy.Fixed) )
		ly.addWidget(self.title_label)

		hb = QHBoxLayout()
		self.board = KLBoard(w)
		hb.addWidget(self.board)
		hb.setStretchFactor( self.board, 100 )
		ly.addLayout(hb)

		# horizontal bottom hbox [ QLabel | QLcdNumber ]
		hb = QHBoxLayout()
		#hb.setSpacing( 5 )
		# hb.setMargin( 5 )
		ml = QLabel("Moves : ", w)
		ml.setFont( ft )
		ml.setAlignment( Qt.AlignRight )
		hb.addWidget( ml )

		self.move_lcd_nb = QLCDNumber(4, w )
		self.move_lcd_nb.adjustSize()
		self.move_lcd_nb.setFixedSize( self.move_lcd_nb.width(), 30 )
		hb.addWidget(self.move_lcd_nb)
		# hb.setFixedHeight( hb.height() )
		ly.addLayout(hb)

		self.adjustSize()

	def generate_mini_maps(self) -> None:
		self.mini_maps_dict = {}
		for i in self.levels_by_id.keys():
			self.mini_maps_dict[i] = self.board.generate_mini_map( self.levels_by_id[i] )
		
	def new_level(self, m: KLMap) -> None:
		'''Display a new map into the main window'''
		if m.name != NAME_SPLASH_SCREEN:
			# display the name of the board
			self.setWindowTitle( "Klotski - " + m.name )
			self.title_label.setText( m.name )
		else:
			# display the splash screen
			self.setWindowTitle( "Klotski" )
			self.title_label.setText('')

		self.klmap = m
		w = max( m.w*TILE_SIZE+10 + 40, self.title_label.sizeHint().width() + 20 )
		h = m.h*TILE_SIZE+10 + 80 + self.title_label.sizeHint().height() + max( self.move_lcd_nb.sizeHint().height(), self.title_label.sizeHint().height())

		center = self.frameGeometry().center()
		self.resize( w, h )

		r = self.frameGeometry()
		r.moveCenter( center )

		desktop = QApplication.desktop()
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

	def choose_board(self) -> None:
		self.board_chooser.exec()
		board_id = self.board_chooser.result()

		if board_id in self.levels_by_id:
			self.new_level( self.levels_by_id[board_id] )

	def init_menu(self) -> None:
		file_menu = QMenu('Game', self)
		file_menu.addAction( "Boards", self.choose_board, Qt.CTRL + Qt.Key_B )
		file_menu.addAction( "Quit", self.close, Qt.CTRL + Qt.Key_X )
		file_menu.addAction( "About Klotski", self.about)

		move_menu = QMenu('Moves', self)
		move_menu.addAction( "Reset", self.reset )
		move_menu.addAction( "Undo", self.undo, Qt.CTRL + Qt.Key_U )
		move_menu.addAction( "Redo", self.redo, Qt.CTRL + Qt.Key_R )

		main_menu = self.menuBar()
		main_menu.addMenu( file_menu )
		main_menu.addMenu( move_menu )
                                       
	def set_move_nb(self, m: int) -> None:
		self.move_lcd_nb.display( m )
		self.moves = m

	def move_tile(self, move_info: Tuple[str, Tuple[int, int]]) -> None:
		pid, delta = move_info
		if not self.move_enabled: return

		assert self.klmap
		self.klmap.move_piece( pid, delta )
		self.board.move_piece( pid, delta )

		if self.move_index < 0:
			self.move_list = [ (pid, (0,0)) ]
			self.move_index = 0
			self.set_move_nb( self.moves + 1 )

		last_move_pid, last_move = self.move_list[ self.move_index ]

		if (pid != last_move_pid):
			self.move_index = self.move_index + 1
			self.move_list[ self.move_index: ] = [(pid, delta)]
			self.set_move_nb( self.moves + 1 )
		else :
			self.move_list[self.move_index:] = [ (pid, ( last_move[0] + delta[0], last_move[1] + delta[1]) )]

		if self.klmap.is_game_won():
			QMessageBox.information( self, "Congratulation",
			"Congratulations!!!\nYou completed this level in %d moves" % self.moves )
			self.move_enabled = False
			self.klmap.reset()

	def reset(self) -> None:
		assert self.klmap
		self.klmap.reset()
		self.board.set_map( self.klmap )
		self.set_move_nb(0) 
		self.move_enabled = True
		self.move_list = []
		self.move_index = -1

	def undo(self) -> None:
		if self.move_index < 0: return
		if not self.move_enabled: return

		pid = self.move_list[ self.move_index ][0]
		d = reverse_move( self.move_list[self.move_index][1] )
		assert self.klmap
		assert self.board
		self.klmap.move_piece( pid, d )
		self.board.move_piece( pid, d )
		self.set_move_nb( self.moves - 1 )

		self.move_index = self.move_index - 1

	def redo( self ) -> None:
		if self.move_index+1 >= len( self.move_list ):
			return
		if not self.move_enabled: return

		self.move_index = self.move_index + 1
		pid, d = self.move_list[ self.move_index ] 
		assert self.klmap
		assert self.board
		self.klmap.move_piece( pid, d )
		self.board.move_piece( pid, d )
		self.set_move_nb( self.moves + 1 )
		

	def about(self) -> None:
		QMessageBox.about(self, 'About Klotski', MSG_ABOUT )

	def print_state( self ) -> None:
		print(self.klmap)
		print("Move list : ", self.move_list)
		print("move list index : ", self.move_index)


def main() -> None:
	a = QApplication( sys.argv )
	maps = load_maps( "boards.kts" )

	firstBoard = None
	if len(sys.argv)>1: 
		firstBoardName = sys.argv[1]
		for m in maps.keys():
			if maps[m].name == firstBoardName:
				firstBoard = m
				break
		else:
			print("No such map: ", firstBoardName)
			print('Map List:')
			for m in maps:
				print(maps[m].name)

	klotski = Klotski(maps, firstBoard)
	klotski.show()
	a.exec()
	del klotski


if __name__ == '__main__':
	main()

# vi:set ts=4 sts=0 sw=4:
