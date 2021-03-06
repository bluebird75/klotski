# Klotski

*by Philippe Fremy <phil@freehackers.org>*

*Graphics by Ben Adler <benadler@bigfoot.de>*

|![Ane Rouge](https://raw.githubusercontent.com/bluebird75/klotski/master/pixmaps/klotski-forget-me-not.png)|![All klotski boards](https://raw.githubusercontent.com/bluebird75/klotski/master/pixmaps/klotski-boards.PNG)|
|--|--|

Klotski is small brick game which has its root in a wooden game named (in french) *Ane rouge*.  The goal is to bring the red piece to its destination by moving other pieces. It sounds simple but it is a real brainteaser.

There was a klotski game on Windows 3.1, and this is were all levels are from. 

Klotski requires Python 3.5 (at least) and PyQt 5. To install Klotski, you must already have Python installed on your computer. 

Type: 

    pip install klotski
    
To play:

    python -m klotski




This was my first program using python and PyQt. I must say I have enjoyed it a lot: Python and Qt are both excellent, easy to use and well documented. I have never been able to implement my ideas so quickly. The usual cycle *think, organise into organigram, code, compile, correct compiling errors, run, correct bugs, run, it works* was reduced to *think, code, run, it works*. Because of the simplicity and the power the python language, my ideas could be expressed very clearly and I could concentrate on what I wanted to do instead of how I needed to code it. The result is a simple and clean program, that was coded in half the time (and probably less) it would have taken to do it in C++.

Contributions and feedback are gladly welcomed. Especially, bug, new levels or new tile themes. To add new levels, just edit [boards.kts](https://github.com/bluebird75/klotski/blob/master/src/boards.kts), the format is pretty simple.  To add new tile themes, look at [pixmap/THEMES.txt](https://github.com/bluebird75/klotski/blob/master/pixmaps/THEMES.txt) and replace the image klotski-tiles.png .

For any bugs or feedback, please use the GitHub page: https://github.com/bluebird75/klotski 

