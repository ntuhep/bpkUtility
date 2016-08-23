#*******************************************************************************
 #
 #  Filename    : makeTriggerBooking.py
 #  Description : Python script for generating TriggerBooking header file
 #  Author      : Yi-Mu "Enoch" Chen [ ensc@hep1.phys.ntu.edu.tw ]
 #
#*******************************************************************************
from bpkFrameWork.bpkUtility.getHLTnames  import getHLTfromlistfile
import optparse
fileformat = """
#ifndef __TRIGGERBOOKING_H__
#define __TRIGGERBOOKING_H__

#define N_TRIGGER_BOOKINGS {0}

const std::string TriggerBooking[N_TRIGGER_BOOKINGS] = {{
{1}
}};

enum TriggerBitNumber {{
{2}
}};

#endif // __TRIGGERBOOKING_H__
"""

def main():
    parser = optparse.OptionParser()
    parser.add_option( '-i', '--input', dest='input' , help='inputfile to read' , type='string', default='data/HLTList.asc' )
    parser.add_option( '-o', '--output',dest='output', help='output destination', type='string', default='./TriggerBooking.h')

    opt, args = parser.parse_args()

    namelist = getHLTfromlistfile( opt.input )

    stringcontent = '   "' +  '",\n   "'.join(namelist) + '"'
    enumcontent   = ""
    for index,name in enumerate(namelist) :
        enumformat = "   {} = {}"
        enumcontent = enumcontent + enumformat.format( name,index )
        if index != len(namelist)-1:
            enumcontent += ',\n'

    print type(enumcontent)
    output = open( opt.output, 'w' )
    outputcontent = fileformat.format(
        len(namelist),
        stringcontent,
        enumcontent
    )
    output.write( outputcontent)
    output.close()


if __name__ == '__main__':
    main()
