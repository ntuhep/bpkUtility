#!/bin/env python
#*******************************************************************************
 #
 #  Filename    : bpk_MakeFormat.py
 #  Description : Making format.h file form variables listed in data/*.csv
 #  Author      : Yi-Mu "Enoch" Chen [ ensc@hep1.phys.ntu.edu.tw ]
 #
#*******************************************************************************
import bpkFrameWork.bpkUtility.variableListing as mylist
import bpkFrameWork.bpkUtility.Prompt as prompt
import os
import sys
import argparse


class_list = [
    "EvtInfo",
    "GenInfo",
    "JetInfo",
    "LepInfo",
    "PhotonInfo",
    "TrgInfo",
    "VertexInfo",
    "RunInfo",
]

format_content = """
/*******************************************************************************
 *
 *  Filename    : format.h
 *  Description : The branch format for the bprimeKit nTuple
 *
*******************************************************************************/
#ifndef __BPRIMEKIT_FORMAT_H__
#define __BPRIMEKIT_FORMAT_H__

//------------------------------  Required libraries  -------------------------------
#include "TriggerBooking.h"
#include <TTree.h>
#include <vector>

//-------------------------------  Size limitations  --------------------------------
#define MAX_LEPTONS        256
#define MAX_TRACKS         256
#define MAX_JETS           128
#define MAX_PHOTONS        128
#define MAX_GENS           128
#define MAX_LHE            256
#define MAX_Vertices       256
#define MAX_BX             128
#define MAX_TRGOBJS        64

{}

#endif // __BPRIMEKIT_FORMAT_H__
"""

defaultdir = os.environ['CMSSW_BASE'] + '/src/bpkFrameWork/bpkUtility/data/'

def main():

    parser = argparse.ArgumentParser("Options for making trigger format")
    parser.add_argument('-d','--dir',help='directory of branch setting csv file', type=str, default=defaultdir )
    parser.add_argument('-o','--output',help='output file', type=str, default='./format.h' )
    parser.add_argument( '-f', '--force', action='store_true', help='force override of output file if already exists' )

    opt = parser.parse_args()

    print ">>> Getting Branch settings from from: ", opt.dir
    print ">>> Saving output to:", opt.output

    if os.path.isfile(opt.output):
        if not opt.force and not prompt.prompt("Override contents in "+opt.output+"?" ):
            print "Aborting...."
            sys.exit(0)
        else:
            print ">>> Overriding contents of:", opt.output

    content = ""
    for classdef in class_list:
        class_name = classdef + "Branches"
        class_file = 'data/' + class_name + '.csv'
        content += mylist.MakeClassString( class_file, class_name , classdef )

    output = open( opt.output , 'w' )
    output.write(
        format_content.format( content )
    )
    output.close()
    os.system('astyle --suffix=none format.h')


if __name__ == "__main__":
    main()
