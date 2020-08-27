'''
This script generates a big pixmap from all the tiles in the subdirs

Author: Philippe Fremy
License: Gnu GPL (see fname LICENSE)
'''


import sys
sys.path.append("../src")

from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QApplication

from kl_enum import pix_list, tile_list, TILE_SIZE, TILE_FILE_NAME

def generate_pix( image: QImage, piece_name: str ) -> None:
	'''Create an image the sub-tiles for the piece_name
	'''
	pix = QImage()
	xoffset = 0
	yoffset = tile_list[piece_name] * TILE_SIZE
	for p in pix_list:
		pname = piece_name + "/" + p + ".xpm"
		if not pix.load(pname):
			raise ValueError("Unable to load " + pname)

		for i in range( TILE_SIZE ):
			for j in range( TILE_SIZE ):
				image.setPixel( xoffset + i,  yoffset + j, pix.pixel( i, j ))

		xoffset = xoffset + TILE_SIZE

def main() -> None:
	result = QImage( TILE_SIZE * len(pix_list), TILE_SIZE * len( tile_list ), QImage.Format_ARGB32 )
	for t in tile_list.keys():
		print("Generating pixmap for ", t)
	generate_pix( result, t ) 

	print("../src/" + TILE_FILE_NAME + " generated!")
	result.save( "../src/" + TILE_FILE_NAME, "PNG" )

if __name__ == '__main__':
	main()
	
