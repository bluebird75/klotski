#!/usr/bin/env python

import sys

try:
	from qt import *
	qtv3 = map(int, qVersion().split('.')) >= [3,0,0]

	if qtv3:
		from qtcanvas import *
	

except ImportError:
	str = """Can not import Qt!

You must have PyQt installed to run klotski. 
Download PyQt from The Kompany home page:
http://www.thekompany.com/projects/pykde/download.php3
and follow installation instructions carefully.

Windows users : 
Edit klotski.bat if klotski doesn't work even if you have instlled PyQt.
"""

	print str
	print "\nPress enter"
	raw_input()
	
	sys.exit(-1)


	

