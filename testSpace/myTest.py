#!/usr/bin/env python2

import csv
import sys
sys.path.append("/home/ltsai/Work/github/ntuhep/bpkUtility")

from python.analysis import nameDict
'''
lst = [2,3,4]

for index,element in enumerate(lst):
    print "index",index,"element",element
'''
branchName=[
    'EvtInfoBranches',
    'GenInfoBranches',
    'JetInfoBranches',
    'LepInfoBranches',
    'PhotonInfoBranches',
    'TrgInfoBranches',
    'VertexInfoBranches' ]

diffNum={}
diffName={}
for it in range( len(branchName) ):
    oldName=nameDict[ branchName[it] ]['variable']
    newName=[]
    with open('../data/'+branchName[it]+'.csv', 'r') as file:
        reader = csv.DictReader(file, delimiter=',')
        for row in reader:
            newName.append( row['Varname'] )

    oldTag = [ False ] * len(oldName)
    newTag = [ False ] * len(newName)

    # compare two list
    for i in range( len(oldTag) ):
        for j in range( len(newTag) ):
            if oldName[i] == newName[j]:
                oldTag[i] = newTag[j] = True

    from python.func import recordNameByTag
    oldDiffList=recordNameByTag( oldName, oldTag )
    newDiffList=recordNameByTag( newName, newTag )
    nameList={ 'old':oldDiffList, 'new':newDiffList }

    diffNum.update( {branchName[it]:len(newName) - len(oldName)} )
    diffName.update( {branchName[it]:nameList} )


for key, val in diffNum.iteritems():
    print key + ': ' + str(val)
