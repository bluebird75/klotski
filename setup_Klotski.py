# ============================================================================
#	Project Name : InKit
#	Version : $Id$
#	
#	The Original Code is inKit code.
#	
#	The Initial Developer of the Original Code is InSeal SAS.
#	
#	Portions created by the Initial Developer are Copyright (C) 2002-2004 the
#	Initial Developer. All Rights Reserved.
#	
#	This file is copyrighted to InSeal SAS and can not be redistributed
#	freely. See the file LICENSE.txt accompanying this file for redistribution.
#	
#	This program is distributed in the hope that it will be useful, but
#	WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
#	or FITNESS FOR A PARTICULAR PURPOSE.
# ============================================================================

import py2exe, sys, os
from distutils.core import setup
from packaging import *

SCRIPTPATH = r'd:\philippe\phil-cvs\devel\klotski\src'
sys.path.append( SCRIPTPATH ) 
SETUPFILE = "Setup - Klotski"
SCRIPTNAME = r"klotski"

SETUPFILE += ' - %s' % datestr()

# clean directories of previous build
cleanTempDir()
cleanPreviousBuild(SETUPFILE)


############################################################################
#			Build python setup() file
############################################################################
dictAppli = {
	'APPLINAME' : 	'Klotski',
	'DESC' : 		'Klotski',
    'SCRIPTPATH' :  SCRIPTPATH,
	'VERSION' : 	datestr_decimal(),
	'SCRIPTS' : 	[ os.path.join( SCRIPTPATH, SCRIPTNAME + ".py" ) ],
	'DATAFILES' : 	[ 
		('.', [ os.path.join( SCRIPTPATH, 'klotski-tiles.png' ),
		os.path.join( SCRIPTPATH, 'boards.kts' ),
		os.path.join( SCRIPTPATH, '..', 'README.txt' ),
		os.path.join( SCRIPTPATH, '..', 'LICENSE.txt' ) ] )
	],


	# used when packaging with the installer
	'SETUPFILE' : 	SETUPFILE,
    'SCRIPTNAME':   SCRIPTNAME,
	'GROUPNAME':    'Klotski'
}

packagePy2exe( dictAppli, WINDOWS_MODE | NO_LOG_FILES )

try:
	raw_input("\nYour application is ready to package in dist/%s\n[Press a key when ready]" % SCRIPTNAME )
except KeyboardInterrupt:
	sys.exit()

packageInno( dictAppli, dictAppli, WITHOUT_DATA, WITH_COMPRESSION )
postPackageClean()


print "Done\n"
raw_input("[Press a key to finish]")
