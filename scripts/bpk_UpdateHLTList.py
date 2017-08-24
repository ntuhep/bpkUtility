#!/bin/env python2
#*************************************************************************
#
#  Filename    : bpk_UpdateHLTList.py
#  Description : Updating an existing HLT List
#  Author      : Yi-Mu "Enoch" Chen [ ensc@hep1.phys.ntu.edu.tw ]
#
#*************************************************************************
import argparse
import subprocess
import os
import re
import sys

from bpkFrameWork.bpkUtility.getHLTnames import getHLTfromlistfile
#from bpkFrameWork.bpkUtility.pluginHLTNames import GetHLTNames

bpkutil_path = os.environ['CMSSW_BASE'] + '/src/bpkFrameWork/bpkUtility/'

formathelp_str = """
    format string must be in the format of a python dictionary with a string as the key value and a list of version integers as the dictionary value.
    Valid examples:
     - { 'v1.0.1':[1,3,4], 'v1.1.1':[6,9,8], }
     - { 'v2.0.1':range(1,9) }
"""

def main(args):
    parser = argparse.ArgumentParser(
        "Options for updating a HLTList file",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )

    inputsource = parser.add_mutually_exclusive_group(required=True)

    # Input source inpur options
    inputsource.add_argument( '-f', '--inputfile',
        help='Input version file to check for new HLT paths' + formathelp_str,
        type=str, default=None)
    inputsource.add_argument( '-s', '--inputstr',
        help='Input version string to check for new HLT paths' + formathelp_str,
        type=str, default=None)

    # Update operation to perform
    parser.add_argument( '-a', '--action',
        help='Operation to perform with the new found HLT names,\nappend: Appending new HLT to end of file.|\nmerge: Sort the new HLT paths along with the existing HLTs.|\nclear: Scrap existing file contents and create new list.|',
        type=str, choices=['append','merge','clear'],default='append'
        )

    parser.add_argument('-o', '--outputfile',
        help='Which HLT list file to update/write to',
        type=str, default=bpkutil_path+'./data/HLTList.asc')
    parser.add_argument('-t', '--tag',
        help='edm::InputTag of trigger collection',
        type=str, default='TriggerResults::HLT')
    parser.add_argument('-p','--pathprefix',
        help='HLT configuration data base prefix path',
        type=str, default = 'orcoff:/cdaq/physics/Run2017/2e34/')
    parser.add_argument('-r','--regexpattern',
        help='HLT regex pattern to get from config files',
        type=str, nargs='+',default=[r'HLT_Mu.*', r'HLT_Ele.*',r'HLT_IsoMu.*',r'HLT_TkMu.*'])

    try:
        opt = parser.parse_args(args[1:])
    except:
        print "Error processing arguments!"
        parser.print_help()
        raise

    ## Getting the list of configuration data bases to check
    inputstr = ""
    configlist = []
    if opt.inputfile :
        with open( opt.inputfile, 'r') as inputfile :
            inputstr = inputfile.read()
    else:
        inputstr = opt.inputstr
    try:
        configlist = eval( inputstr )
    except:
        print 'Bad format detected!'
        print formathelp_str
        raise

    # Getting the unique list of HLT paths from the configuration file that match the required
    # HLT string pattern.
    names_in_config = []
    for tag , versionlist in configlist.iteritems() :
        for version in versionlist:
            configpath = '{0}/{1}/HLT/V{2}'.format( opt.pathprefix, tag, version )
            configpath = re.sub( r'\/+','/', configpath ) # Stripping double slashes to single
            print 'Getting config paths: [', configpath , ']....'
            process = subprocess.Popen(['hltListPaths', configpath, '--only-paths'], stdout=subprocess.PIPE)
            out, err = process.communicate()
            for x in out.split() :
                for pattern in opt.regexpattern :
                    if re.match( pattern, x.strip() ):
                        names_in_config.append( x.strip() )

            names_in_config = set(names_in_config)
            names_in_config = list(names_in_config)

    names_in_config.sort()


    # Comparing the list with the existing one in the target output file, overwrite if nessasary
    names_in_file = []
    if opt.action == 'clear' :
        names_in_file = names_in_config
    else:
        names_in_file = getHLTfromlistfile(opt.outputfile)
        for name in names_in_config:
            if name not in names_in_file:
                print "New name (", name, ") found!"
                names_in_file.append(name)
        if opt.action == 'merge':
            names_in_file.sort()

    checkfile = open(opt.outputfile, 'w')
    checkfile.write('\n'.join(names_in_file))
    checkfile.close()

if __name__ == '__main__':
    main(sys.argv)
