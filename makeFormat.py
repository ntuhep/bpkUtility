#!/bin/env python
#*******************************************************************************
 #
 #  Filename    : makeFormat.py
 #  Description : Making format.h file form variables listed in data/*.csv
 #  Author      : Yi-Mu "Enoch" Chen [ ensc@hep1.phys.ntu.edu.tw ]
 #
#*******************************************************************************
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

import bpkFrameWork.bpkUtility.variableListing as mylist
import os

def main():
    content = ""
    for classdef in class_list:
        class_name = classdef + "Branches"
        class_file = 'data/' + class_name + '.csv'
        content += mylist.MakeClassString( class_file, class_name , classdef )

    output = open('format.h' , 'w' )
    output.write(
        format_content.format( content )
    )
    output.close()
    os.system('astyle --suffix=none format.h')


if __name__ == "__main__":
    main()
