#
#	Klotski :  a bricks game
#



PACKAGE = klotski
VERSION = beta_1.0

# edit this line if you want to install klotski somewhere else.
prefix = /usr/local

bindir = $(prefix)/bin
datadir = $(prefix)/share

pkgdatadir = $(datadir)/klotski/$(VERSION)



#######################################################
# Users are not supposed to change anything below that point.


sources = src/have_pyqt.py src/klotski.py src/map.py src/board.py src/enum.py	

#
# targets
#

all: run-klotski

run-klotski: src/klotski
	cd src && ./klotski


test: src/have_pyqt.py
	cd src && python have_pyqt.py


install: test install-bin install-data 
	-echo "Ok, you can now run klotski by typing klotski"

install-bin: src/klotski
	-mkdir -p $(bindir)
	sed -e 's|@pkgdatadir@|$(pkgdatadir)|' < $< > $(bindir)/klotski
	chmod a+rx,go-w $(bindir)/klotski
ifdef KDEDIR
	-mkdir -p $(KDEDIR)/share/applnk/Games
	cp klotski.desktop $(KDEDIR)/share/applnk/Games
endif


install-data:
	-rm -rf $(pkgdatadir)
	mkdir -p $(pkgdatadir)
	cp -dR -p src/* $(pkgdatadir)/
	chmod -R a+r $(pkgdatadir)

uninstall:
	-rm -f $(bindir)/klotski
	-rm -rf $(pkgdatadir)


.PHONY: default run-klotski install install-bin install-data uninstall

