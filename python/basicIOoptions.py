#!/usr/bin/env python2
'''
This is the module for options setting.
This module allows you use options:
    --input     add a input file
    --output    modify the output fileName
    --force     if the file exists, force the program to overwrite
                if this is not set, use the default name 'result.txt'
'''



def basicIOoptions():
    import argparse
    option=argparse.ArgumentParser()

    option.add_argument('--input', '-i',
                        default='',
                        type=str,
                        help='add a input file')
    option.add_argument('--output', '-o',
                        default='result.txt',
                        type=str,
                        help='add a input file')
    option.add_argument('--force', '-f',
                        default=False,
                        action='store_true',
                        help='if the file exists, the tag to overwrite the file')
    options=option.parse_args()

    inputFile=options.input
    outputFile=options.output
    forceTag=options.force

    if inputFile == '':
        options.print_help()
        exit(1)

    print 'import file is: '+inputFile
    print 'created file is: '+outputFile
    print 'force to overwrite file: '+str(forceTag)
    print ''

    return { 'in':inputFile, 'out':outputFile, 'force':forceTag }


if __name__ == "__main__":
    basicIOoptions()



