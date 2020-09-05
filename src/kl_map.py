'''
KLMap is the internal structure used to store the info on the boards.

Author: Philippe Fremy
License: Gnu GPL (see fname LICENSE)
'''
from typing import Tuple, Dict, List, Optional
import copy
from functools import reduce

from PyQt5.QtCore import QObject, pyqtSignal

from .kl_enum import *

class KLMap(QObject):

    sig_del_s_wall = pyqtSignal(int, int)

    def __init__(self) -> None:
        QObject.__init__(self)
        self.xymap  = [] # type: List[ List[str] ]
        self.goal   = [] # type: List[ Tuple[int,int] ]
        self.s_wall = [] # type: List[ Tuple[int, int] ]

        self.name = ""
        self.w = -1
        self.h = -1
        self.menu_name = ""
        self.pid_size = 1
        self.orig_xymap = [] # type: List[ List[str] ]


    def __repr__(self) -> str:
        return self.to_string(self.xymap)


    def to_string(self, m: List[List[str]]) -> str:
        r = "xymap %s : %d x %d\n" % (self.name, self.w, self.h)
        for row in m:
            r = r + Piece.border
            for i in row:
                r = r + (' '*self.pid_size + i)[-self.pid_size:]
            r = r + Piece.border + '\n'
        return r


    def reset( self ) -> None:
        '''Reset the current xymap to its original value'''
        self.xymap = copy.deepcopy( self.orig_xymap )


    def pid(self, x:int, y:int) -> str:
        '''Return the piece id located at x,y'''
        if x < 0 or y < 0 :
            return Piece.none
        if x >= self.w or y >= self.h :
            return Piece.none
        return self.xymap[y][x]


    def canMove(self, pid:str, dx:int, dy:int) -> bool:
        if abs(dx)+abs(dy) != 1:
            raise ValueError("test of illegal move")

        if not (pid == Piece.heart or is_piece( pid )):
            return False

        for x in range(self.w):
            for y in range(self.h):
                if self.pid(x, y) != pid:
                    continue
                move_id = self.pid(x+dx, y+dy)

                # moving outside the board is forbidden
                if move_id == Piece.none:
                    return False

                # moving through the door is ok for the heart piece
                if move_id == Piece.s_wall and pid == Piece.heart:
                    continue

                # moving onto oneself is ok
                # moving into space is ok
                # moving into final goal is ok
                if (move_id == pid
                        or move_id == Piece.space
                        or move_id == Piece.goal):
                    continue

                # all other cases (moving onto other pieces) are forbidden
                return False

        return True


    def move_piece(self, pid: str, deltaxy: Optional[Tuple[int, int]] = None) -> None:
        '''Move the piece pid by delta_x, delta_y wrapped in deltaxy

        If deltaxy is None, check of all possible moves and only move if one actual move is possible, else raises an exception.
        '''
        if not (pid == Piece.heart or is_piece( pid )):
            raise Exception(str(pid) + " is not a piece, can not move it")

        if deltaxy is None:
            pm = self.possibleMove(pid)
            if (len(pm) == 0):
                raise Exception("No possible move")
            if (len(pm) > 1):
                raise Exception("Too many possible move")
            (dx, dy) = pm[0]
        else :
            dx, dy = deltaxy

        move_xymap = copy.deepcopy( self.xymap )
        pid_pos = []
        for x in range(self.w):
            for y in range(self.h):
                if (self.xymap[y][x] == pid):
                    move_xymap[y][x] = Piece.space
                    pid_pos.append( (x,y) )

        for p in pid_pos:
            move_xymap[ p[1]+dy ][ p[0]+dx ] = pid
        for p in self.goal:
            if move_xymap[ p[1] ][ p[0] ] == Piece.space:
                move_xymap[ p[1] ][ p[0] ] = Piece.goal

        to_be_del_idx = []
        for i in range(len(self.s_wall)):
            p = self.s_wall[i]
            if move_xymap[ p[1] ][ p[0] ] == Piece.space:
                move_xymap[ p[1] ][ p[0] ] = Piece.s_wall
            elif move_xymap[ p[1] ][ p[0] ] == Piece.heart:
                # no longer a s_wall
                to_be_del_idx.append( i )

        to_be_del_idx.reverse()
        for i in to_be_del_idx:
            self.sig_del_s_wall.emit( *self.s_wall[i] )
            del self.s_wall[i]
                    
        self.xymap = move_xymap


    def possibleMove(self, pid: str) -> List[Tuple[int, int]]:
        '''Return the list of allowed moves for a given piece'''
        m = [] # type: List[ Tuple[int,int] ]
        for move in ((1,0),(0,1),(-1,0),(0,-1)):
            if (self.canMove(pid, move[0],move[1])):
                m.append( move )
        return m

    def whole_tile(self, x: int, y: int) -> List[Tuple[int, int]]:
        '''returns all the tiles belonging to the piece in x,y'''
        pid = self.pid(x, y)
        to_be_tested = [ (x,y) ]
        tested = {} # type: Dict[Tuple[int, int], int]
        while( len(to_be_tested) ):
            x,y = to_be_tested[-1]
            tested[(x,y)] = 0
            to_be_tested[-1:] = []

            # find adjacent tile of the same piece
            adj = [] # type: List[ Tuple[int, int]]
            for delta in [ (0,1), (1,0), (-1,0), (0,-1) ]:
                if self.pid(x+delta[0], y+delta[1]) == pid:
                    adj.append( (x+delta[0], y+delta[1] ) )

            for delta in adj:
                # Add d to to_be_tested list if d is not in tested
                # and if d is not in to_be_tested
                if delta not in tested:
                    if not delta in to_be_tested:
                        to_be_tested.append(delta)
        return list(tested.keys())

        
    def remove_doublon(self) -> None:
        def generate_new_pid(frompid: str) -> str:
            '''Generates a new identifier string which is not already defined in pid_dict'''
            while(1):
                if frompid in pid_dict:
                    frompid = frompid + pid[0]
                else: 
                    return frompid

        self.pid_size = 1
        pid_dict = {}   # type: Dict[str, int]
        new_xymap = copy.deepcopy( self.xymap )

        for y in range(self.h):
            for x in range(self.w):
                pid = self.pid(x,y)
                if not is_piece(pid):
                    continue

                if pid in pid_dict:
                    new_pid = generate_new_pid( pid )
                    self.pid_size = max( self.pid_size, len( new_pid ))
                else:
                    # pid_dict does not already contain pid
                    new_pid = pid

                pid_dict[ new_pid ] = 0
                l = self.whole_tile(x,y)
                for t in l:
                    tx, ty = t
                    new_xymap[ty][tx] = new_pid
                    # mark the piece as a wall to avoid reprocessing it
                    self.xymap[ty][tx] = Piece.s_wall

        self.xymap = new_xymap


    def check(self, line_no: int) -> None:
        '''Check the general consistency of the current map.

        Raises an exception in case of inconsistency.

        Normally, all maps are correctly defined, exceptions should only be raised during
        development of new maps.
        '''
        try:
            if (len(self.name) == 0):
                raise ValueError("No name for level")

            if (len(self.xymap) != self.h):
                raise AssertionError("xymap '%s' (line %d) has an inconsistent height %d." % (self.name, line_no, len(self.xymap) ))
            for row in self.xymap:
                if (len(row) != self.w):
                    raise AssertionError( "xymap '%s' (line %d) has a line with inconsistent width %d.\nKLMap was supposed to be of width %d" % (self.name, line_no, len(row), self.w ) )

            l = reduce( lambda x,y:x+y, self.xymap )
            s = reduce( lambda x,y:x+y, l, '' )
            if -1 == s.find( Piece.heart ) and self.name != "Icon":
                raise ValueError( "xymap %s has no heart piece" % self.name )

            if -1 == s.find( Piece.goal ) and self.name != "Icon":
                raise ValueError( "xymap %s has no goal" % self.name )
        except (ValueError, AssertionError):
            print(self)
            raise


    def is_game_won(self) -> bool:
        '''Return True if the game is won'''
        for p in self.goal:
            if self.pid(p[0], p[1]) != Piece.heart:
                return False
        return True


    def loadline(self, line_nb: int, name: str) -> None:
        '''Fill the current xymap with one more line of data'''
        self.h = len( self.xymap )
        self.w = len( self.xymap[0] )
        self.name = name
        self.check(line_nb)
        self.remove_doublon()

        self.goal = []
        self.s_wall = []
        for y in range(self.h):
            for x in range(self.w):
                if self.xymap[y][x] == Piece.goal :
                    self.goal.append( (x,y) )
                if self.xymap[y][x] == Piece.s_wall:
                    self.s_wall.append( (x,y) )

        self.orig_xymap = copy.deepcopy( self.xymap )

    
