#!/usr/bin/env python

##############################################################################
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


if __name__ == '__main__': main()

# vi:set ts=4 sts=0 sw=4:
