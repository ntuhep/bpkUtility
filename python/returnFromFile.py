#!/usr/bin/env python2
'''
this is the small functions to operate with file
listDIR:
    input the file path and the pattern(regular expression)
        1. list the files in path.
        2. search for the file with the pattern(include the pattern)
        3. collect the file names and output them as a list
dictInTXT:
    input a file.txt
        1. open the file
        2. let all of the content to be one line
        3. regard the words as options in python and output them (ex: 'num=True' as num variable)
addDictFromCSV:
    input a file.csv
        1. write the file with delimiter ','
        2. load the row with the first element names 'Varname'
        3. create the dictionary with the format:
            dic={ 'aaaBranches': { 'instance': 'aaa', 'variable': ['var1', 'var2', ...] },
                  'bbbBranches': { 'instance': 'bbb', 'variable': ['var1', 'var2', ...] }    }
'''

import os
import re
import csv

def listDIR(path, pattern='.+Branches.csv'):
    dirName = os.listdir(path)
    nameList = []
    for dName in dirName:
        match=re.search(pattern, dName)
        if match is not None:
            nameList.append( match.group().replace('.csv', '' ) )
    return nameList

def dictInTXT(inputfile):
    with open(inputfile, 'r') as txtfile:
        return eval(txtfile.read())

def addDictFromCSV(branchName, csvFile):
    outDict={}
    with open(csvFile, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        name=[]
        for row in reader:
            name.append( row['Varname'] )
        dVar={'instance':branchName.replace('Branches', ''), 'variable':name}
        outDict[branchName]=dVar
    return outDict

if __name__ == "__main__":
    print 'listDIR testint:'
    lists = listDIR("../data/", '.+Branches.csv')
    print lists

    print 'dictInTXT testint:'
    dicts=dictInTXT("analysis.txt")
    for key, val in dicts.iteritems():
        print key + ': ' + str(val)

    print 'addDictFromCSV testint:'
    dicts=addDictFromCSV( 'VertexInfoBranches', '../data/VertexInfoBranches.csv' )
    for key, val in dicts['VertexInfoBranches'].iteritems():
        print key + ': ' + str(val)