def load_maps(fname: str) -> Dict[int, KLMap]:
    '''Parses the file name to build a dictionnary of map id to KLMap objects'''
    f = open(fname)
    level_by_id = {} # type: Dict[int, KLMap]
    intro = False
    klmap = KLMap()
    filling_map = False
    map_nb = -1
    line_nb = 0
    map_line_nb = 0
    map_name = ''
    
    for l in f.readlines():
        line_nb = line_nb + 1
        l = l[:-1].strip()
        if (not len(l)):
            continue

        if (l[0] == Piece.border and (l.rfind(Piece.border) != l.find(Piece.border))):
            if not intro:
                continue
            filling_map = True
            klmap.xymap.append( list(l[1:l.rfind(Piece.border)]))
            continue

        if intro and filling_map:
            map_nb = map_nb + 1
            klmap.loadline(map_line_nb, map_name)
            level_by_id[map_nb] = klmap
            klmap = KLMap()
            filling_map = False
            intro = False
            map_name = ''

        if (l[0] == '<' and l[-1] == '>'):
            intro = True
            map_name = l[1:-1]
            filling_map = True
            map_line_nb = line_nb
            continue
        
    if filling_map and intro:
        map_nb = map_nb + 1
        klmap.loadline(map_line_nb, map_name)
        level_by_id[map_nb] = klmap
        
    f.close()
    return level_by_id



