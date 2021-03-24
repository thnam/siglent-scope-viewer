#!/usr/bin/env python3
import pyvisa
import sys
import argparse

from datetime import datetime, timezone
from PIL import Image
from io import BytesIO

def main(ip, output):
    try:
        rm = pyvisa.ResourceManager()
        sds = rm.open_resource(f"TCPIP::{ip}::INSTR")
        
        sds.chunk_size = 2*1024*1024 #default value is 20*1024(20k bytes)
        sds.timeout = 3000 #default value is 2000(2s)
        
        sds.write("SCDP")
        result_str = sds.read_raw()
        
        tempBuff = BytesIO()
        tempBuff.write(result_str)
        tempBuff.seek(0)
        
        image = Image.open(tempBuff)
        image.save(output)

        utc_dt = datetime.now(timezone.utc)
        print("{} - screenshot captured.".format(utc_dt.astimezone().isoformat()))
    except pyvisa.errors.VisaIOError:
        print('Could not connect to device, is the IP address correct?')
        exit(-1)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(allow_abbrev=False,
            description='Capture screenshot from a Siglent SDS scope')
    parser.add_argument('--ip', dest='ip', action='store',
            required=True, help='IP address of the scope')
    parser.add_argument('-o', '--ouput', action='store', dest='output',
            help='Output file name', default='scope.png')
    args = parser.parse_args()

    main(args.ip, args.output)
