# siglent-scope-viewer
This is a naiive web viewer for a Siglent oscilloscope. The idea is simple: a
python script periodically fetches the screenshot from the scope, and a HTML page
displays the screenshot. The refresh rate is 1 Hz.

Tested working on:
- Debian 10.8 with Python 3.7.3
- Ubuntu 16.04.6 with Python 3.7.10
