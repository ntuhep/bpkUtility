#!/usr/bin/env python2

def printByTag( LIST, TAG ):
    for i in range( len(TAG) ):
        if TAG[i] is False:
            print '    '+ LIST[i]

def recordNameByTag( LIST, TAG):
    nameList=[]
    for i in range( len(TAG) ):
        if TAG[i] is False:
            nameList.append( LIST[i] )
    return nameList
