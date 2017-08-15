#!/bin/env python2
#*************************************************************************
#
#  Filename    : bpk_UpdateTrgBook.py
#  Description : Updating an existing HLT List
#  Author      : Pu-Sheng Chen [ sam7k9621@hep1.phys.ntu.edu.tw ]
#
#*************************************************************************
from bpkFrameWork.bpkUtility.getHLTnames  import getHLTfromlistfile
import argparse
import sys
import os

TrgBook_h ="""\
#ifndef __TRIGGERBOOKING_H__
#define __TRIGGERBOOKING_H__

#define N_TRIGGER_BOOKINGS {0}

//update to {1}

const std::string TriggerBooking[N_TRIGGER_BOOKINGS] = {{

    {2}

}};

enum TriggerBitNumber {{

    {3}

}};

#endif // __TRIGGERBOOKING_H__
"""

def main(args):
    parser = argparse.ArgumentParser(
            "Options for updating TriggerBooking.h",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
            )

    # Operation to perform
    parser.add_argument(
            '-f', '--inputfile',
            help='Input trigger list file',
            type=str, default=None, required=True
            )

    parser.add_argument(
            '-v', '--version',
            help='Input the latest version you have added in trigger list file',
            type=str, default=None, required=True
            )

    parser.add_argument(
            '-o', '--outputfile',
            help='Output file in interface',
            type=str, default="TriggerBooking.h"
            )

    try:
        opt = parser.parse_args()
    except:
        print "Error processing arguments!"
        parser.print_help()
        raise

    print ">>> Getting trigger list from: ", opt.inputfile

    ## Transform the lines from HLT list into output.h
    content = getHLTfromlistfile( opt.inputfile )

    content_dec = [ " \"{}\"".format(c) for c in content ]
    dclr_line = ",\n    ".join(content_dec)

    content_mod = [ "{0} = {1}".format( trg, idx ) for idx, trg in enumerate(content)]
    enum_line =  ",\n    ".join(content_mod)

    with open(opt.outputfile, "w") as hfile :
        hfile.write( TrgBook_h.format( len(content), opt.version, dclr_line, enum_line ) )

    print ">>> Saving output to:", opt.outputfile

if __name__ == '__main__':
    main(sys.argv)
