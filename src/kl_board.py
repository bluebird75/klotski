'''
This file provides all the functions and classes to handle painting
graphics and moving things: qcanvasitem generation, minimap generation,
moves, ...

Author: Philippe Fremy
License: Gnu GPL (see fname LICENSE)
'''
from typing import Optional, Tuple, List, Dict
import math, pathlib

from PyQt5.QtWidgets import QSizePolicy, QFrame, QGraphicsScene, QGraphicsView, QWidget, QGraphicsPixmapItem
from PyQt5.QtGui import QImage, QBitmap, QPixmap, QPainter, QBrush, QColor, QMouseEvent
from PyQt5.QtCore import QTimer, pyqtSignal, Qt

from .kl_enum import *
from .kl_map import KLMap

def cos( a: Tuple[int, int], b: Tuple[int, int] ) -> float :
    '''computes cos(angle(a,b)) = scalar(a,b) / ( abs(a) * abs(b) )'''
    scal = a[0]*b[0] + a[1]*b[1]
    na = math.sqrt( a[0]**2 + a[1]**2 )
    nb = math.sqrt( b[0]**2 + b[1]**2 )
    return float(scal) / ( na * nb )


class KLBoard(QGraphicsView):

    sig_move = pyqtSignal(tuple)

    def __init__(self, parent: QWidget):
        QGraphicsView.__init__(self, parent)
        self.klmap = KLMap()
        self.setSizePolicy( QSizePolicy( QSizePolicy.Expanding,
            QSizePolicy.Expanding) )
        self.setLineWidth( 2 )
        self.setFrameShape( QFrame.NoFrame )
        self.scene_item_dict = {}   # type: Dict[str, List[QGraphicsPixmapItem]]
        self.m_scene = QGraphicsScene(self)

        self.is_draging = False
        self.is_clicking = False
        self.drag_pid = ''
        self.drag_x = -1
        self.drag_y = -1
        self.drag_timer = QTimer( self )
        self.drag_timer.setSingleShot(True)
        self.drag_timer.timeout.connect( self.set_draging )


    pix_tiles = None    # type: Optional[QPixmap]
    tiles_mask = None   # type: Optional[QBitmap]

    def load_tiles(self) -> None:
        '''Load the tiles representation from the default filename and put the result and the bitmap mask
        in KLBoard.tiles_mask and KLBoard.pix_tiles'''
        img_tile = QImage( str(pathlib.Path(__file__).parent/TILE_FILE_NAME) )

        w = img_tile.width()
        h = img_tile.height()
        assert w != 0 and h != 0, "%s gives a null image" % TILE_FILE_NAME

        # Build mask
        img_mask = QImage( w, h, QImage.Format_Mono )
        for x in range(w):
            for y in range(h):
                if (img_tile.pixel(x,y) == TRANSP_COLOR):
                    img_mask.setPixel( x, y, 0 )
                else:
                    img_mask.setPixel( x, y, 1 )

        KLBoard.tiles_mask = QBitmap()
        if not KLBoard.tiles_mask.convertFromImage(img_mask,
                Qt.ImageConversionFlags(Qt.MonoOnly | Qt.ThresholdDither | Qt.AvoidDither)) :   # type: ignore
            raise Exception("Could not convert to Bitmap !")

        KLBoard.pix_tiles = QPixmap()
        if not KLBoard.pix_tiles.convertFromImage(img_tile):
            raise Exception("Could not convert to Pixmap !")


    def del_s_wall( self, x: int, y: int ) -> None:
        '''Called when a s_wall is hit by the heart piece, to hide it'''
        for cs in self.scene_item_dict[ Piece.s_wall]:
            if cs.x() == x * TILE_SIZE and cs.y() == y * TILE_SIZE:
                cs.setVisible( False )


    def generate_mini_map(self, m: KLMap) -> QPixmap:
        '''Generate a QPixmap representing the map (to be used as an icon)'''
        pm = QPixmap( MINI_TILE_SIZE * (m.w + 2)-1, MINI_TILE_SIZE * (m.h + 2)-1)
        pm.fill( mini_tile_colors[ Tile.space ] )
        p = QPainter( pm )

        # draw border
        brush = QBrush(mini_tile_colors[ piece_tile[Piece.wall]] )
        p.fillRect(0,0,MINI_TILE_SIZE*(m.w+2), MINI_TILE_SIZE-1, brush )
        p.fillRect(0,0,MINI_TILE_SIZE-1, MINI_TILE_SIZE*(m.h+2), brush )
        p.fillRect(0,MINI_TILE_SIZE*(m.h+1),MINI_TILE_SIZE*(m.w+2), MINI_TILE_SIZE-1 , brush )
        p.fillRect(MINI_TILE_SIZE*(m.w+1),0,MINI_TILE_SIZE-1,MINI_TILE_SIZE*(m.h+2), brush )

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

                p.setPen( color )
                if rpid == pid:
                    p.drawLine( (x+1)*MINI_TILE_SIZE-1, y*MINI_TILE_SIZE, (x+1)*MINI_TILE_SIZE-1 , (y+1)*MINI_TILE_SIZE-2 )
                if dpid == pid:
                    p.drawLine( x*MINI_TILE_SIZE, (y+1)*MINI_TILE_SIZE-1, (x+1)*MINI_TILE_SIZE -2 , (y+1)*MINI_TILE_SIZE-1 )
                if rdpid == pid:
                    p.drawPoint( (x+1)*MINI_TILE_SIZE -1 , (y+1)*MINI_TILE_SIZE-1 )

        p.end()
        return pm


    def generate_scene(self, m: KLMap) -> None:
        '''Generate a QGraphicScene object from a map and fills up the scene_item_dict'''
        new_scene = QGraphicsScene(0, 0, m.w * TILE_SIZE, m.h * TILE_SIZE)
        self.setScene( new_scene )
        del self.scene_item_dict
        if self.m_scene:
            del self.m_scene
        self.m_scene = new_scene
        self.scene_item_dict = {}

        #  set the background color <=> fill
        self.m_scene.setBackgroundBrush(Qt.black)

        pix = QPixmap( TILE_SIZE, TILE_SIZE )
        mask = QBitmap( TILE_SIZE, TILE_SIZE )

        for x in range( m.w ):
            for y in range( m.h ):
                pid = m.pid(x, y) 
                if pid == Piece.space:
                    continue

                # We pass the pixmap and bitmap object to avoid recreating them
                # on each function call
                self.set_tile_pix( pix, mask, x, y )
                item = QGraphicsPixmapItem(pix)
                item.setX(x * TILE_SIZE)
                item.setY(y * TILE_SIZE)
                self.m_scene.addItem(item)

                # moving tiles are above walls, special walls
                # and goals
                if (pid == Piece.goal or pid == Piece.wall
                   or pid == Piece.s_wall):
                    item.setZValue(1)
                else:
                    item.setZValue( 10 )

                if not pid in self.scene_item_dict:
                    self.scene_item_dict[pid] = []
                self.scene_item_dict[pid].append(item)

                item.show()


    def set_map(self, m: KLMap) -> None:
        m.sig_del_s_wall.connect(self.del_s_wall)
        self.klmap = m
        self.setFixedSize( self.klmap.w * TILE_SIZE, self.klmap.h * TILE_SIZE )
        self.generate_scene(m)
        self.update()


    def set_tile_pix(self, pix: QPixmap, mask: QBitmap, x: int, y: int) -> None:
        '''Create the pixmap for the part of the piece located at x,y .
        The pixmap is created inside the pix argument'''
        pid = self.klmap.pid(x,y)
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
        # (dx, dy, val)
        neighbour_val_list = [ [ (0, -1, 1), (-1, -1, 2), (-1, 0, 4) ],
                               [ (0, -1, 1), ( 1, -1, 2), ( 1, 0, 4) ],
                               [ (0,  1, 1), ( 1,  1, 2), ( 1, 0, 4) ],
                               [ (0,  1, 1), (-1,  1, 2), (-1, 0, 4) ] ]


        # which pixmap to choose according to the value of the
        #   neighbours
        which_quarter = {
             0 : Tile.corner,
             1 : Tile.ver_edge,
             2 : Tile.corner,
             3 : Tile.ver_edge,
             4 : Tile.hor_edge,
             5 : Tile.miss_corner,
             6 : Tile.hor_edge,
             7 : Tile.inner
        }

        p = QPainter( pix )
        pm = QPainter( mask )
        for i in range(4):
            offset = offset_list[i]
            neighbour_val = neighbour_val_list[i]

            pix_nb = 0
            for neigh in neighbour_val:
                if (pid == self.klmap.pid(x + neigh[0],
                        y + neigh[1])):
                    pix_nb = pix_nb + neigh[2]
        
            quarter_nb = which_quarter[ pix_nb ]

            assert KLBoard.pix_tiles        # to help mypy making sure that tiles_mask is not None
            p.drawPixmap(offset[0], offset[1],
                         KLBoard.pix_tiles,
                         quarter_nb * TILE_SIZE + offset[0], piece_tile[piece_type] * TILE_SIZE + offset[1],
                         PIX_SIZE, PIX_SIZE)

            assert KLBoard.tiles_mask       # to help mypy making sure that tiles_mask is not None
            pm.drawPixmap(offset[0], offset[1],
                          KLBoard.tiles_mask,
                          quarter_nb * TILE_SIZE + offset[0], piece_tile[piece_type] * TILE_SIZE + offset[1],
                          PIX_SIZE, PIX_SIZE)

        p.end()
        pm.end()
        pix.setMask( mask )


    def move_piece( self, pid: str, delta: Tuple[int, int] ) -> None:
        dx, dy = delta
        sz = len(self.scene_item_dict[pid])

        # For big tiles, we need to move big step by big step to keep smooth
        # display. For small tiles, we can move pixel by pixel.
        if (sz < 3): incr = 1
        elif sz < 8: incr = 2
        elif sz < 16: incr = 4
        elif sz < 32: incr = 8
        else : incr = 16
        
        for _ in range( TILE_SIZE//incr ):
            for cs in self.scene_item_dict[pid]:
                cs.moveBy( float( dx*incr ), float( dy*incr ) )
            self.m_scene.update()

        incr = TILE_SIZE % incr
        if incr :
            for cs in self.scene_item_dict[pid]:
                cs.moveBy( float( dx*incr ), float( dy*incr ) )
            self.m_scene.update()
            

    def mousePressEvent(self, e: QMouseEvent) -> None:
        pid = self.klmap.pid( e.x() // TILE_SIZE, e.y() // TILE_SIZE )
        if len( self.klmap.possibleMove( pid ) ) == 0:
            return

        self.is_clicking = True
        self.is_draging = False
        self.drag_pid = pid
        self.drag_x = e.x() // TILE_SIZE
        self.drag_y = e.y() // TILE_SIZE
        self.drag_timer.start(500)


    def set_draging(self) -> None:
        assert self.is_clicking, "timer expired while not clicking!!!"
        self.is_draging = True
        self.setCursor(Qt.ClosedHandCursor)


    def mouseReleaseEvent(self, _e: QMouseEvent) -> None:
        self.setCursor(Qt.ArrowCursor)
        if not self.is_clicking:
            return
    
        pm = self.klmap.possibleMove(self.drag_pid)
        if len(pm) == 0: 
            self.drag_timer.stop()
            self.is_clicking = False
            return

        # tile was clicked
        if not self.is_draging:
            self.drag_timer.stop()
            if len(pm) == 1:
                self.sig_move.emit((self.drag_pid, pm[0]))
            self.is_clicking = False
            return

        # tile was dragged
        self.drag_timer.stop()
        self.is_clicking = False
        self.is_draging = False


    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        if not self.is_clicking :
            return

        dx = e.x() // TILE_SIZE - self.drag_x
        dy = e.y() // TILE_SIZE - self.drag_y
        d = dx, dy
        if d == (0,0): return

        pm = self.klmap.possibleMove(self.drag_pid)

        # computes the cos of the angle between d and the possible move
        l0 = map( lambda v,m : (cos(v,m), m), [d] * len(pm), pm )

        # keeps only moves in almost the same direction (cos > 0)
        l1 = filter( lambda x : x[0] > 0, l0 )
        l2 = sorted(l1, reverse=True)
        rpm = list(map( lambda x : x[1], l2 ))

        if len(rpm) > 0:
            self.sig_move.emit((self.drag_pid, rpm[0]))
            self.is_draging = True
            self.drag_x = self.drag_x + rpm[0][0]
            self.drag_y = self.drag_y + rpm[0][1]

