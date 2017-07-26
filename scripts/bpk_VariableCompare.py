#!/usr/bin/env python2
'''
main code for analyze two files:
    csv in 'data/'
    new txt file (analysis.txt'(you should input it when you execute the file)

    Main code adds functions and control the flow.
    this code contains:
        1. add options to be used
        2. analyze dictionary in the input file and old data/
        3. compare easily about branch name

        4. compare old and new dictionaries and record the difference

        5. output the result
'''
import argparse
import os
import sys

# 1. add file options, ex: '--help'
from bpkFrameWork.bpkUtility.returnFromFile import listDIR, dictInTXT, addDictFromCSV
from bpkFrameWork.bpkUtility.analyzeFile import analyze2Dictionary

def main():

    desc=argparse.ArgumentParser()
    desc.add_argument('-i', '--input',
                        help='The input file of user code variables in txt format.',
                        type=str, , require=True)
    desc.add_argument( '-o', '--output',
                        help='The output file to print the results',
                        type=str, default='result.txt', )
    desc.add_argument('--force', '-f',
                        help='Whether to overwrite the file if already exists',
                        action='store_true',)
    args=desc.parse_args()

    # 2. create two dictionaries
    oldBranchDicts={}
    newBranchDicts=dictInTXT(args.input)

    # 3. create two branches and compare them
    datapath = os.environ['CMSSW_BASE'] + '/src/bpkFrameWork/bpkUtility/data/'
    oldBranches=listDIR( datapath, '.+Branches.csv')

    newBranches=[]
    for key in newBranchDicts:
        newBranches.append( key )

    if len(oldBranches) is not len(newBranches):
        print 'numbers of branches are not the same, check it out!'
        print 'old: ' + str( len(oldBranches) )
        print 'new: ' + str( len(newBranches) )

    for bName in oldBranches:
        oldBranchDicts.update( addDictFromCSV(bName, datapath+bName+'.csv') )

    # 4. analyze two dictionaries
    results=analyze2Dictionary( oldBranchDicts, newBranchDicts )

    # 5. output results (quickly check if output already exists)
    if os.path.isfile( args.output ) and not args.force :
        if not opt.force and not prompt.prompt("Override contents in "+args.output+"?" ):
            print "Aborting...."
            sys.exit(0)
        else:
            print ">>> Overriding contents of:", args.output

    with open( args.output, 'w') as outputfile :
        for branchName, nameList in results.iteritems():
            f.write( '----------------------------------\n' )
            f.write( '%s : \n' %branchName )
            f.write( '### Variable only in config files:\n' )
            f.write( '\n'.join( nameList['old'] ) )
            f.write( '### Variables only in code files:\n' )
            f.write( '\n'.join( nameList['new'] ) )
    f.close()


if __name__ == '__main__':
    main()
