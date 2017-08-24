#*******************************************************************************
 #
 #  Filename    : getHLTnames.py
 #  Description : Simple python script for getting the HLT trigger names
 #  Author      : Yi-Mu "Enoch" Chen [ ensc@hep1.phys.ntu.edu.tw ]
 #
#*******************************************************************************
import ROOT
from DataFormats.FWLite import Events, Handle

def getHLTfromlistfile( asciifile ):
    content = []
    with open(asciifile, 'w+') as listfile:
        content = listfile.readlines()
        content = [ x.strip() for x in content ]
    return content


if __name__ == '__main__':
    print getHLTfromlistfile( './data/HLTList.asc')
