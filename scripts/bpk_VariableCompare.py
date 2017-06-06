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


# 1. add file options, ex: '--help'
from bpkFrameWork.bpkUtility.basicIOoptions import basicIOoptions
from bpkFrameWork.bpkUtility.returnFromFile import listDIR, dictInTXT, addDictFromCSV
fileNameSet=basicIOoptions()

# 2. create two dictionaries
oldBranchDicts={}
newBranchDicts=dictInTXT(fileNameSet['in'])

# 3. create two branches and compare them
oldBranches=listDIR('../data/', '.+Branches.csv')


newBranches=[]
for key in newBranchDicts:
    newBranches.append( key )

if len(oldBranches) is not len(newBranches):
    print 'numbers of branches are not the same, check it out!'
    print 'old: ' + str( len(oldBranches) )
    print 'new: ' + str( len(newBranches) )
    #exit(1)

for bName in oldBranches:
    oldBranchDicts.update( addDictFromCSV(bName, '../data/'+bName+'.csv') )

# 4. analyze two dictionaries
from bpkFrameWork.bpkUtility.analyzeFile import analyze2Dictionary
results=analyze2Dictionary( oldBranchDicts, newBranchDicts )

# 5. output results
import os
if os.path.exists(fileNameSet['out']) and not fileNameSet['force']:
    print '###file exists! add "-f" to force it overriding'
    exit(1)
f=open(fileNameSet['out'], 'w')
for branchName, nameList in results.iteritems():
    f.write( '----------------------------------\n' )
    f.write( '%s : \n' %branchName )
    f.write( '### in old files:\n' )
    for varName in nameList['old']:
        f.write( '%s\n' %str(varName) )
    f.write( '### in new files:\n' )
    for varName in nameList['new']:
        f.write( '%s\n' %str(varName) )
f.close()


