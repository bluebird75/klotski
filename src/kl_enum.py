'''
This fname provides all the constants and enums other files need to share.

Author: Philippe Fremy
License: Gnu GPL (see fname LICENSE)
'''

from typing import Dict, List

from PyQt5.QtGui import qRgb
from PyQt5.QtCore import Qt

VERSION = '1.3'

TILE_SIZE = 32
TRANSP_COLOR= qRgb( 0, 0, 0 )
ID_SPLASH_SCREEN = 0
NAME_SPLASH_SCREEN = 'Splash'

PIX_SIZE = TILE_SIZE // 2
MINI_TILE_SIZE = 4

TILE_FILE_NAME = "klotski-tiles.png"

MSG_ABOUT = """Klotski %s

by Philippe Fremy <phil.fremy@free.fr>
Graphics by Ben Adler <benadler@bigfoot.de

Klotski is the reborn version of a game existing under Windows 3.1 . This is where all the levels are coming from.

Klotski has been written in 2000 in Python with the graphical toolkit Qt. This was my first big program ever written in Python.

For more information about Python, see http://www.python.org
For more information about Qt, see http://www.qt.io.
For more information about PyQt, see https://www.riverbankcomputing.com/software/pyqt/intro
"""  % VERSION

# Piece is used in the map structure
class Piece:
    wall    = '#'
    heart   = '*'
    pieces  = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    s_wall  = '-'
    goal    = '.'
    border  = '@'
    space   = ' '
    none    = 'none'

def is_piece(p: str) -> bool:
    '''Analyse the graphic element described by this string and return True if this is a moveable block'''
    for i in p:
        if not i in Piece.pieces:
            return False
    return True


# Tile is use for drawing only  
class Tile:
    corner      = 0
    hor_edge    = 1
    ver_edge    = 2
    miss_corner = 3
    inner       = 4

    piece       = 0
    m_piece     = 1
    wall        = 2
    s_wall      = 3
    goal        = 4

    space       = 5 # used only for mini tiles color


mini_tile_colors = {
    Tile.piece   : Qt.yellow,
    Tile.m_piece : Qt.red,
    Tile.wall    : Qt.gray,
    Tile.s_wall  : Qt.lightGray,
    Tile.goal    : Qt.darkRed,
    Tile.space   : Qt.black
}   # type: Dict[int, Qt.GlobalColor]

pix_list = [
    "corner",
    "hor_edge",
    "ver_edge",
    "miss_corner",
    "inner"
] # type: List[str]


tile_list = {
    "piece"   : Tile.piece,
    "m_piece" : Tile.m_piece,
    "wall"    : Tile.wall ,
    "s_wall"  : Tile.s_wall,
    "goal"    : Tile.goal
} # type: Dict[str, int]


# Translation between map content and tiles
piece_tile = {
    Piece.heart      : Tile.m_piece,
    Piece.pieces[0] : Tile.piece,
    Piece.wall      : Tile.wall,
    Piece.s_wall    : Tile.s_wall,
    Piece.goal      : Tile.goal,
    Piece.space     : Tile.space
} # type: Dict[str, int]

