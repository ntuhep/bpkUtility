#!/bin/env python
#*************************************************************************
#
#  Filename    : bpk_UpdateHLTList.py
#  Description : Updating an existing HLT List
#  Author      : Yi-Mu "Enoch" Chen [ ensc@hep1.phys.ntu.edu.tw ]
#
#*************************************************************************
import argparse

from bpkFrameWork.bpkUtility.getHLTnames import getHLTfromlistfile
from bpkFrameWork.bpkUtility.pluginHLTNames import GetHLTNames


def main():
    parser = argparse.ArgumentParser("Options for updating a HLTList file")
    parser.add_argument('-c', '--checkfile', help='Which HLT list file to check for updates', type=str, default='./data/HLTList.asc')
    parser.add_argument('-i', '--input', help='Input EDM file to check for HLT updates', type=str, nargs='+',default=None)
    parser.add_argument('-t', '--tag', help='edm::InputTag of trigger collection', type=str, default='TriggerResults::HLT')

    opt = parser.parse_args()

    if not opt.input:
        print "Error! Input edm file is missing!"
        parser.print_help()
        return 1

    names_in_edm = []
    for inputfile in opt.input:
        names_in_edm.extend( GetHLTNames(inputfile, *opt.tag.split(':')) )
        names_in_edm = set(names_in_edm)
        names_in_edm = list(names_in_edm)

    names_in_edm.sort()
    names_in_file = getHLTfromlistfile(opt.checkfile)

    print len(names_in_file)
    for name in names_in_edm:
        if name not in names_in_file:
            print "New name (", name, ") found!"
            names_in_file.append(name)
    print len(names_in_file)

    checkfile = open(opt.checkfile, 'w')
    checkfile.write('\n'.join(names_in_file))
    checkfile.close()

if __name__ == '__main__':
    main()
