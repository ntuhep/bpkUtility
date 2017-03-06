#*******************************************************************************
 #
 #  Filename    : VariableListing.py
 #  Description : Helper function for listing all bprimeKit flavour variable in
 #                a input file
 #  Author      : Yi-Mu "Enoch" Chen [ ensc@hep1.phys.ntu.edu.tw ]
 #
#*******************************************************************************
import csv
import re

def ListFromFile( inputfile ):
    ans=[]
    with open(inputfile,'r') as csvfile:
        reader=csv.DictReader(csvfile,delimiter=',')
        for row in reader:
            myrow = {}
            for k,v in row.iteritems():
                try:
                    myrow[k] = v.strip()
                except:
                    myrow[k] = ""
            ans.append( myrow )
    return ans

def BranchName( row ):
    varname = row['Varname']
    varname = re.sub( '_w' , '' , varname )
    return "(name+\".{}\").c_str()".format( varname )

def Address( row ):
    if row['Size']:
        return row['Varname'];
    else:
        return '&'+row['Varname'];

def MakeTypeToken( row ):
    if row['Datatype'] == "Int_t":
        return 'I'
    elif row['Datatype'] == "Float_t":
        return 'F'
    elif row['Datatype'] == "Bool_t":
        return 'O'
    elif row['Datatype'] == "Char_t" :
        return 'C'
    elif row['Datatype'] == "ULong64_t" :
        return 'l'
    elif re.match('std::vector\<.*\>\*' , row['Datatype'] ):
        return None
    elif re.match('std::vector\<.*\>' , row['Datatype'] ):
        return 'V'
    else:
        raise Exception("Unkown variable type in entry " + str(row) )

def MakeLeaf( row ):
    token = MakeTypeToken( row )

    single_format= "(name+\"{}/{}\").c_str()"
    fixed_format = "(name+\".{}[{}]/{}\").c_str()"
    leaf_format  = "(name+\".{}[\"+name+\".{}]/{}\").c_str()"
    varname      = row['Varname']
    size         = row['Size']

    ## No particular action for vector related variables
    if not token or token == 'V' :
        return None

    if not row['Size'] :
        return single_format.format( varname, token )
    if size== 'MAX_BX' :
        return leaf_format.format( varname, 'nBX', token )
    elif re.match('HLT.*' , varname ):
        return leaf_format.format( varname, 'nHLT', token )
    elif varname == 'TrgBook' :
        return leaf_format.format( varname, 'nTrgBook' , token )
    elif size == 'MAX_LHE':
        return leaf_format.format( varname, 'LHESize' , token )
    elif size.isdigit():
        return fixed_format.format( varname, size, token );
    else:
        return leaf_format.format( varname, 'Size' , token )

def MakeVariablePart( reader ):
    ans = ''
    for row in reader :
        if row['Size']:
            ans += "{} {} [{}];\n".format( row['Datatype'] , row['Varname'], row['Size'] )
        else:
            ans += "{} {};\n".format( row['Datatype'] , row['Varname'] )
    return ans.rstrip()

def MakeRegisterFunction( reader , default_name ):
    var_format = "root->SetBranchAddress( {} , {} );\n"
    statementlist = ""
    for row in reader:
        var_line = ""
        if re.match( 'std::vector.*\*' , row['Datatype'] ) :
            var_line = "{}=0;\n".format( row['Varname']  );
        elif re.match( 'std::vector.*' , row['Datatype'] ):
            continue;
        var_line      += var_format.format( BranchName(row), Address(row) )
        statementlist += var_line
    return """
    void Register( TTree* root, const std::string& name=\"{}\" ){{
        {}
    }}""".format( default_name, statementlist.strip() )

def MakeRegisterTreeFunction( reader, default_name ):
    statementlist = ""
    for row in reader :
        branchname = BranchName( row )
        address    = Address( row )
        leafname   = MakeLeaf( row )
        token      = MakeTypeToken(row)
        if leafname:
            statementlist += "root->Branch({},{},{});\n".format( branchname, address, leafname)
        elif token:
            statementlist += "root->Branch({},{});\n".format( branchname, address )
    return """
    void RegisterTree( TTree* root, const std::string& name=\"{}\"){{
        {}
    }}""".format( default_name, statementlist.strip() )

def MakeClassString( inputfile, class_name, default_name ):
    myreader = ListFromFile( inputfile );
    varstr   = MakeVariablePart( myreader );
    rtfunc   = MakeRegisterTreeFunction( myreader , default_name )
    rfunc    = MakeRegisterFunction( myreader, default_name )
    return """
    class {} {{
    public:
        {}
        {}
        {}
    }};
    """.format( class_name , varstr, rtfunc, rfunc )


if __name__ == "__main__":
    print MakeClassString( 'test.csv', 'EvtInfoBranches' , 'EvtInfo' )
