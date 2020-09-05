'''
Author: Philippe Fremy
License: Gnu GPL (see file LICENSE)
'''
from typing import Union, Dict

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListView, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QAbstractListModel, QModelIndex, QVariant, Qt

from .kl_enum import *
from .kl_map import KLMap

class KlMinimapProvider(QAbstractListModel):

    def __init__(self, level_dict: Dict[int, KLMap], mini_maps_dict: Dict[int, QPixmap ]) -> None:
        super().__init__()
        assert len(mini_maps_dict) > 0, "minimap board dict is empty!"
        assert len(level_dict) > 0, "level dict is empty!"

        self.level_dict = level_dict
        self.mini_maps_dict = mini_maps_dict

    def rowCount(self, parentIdx: QModelIndex) -> int:  # type: ignore # mypy does not understand the Qt overload of that one
        # -1 because we don't want to display splash screen as a board
        return len(self.level_dict) - 1

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Union[str, QPixmap, QVariant]:
        if not index.isValid():
            return QVariant()

        row = index.row()
        if role == Qt.DisplayRole:
            return self.level_dict[row+1].name

        if role == Qt.DecorationRole:
            return self.mini_maps_dict[row+1]

        return QVariant()


class KLBoardChooser(QDialog) :

    def __init__(self, minimapProvider: KlMinimapProvider, parent: QWidget) -> None:
        super().__init__(parent)
        ly = QVBoxLayout( self )
        self.iv = QListView( self )
        self.iv.setModel( minimapProvider )
        ly.addWidget( self.iv, 1 )
        self.iv.setViewMode( QListView.IconMode )
        self.iv.setWrapping(True)
        self.iv.setResizeMode( QListView.Adjust )

        self.iv.activated.connect(self.mini_map_selected)
        self.resize( 500, 500  )


    def mini_map_selected(self, item: QModelIndex) -> None:
        if not item: return
        self.done(item.row() + 1)


