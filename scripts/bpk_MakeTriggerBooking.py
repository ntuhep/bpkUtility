#!/bin/env python
#*******************************************************************************
 #
 #  Filename    : bpkg_MakeTriggerBooking.py
 #  Description : Python script for generating TriggerBooking header file
 #  Author      : Yi-Mu "Enoch" Chen [ ensc@hep1.phys.ntu.edu.tw ]
 #
#*******************************************************************************
from bpkFrameWork.bpkUtility.getHLTnames  import getHLTfromlistfile
import bpkFrameWork.bpkUtility.Prompt as prompt
import argparse
import os
import sys

fileformat = """
#ifndef __TRIGGERBOOKING_H__
#define __TRIGGERBOOKING_H__

#define N_TRIGGER_BOOKINGS {0}

const std::string TriggerBooking[N_TRIGGER_BOOKINGS] = {{
{1}
}};

enum TriggerBitNumber {{
{2}
}};

#endif // __TRIGGERBOOKING_H__
"""

defaultinput = os.environ['CMSSW_BASE'] + '/src/bpkFrameWork/bpkUtility/data/HLTList.asc'

def main():
    parser = argparse.ArgumentParser(description="Options for generating TriggerBooking file")
    parser.add_argument( '-i', '--input',  help='input file to read', type=str, default=defaultinput )
    parser.add_argument( '-o', '--output', help='output file', type=str, default='./TriggerBooking.h')
    parser.add_argument( '-f', '--force', action='store_true', help='force override of output file if already exists' )

    opt = parser.parse_args()

    print ">>> Getting trigger list from: ", opt.input
    print ">>> Saving output to:", opt.output

    if os.path.isfile(opt.output):
        if not opt.force and not prompt.prompt("Override contents in "+opt.output+"?" ):
            print "Aborting...."
            sys.exit(0)
        else:
            print ">>> Overriding contents of:", opt.output

    namelist = getHLTfromlistfile( opt.input )

    stringcontent = '   "' +  '",\n   "'.join(namelist) + '"'
    enumcontent   = ""
    for index,name in enumerate(namelist) :
        print "\rTrigger [{}/{}]".format(index+1,len(namelist)) ,
        enumcontent = enumcontent + "   {} = {}".format( name,index )
        if index != len(namelist)-1:
            enumcontent += ',\n'

    output = open( opt.output, 'w' )
    outputcontent = fileformat.format(
        len(namelist),
        stringcontent,
        enumcontent
    )
    output.write( outputcontent )
    output.close()


if __name__ == '__main__':
    main()
