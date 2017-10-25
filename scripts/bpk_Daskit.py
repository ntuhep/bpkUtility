#!/usr/bin/env python

from das_client import get_data as das_query
from optparse import OptionParser
from multiprocessing import Process, Manager
import os, sys
import json
import time
from random import random
#-------------------------------------------------------------------------------------
import pwd
def x509 ():
    "Helper function to get x509 either from env or tmp file"
    x509 = os.environ.get('X509_USER_PROXY', '')
    if  not x509:
        x509 = '/tmp/x509up_u%s' % pwd.getpwuid( os.getuid() ).pw_uid
        if  not os.path.isfile(x509):
            return ''
    return x509
#-------------------------------------------------------------------------------------
def Option_Parser():
    usage='usage: %prog [options] arg\n'
    usage+='Please use -d or --dataset to input the name of dataset you want.\n'
    usage+='If your input name has "*", the script will print all datasets satisfied this name ONLY.\n'
    usage+='If your input name has a complete name, the script will show the all corresponding CMSSW releases and global tags and you can use other args.'
    parser = OptionParser(usage=usage)
    parser.add_option('-d','--dataset',
            type='str',dest='dataset',
            help='input your dataset like /ZMM*/*/MINIAOD'
            )
    parser.add_option('--getLumiSection',
            action='store_true', dest='getLumiSection',
            help='output a txt file with run number and lumi section'
            )
    parser.add_option('--instance',
            type='str',dest='instance',default='prod/global',
            help='choose instance'
            )
    parser.add_option('--getTestfile',
            action='store_true', dest='getTestfile',
            help='download a test file with more than 5000 events'
            )
    parser.add_option('-o','--outpath',
            type='str',dest='outpath',default='.',
            help='output site for any output file you specify'
            )
    (options, args) = parser.parse_args()
    return options

def info_list (query):
    host = 'https://cmsweb.cern.ch'
    idx = 0
    limit = 0
    debug = False
    response = das_query(host,query,idx,limit,debug,ckey=x509(),cert=x509())
    if response['status'] == 'ok':
        return response['data']
        #    print 'Can not find the information of corresponding dataset'
        #    print 'Please check the name you input !!'
        #    sys.exit()
    else:
        print 'Input wrong DAS format of dataset name!!'
        print 'Please check the name you input!!'
        sys.exit()

def download (query, outpath):
    for fileinfo in info_list('file ' + query):
        if int( fileinfo['file'][1]['nevents'] ) > 5000:
            os.system('xrdcp root://cms-xrd-global.cern.ch/%s %s' % (fileinfo['file'][0]['name'], outpath))
            break

def getlumi (query, lumi_dict):
    lumiinfo = info_list(query)
    runnumber = lumiinfo[0]['lumi'][0]['run_number']
    lumisection = lumiinfo[0]['lumi'][0]['number']
    for lumi in lumisection:
        lumi_dict[runnumber]+=list([lumi])

def main ():
    """Main function"""
    options = Option_Parser()
    if options.dataset == None:
        print 'Please input the name of dataset you want'
        sys.exit()

    query = 'dataset=%s instance=%s' % (options.dataset, options.instance)

    if query.find('*') == -1:
        config = info_list('config ' + query)
        try:
            datasetname = config[0]['config'][0]['dataset']
            conf_list = config[1]['config'];
        except:
            datasetname = config[1]['config'][0]['dataset']
            conf_list = config[0]['config'];

        print 'name : %s' % datasetname
        for conf in conf_list:
            print 'release : %s' % conf['release_version']
            print 'global tag : %s' % conf['global_tag']
        if (options.getTestfile):
            print 'Start to download a test file of %s' % datasetname
            download(query, options.outpath)
        if (options.getLumiSection):
            manager = Manager()
            lumi_dict = manager.dict()
            for run in info_list('run ' + query):
                lumi_dict[ run['run'][0]['run_number'] ] = []
            process_list = list()
            for fileinfo in info_list('file ' + query):
                p = Process(target=getlumi, args=('lumi file=%s' % fileinfo['file'][0]['name'], lumi_dict))
                process_list.append(p)
                p.start()
                time.sleep(random())
            for process in process_list:
                process.join()
            with open(options.outpath + '/' + datasetname.replace('/','') + '.txt','w') as f:
                json.dump(lumi_dict._getvalue(),f,sort_keys=True)
                print 'file have been produced!'
    else:
        for datainfo in info_list(query):
            print datainfo['dataset'][0]['name']


if __name__ == '__main__':
    main()
