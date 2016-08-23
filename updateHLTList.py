#!/bin/env python
#*******************************************************************************
 #
 #  Filename    : updateHLTList.py
 #  Description : Updating an existing HLT List
 #  Author      : Yi-Mu "Enoch" Chen [ ensc@hep1.phys.ntu.edu.tw ]
 #
#*******************************************************************************
from bpkFrameWork.bpkUtility.getHLTnames    import getHLTfromlistfile
from bpkFrameWork.bpkUtility.pluginHLTNames import GetHLTNames
import optparse

def main():
    parser = optparse.OptionParser()
    parser.add_option( '-c' , '--checkfile' , dest='checkfile' , help='Which file to checkfor updates' , type='string', default='./data/HLTList.asc')
    parser.add_option( '-i' , '--input'     , dest='input'     , help='input edm file to add hlt names', type='string', default=None )
    parser.add_option( '-t' , '--tag'       , dest='tag'       , help='Input tag of trigger results'   , type='string' ,default='TriggerResults::HLT')

    opt, args = parser.parse_args()

    if not opt.input :
        print "Error! Input edm file is missing!"
        return 1

    names_in_edm = GetHLTNames( opt.input , *opt.tag.split(':'))
    names_in_file= getHLTfromlistfile( opt.checkfile )

    print len( names_in_file )
    for name in names_in_edm :
        if name not in names_in_file:
            print "New name (", name, ") found!"
            names_in_file.append(name)
    print len( names_in_file )

    checkfile = open( opt.checkfile , 'w' )
    checkfile.write( '\n'.join(names_in_file) )
    checkfile.close()

if __name__ == '__main__':
    main()
