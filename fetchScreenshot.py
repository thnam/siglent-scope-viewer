#!/usr/bin/env python3
import pyvisa
import sys, os, signal
import argparse

from datetime import datetime, timezone
from time import sleep
from PIL import Image, ImageDraw
from io import BytesIO
from filelock import Timeout, FileLock

class GracefulKiller:
    kill_now = False
    def __init__(self):
      signal.signal(signal.SIGINT, self.exit_gracefully)
      signal.signal(signal.SIGTERM, self.exit_gracefully) 
      
    def exit_gracefully(self,signum, frame):
      print('Received SIGTERM, exiting gracefully.')
      self.kill_now = True

lock = '/tmp/scdp.quad.lock'
ip = '192.168.1.119'
output = 'scope.png'
interval = 1.
killer = GracefulKiller()

def takeScreenshot():
    try:
        rm = pyvisa.ResourceManager('@py')
        sds = rm.open_resource(f"TCPIP::{ip}::INSTR")
    except pyvisa.errors.VisaIOError:
        print('Could not connect to device, is the IP address correct?',
                file=sys.stderr)
        exit(-1)

    try:
        sds.chunk_size = 2*1024*1024 
        #default value is 20*1024(20k bytes), and the bitmap size is about 700 KB
        sds.timeout = 5000 #default value is 2000(2s)
        while not killer.kill_now:
            sds.write("SCDP")
            result_str = sds.read_raw()

            # the result is in bitmap format, want to convert to png
            tempBuff = BytesIO()
            tempBuff.write(result_str)
            tempBuff.seek(0)

            image = Image.open(tempBuff)
            markup = ImageDraw.Draw(image)
            markup.rectangle([100, -1, 152, 24], fill=None, outline="orange", width=3)

            image.save(f'tmp_{output}')
            os.rename(f'tmp_{output}', output)

            utc_dt = datetime.now(timezone.utc)
            print("{} - screenshot captured.".format(utc_dt.astimezone().isoformat()),
                    flush=True)
            sleep(interval)
    except Exception as e:
        print(e)

def main():
    try:
        with FileLock(lock).acquire(timeout=1):
            takeScreenshot()
    except Timeout:
        print('Could not acquire lock, is there another instance of this '
                'script running?', file=sys.stderr)
        exit(-1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(allow_abbrev=False, add_help=False,
            description='Fetch screenshot from a Siglent SDS scope')
    required = parser.add_argument_group('Required arguments')
    optional = parser.add_argument_group('Optional arguments')

    required.add_argument('--ip', dest='ip', action='store', required=True,
            help='IP address of the scope')

    optional.add_argument('-h', '--help', action='help',
            default=argparse.SUPPRESS, help='show this help message and exit')
    optional.add_argument('-o', '--ouput', action='store', dest='output',
            help='output file name', default='scope.png')
    optional.add_argument('--interval', dest='interval', action='store',
            default=1.0, help='interval between screenshots', type=float)
    optional.add_argument('--lock', dest='lock', action='store',
            help='lock file', default='/tmp/scdp.quad.lock')
    args = parser.parse_args()

    ip, output, interval, lock = args.ip, args.output, args.interval, args.lock
    main()
