#!/usr/bin/env python2

def listDIR(path, pattern=None):
    import os, re
    dirName = os.listdir(path)
    pat='.+Branches.csv'
    if pattern is not None:
        pat=pattern
    nameList = []
    for dName in dirName:
        match=re.search(pat, dName)
        if match is not None:
            nameList.append( match.group().replace('.csv', '' ) )
    return nameList

def dictInTXT(path):
    with open(path, 'r') as file:
        fileContent=''
        for line in file:
            fileContent+=line
        return eval(fileContent)

def addDictFromCSV(branchName, csvPath):
    import csv
    outDict={}
    with open(csvPath, 'r') as file:
        reader = csv.DictReader(file, delimiter=',')
        name=[]
        for row in reader:
            name.append( row['Varname'] )
        dVar={'instance':branchName.replace('Branches', ''), 'variable':name}
        outDict[branchName]=dVar
    return outDict

if __name__ == "__main__":
    lists = listDIR("../data/", '.+Branches.csv')
    print lists

    #dicts=dictInTXT("analysis.txt")
    #for key, val in dicts.iteritems():
    #    print key + ': ' + str(val)

    #dicts=addDictFromCSV( 'VertexInfoBranches', '../data/VertexInfoBranches.csv' )
    #for key, val in dicts['VertexInfoBranches'].iteritems():
    #    print key + ': ' + str(val)

