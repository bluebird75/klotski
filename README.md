# Klotski

*by Philippe Fremy <phil@freehackers.org>*

*Graphics by Ben Adler <benadler@bigfoot.de>*

|![Ane Rouge](https://raw.githubusercontent.com/bluebird75/klotski/master/pixmaps/klotski-forget-me-not.png)|![All klotski boards](https://raw.githubusercontent.com/bluebird75/klotski/master/pixmaps/klotski-boards.PNG)|
|--|--|

Klotski is small brick game which has its root in a wooden game named (in french) *Ane rouge*.  The goal is to bring the red piece to its destination by moving other pieces. It sounds simple but it is a real brainteaser.

There was a klotski game on Windows 3.1, and this is where all levels are from. 

To run Klotski:

1. If you are Windows, simply download the exe file from [here](https://github.com/bluebird75/klotski/releases/tag/VERSION_1_3_2) and run it.
   

2. In other situations, you need to use Python to run it. Klotski requires Python 3.5 (at least) and PyQt 5.

Type: 

    python3 -m pip install klotski
    
To play:

    python3 -m klotski



This was my first program using Python and PyQt back in 2001.

Contributions and feedback are gladly welcome. Especially, bug, new levels or new tile themes. To add new levels, just edit [boards.kts](https://github.com/bluebird75/klotski/blob/master/src/boards.kts), the format is pretty simple.  To add new tile themes, look at [pixmap/THEMES.txt](https://github.com/bluebird75/klotski/blob/master/pixmaps/THEMES.txt) and replace the image klotski-tiles.png .

For any bugs or feedback, please use the GitHub page: https://github.com/bluebird75/klotski 

Full solution to *Ane Rouge* are available [here](https://www.freehackers.org/Klotski:Solution_of_Ane_Rouge).

### Release history

#### v1.3.2: 22 Nov 2021
* fix bug due to new window resizing capability. Add executable for Windows.

#### v1.3.1: 16 May 2021
* window may be resized smaller than the board, to fit smaller screens 

#### v1.3: 10 September 2020
* make it installable through pypi.org and pip
* move project to GitHub
* internal:
    * add type annotations
    * port from PyQt3 to PyQt5
    


#### version 1.2: 01 June 2006
* Windows version with installer: [Setup-Klotski-1.2-20060601.exe](http://www.freehackers.org/media/bluebird/klotski/Setup-Klotski-1.2-20060601.exe)


#### version 1.1: 17 November 2004

* Unix version: [klotski-1-1.tar.bz2](http://www.freehackers.org/media/bluebird/klotski/klotski-1-1.tar.bz2)
* Windows Version with installer: [Setup-Klotski-1.1-20050416.exe](http://www.freehackers.org/media/bluebird/klotski/Setup-Klotski-1.1-20050416.exe)


#### version 1.0 : 23 January 2001

* Unix version: [klotski-1.0.tar.bz2](http://www.freehackers.org/media/bluebird/klotski/klotski-1.0.tar.bz2)
* Windows version (no installer): [klotski-1.0.zip](http://www.freehackers.org/media/bluebird/klotski/klotski-1.0.zip)
