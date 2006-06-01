					Klotski


       by Philippe Fremy <phil@freehackers.org>
       Graphics by Ben Adler <benadler@bigfoot.de>


Klotski is small brick game which has its root in a wooden game named (in
french) "Ane rouge".  The goal is to bring the red piece to its destination
by moving other pieces. It sounds simple but it is a real brainteaser.

There was a klotski game on Windows 3.1, and this is were all levels are from.
There is also a basic gnome version of klotski at xxx. I had a look at it
before starting Klotski, so some design ideas have probably slipped from there
:-)

Klotski requires that python and PyQt are installed on the target computer I
have run it under Windows 98 and Linux, and it is supposed to run on any
flavour of Unix or Windows.

Check the INSTALL file for details on how to customize installation. Note that
this is not standard installation procedure with configure and so on, so
please read it.

Klotski is written in Python (www.python.org) and uses the
PyQt binding (http://www.thekompany.com/projects/pykde/)
developped by Phil Thompson, to take advantage of the QCanvas from Qt 
(www.trolltech.com)

This is my first program using python and PyQt. I must say I have enjoyed it a
lot: Python and Qt are both excellent, easy to use and well documented. I have
never been able to implement my ideas so quickly. The usual cycle "think,
organise into organigram, code, compile, correct compiling errors, run,
correct bugs, run, it works" was reduced to "think, code, run, it works".
Because of the simplicity and the power the python language, my ideas could be
expressed very clearly and I could concentrate on what I wanted to do instead
of how I needed to code it. The result is a simple and clean program, that was
coded in half the time (and probably less) it would have taken to do it in
C++.

This program is Qt only for the moment, but as soon as the python bindings for
Kde 2.0 are released, I will take advantage of them.

Contributions and feedback are gladly welcomed. Especially, bug, new levels or
new tile themes. To add new levels, just edit boards.kts, the format is pretty
simple.  To add new tile themes, look at pixmap/THEMES.txt and replace the
image klotski-tiles.png .
