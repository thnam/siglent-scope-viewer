# siglent-scope-viewer
This is a naive web viewer for a Siglent oscilloscope. The idea is simple:
- a python script periodically fetches the screenshot from the scope, 
- and a HTML page displays the screenshot.

Tested working on:
- Debian 10.8 with Python 3.7.3
- Ubuntu 16.04.6 with Python 3.7.10

Usage:
```bash
usage: scdp.py --ip IP [-h] [-o OUTPUT] [--interval INTERVAL] [--lock LOCK]

Capture screenshot from a Siglent SDS scope

Required arguments:
  --ip IP               IP address of the scope

Optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --ouput OUTPUT
                        output file name
  --interval INTERVAL   interval between screenshots
  --lock LOCK           lock file
```
