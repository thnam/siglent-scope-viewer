#!/usr/bin/env python3
import pyvisa
import sys, os, signal
import argparse

from datetime import datetime, timezone
from time import sleep
from PIL import Image
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
        rm = pyvisa.ResourceManager()
        sds = rm.open_resource(f"TCPIP::{ip}::INSTR")

        sds.chunk_size = 2*1024*1024 
        #default value is 20*1024(20k bytes), and the bitmap size is about 700 KB
        sds.timeout = 3000 #default value is 2000(2s)

        while not killer.kill_now:
            sds.write("SCDP")
            result_str = sds.read_raw()

            tempBuff = BytesIO()
            tempBuff.write(result_str)
            tempBuff.seek(0)

            image = Image.open(tempBuff)
            image.save(output)

            utc_dt = datetime.now(timezone.utc)
            print("{} - screenshot captured.".format(utc_dt.astimezone().isoformat()))
            sleep(interval)
    except pyvisa.errors.VisaIOError:
        print('Could not connect to device, is the IP address correct?',
                file=sys.stderr)
        exit(-1)
    pass

def main():
    try:
        with FileLock(lock).acquire(timeout=1):
            takeScreenshot()
    except Timeout:
        print('Could not acquire lock, is there another instance of this '
                'script running?', file=sys.stderr)
        exit(-1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(allow_abbrev=False,
            description='Capture screenshot from a Siglent SDS scope')
    parser.add_argument('--ip', dest='ip', action='store',
            required=True, help='IP address of the scope')
    parser.add_argument('-o', '--ouput', action='store', dest='output',
            help='output file name', default='scope.png')
    parser.add_argument('--interval', dest='interval', action='store',
            default=1.0, help='interval between screenshots', type=float)
    parser.add_argument('--lock', dest='lock', action='store',
            help='lock file', default='/tmp/scdp.quad.lock')
    args = parser.parse_args()

    ip, output, interval, lock = args.ip, args.output, args.interval, args.lock
    main()
