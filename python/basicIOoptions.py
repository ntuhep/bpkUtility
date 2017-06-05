#!/usr/bin/env python2
'''
This is the module for options setting.
This module allows you use options:
    -h, --help: print the usage
    -i, --input: add a input file
    -o, --output: modify the output fileName
                  if this is not set, use the default name 'result.txt'
'''


import sys, getopt
def usage():
    print "usage:%s [i|o|h|f] [--help|--output|--input|--force] args..."
    print "especially, you need to input a file"

def basicIOoptions():
    inputFile=''
    outputFile='result.txt'
    forceTag=False

    opts,args = getopt.getopt(sys.argv[1:], "i:o:hf", ['help', 'output=', 'input=', 'force'])
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit(1)
        elif opt in ("-i", "--input"):
            inputFile=arg
        elif opt in ("-o", "--output"):
            outputFile=args
        elif opt in ('-f', '--force'):
            forceTag=True
    if inputFile == '':
        usage()
        sys.exit(1)

    print 'import file is: '+inputFile
    print 'created file is: '+outputFile

    return { 'in':inputFile, 'out':outputFile, 'force':forceTag }


if __name__ == "__main__":
    basicIOoptions()



