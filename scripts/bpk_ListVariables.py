#!/bin/env python2
#*******************************************************************************
 #
 #  Filename    : ListVariables.py
 #  Description : Takes input C++ files and list all the variables used in files
 #  Author      : Yi-Mu "Enoch" Chen [ ensc@hep1.phys.ntu.edu.tw ]
 #
#*******************************************************************************
import argparse
import re # regular expression
import pprint

branchlist  = [
    'EvtInfoBranches',
    'GenInfoBranches',
    'JetInfoBranches',
    'LepInfoBranches',
    'PhotonInfoBranches',
    'TrgInfoBranches',
    'VertexInfoBranches',
]

def getbranchinstance( results, inputfile ):
    filecontent = [ x.strip() for x in open(inputfile) ]
    for branch in branchlist:
        if "instance" not in results[branch] :
            results[branch]["instance"] = []

    for branch in branchlist:
        branchregex = re.compile( branch+r"\ *\&*\ *(\w+)" )
        for line in filecontent:
            results[branch]["instance"].extend( branchregex.findall(line) )

        results[branch]['instance'] = list(set(results[branch]['instance']))

def getvariableinstace( results, inputfile ):
    filecontent = [ x.strip() for x in open(inputfile) ]

    for branch in branchlist:
        if 'variable' not in results[branch]:
            results[branch]['variable'] = []

        for binstance in results[branch]["instance"]:
            varregex = re.compile( binstance+r"\ *\.\ *(\w+)" )
            for line in filecontent:
                results[branch]["variable"].extend( varregex.findall(line) )

        results[branch]['variable'] = list(set(results[branch]['variable']))
        results[branch]['variable'].sort()
        try:
            results[branch]['variable'].remove('Register')
        except:
            pass
        try:
            results[branch]['variable'].remove('RegisterTree')
        except:
            pass

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument(
        '--inputfilelist','-i', type=str, nargs='+',
        help='List of input files to use'
        )
    parser.add_argument(
        '--output','-o', type=str, help='write to a certain output file'
    )
    args = parser.parse_args()

    results = {}
    for branch in branchlist:
        results[branch] = {}

    for inputfile in args.inputfilelist:
        getbranchinstance( results , inputfile )

    for inputfile in args.inputfilelist:
        getvariableinstace( results, inputfile )

    if args.output :
        print 'Writting results to ', args.output
        with open(args.output,'w') as fout:
            pprint.pprint(results,stream=fout,depth=3)
    else:
        pprint.pprint(results,depth=3)


    return 0


if __name__ == "__main__":
    main()
