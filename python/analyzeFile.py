#!/usr/bin/env python2
'''
this code is to compare two dictionaries
the dictionary should have the format:
    dic={ 'aaaBranches': { 'instance': 'aaa', 'variable': ['var1', 'var2', ...] },
          'bbbBranches': { 'instance': 'bbb', 'variable': ['var1', 'var2', ...] }    }
compare about the variables within the same Branches.
and the output is the different list
the output owns the format:
    out={ 'aaaBranches': { 'old': ['var1', 'var2'], 'new': ['var3', 'var4'] },
          'bbbBranches': { 'old': ['var1', 'var2'], 'new': ['var3', 'var4'] }   }

'''


def printByTag( LIST, TAG ):
    for l, t in zip( LIST, TAG ):
        if t is False:
            print '    '+ l

def recordNameByTag( LIST, TAG):
    nameList=[]
    for l, t in zip( LIST, TAG ):
        if t is False:
            nameList.append( l )
    return nameList

def analyze2Dictionary(oldNameDict, newNameDict):

    # find branchName, find the shorter one
    branchName=[]

    oldbName=[]
    newbName=[]
    for key in newNameDict:
        newbName.append( key )
    for key in oldNameDict:
        oldbName.append( key )
    if len(oldbName) > len(newbName):
        branchName=newbName
    else:
        branchName=oldbName


    diffNum={}
    diffName={}
    for bName in branchName:
        oldName=oldNameDict[ bName ]['variable']
        newName=newNameDict[ bName ]['variable']

        oldTag = [ False ] * len(oldName)
        newTag = [ False ] * len(newName)

        for i, oName in enumerate( oldName ):
            for j, nName in enumerate( newName ):
                if oName == nName:
                    oldTag[i] = newTag[j] = True

        oldAdditionalList=recordNameByTag( oldName, oldTag )
        newAdditionalList=recordNameByTag( newName, newTag )
        nameList={ 'old':oldAdditionalList, 'new':newAdditionalList }

        diffNum.update( {bName:( len(newName) - len(oldName) )} )
        diffName.update( {bName:nameList} )

    return diffName
    #return diffNum


if __name__ == "__main__":
    print "HI"
