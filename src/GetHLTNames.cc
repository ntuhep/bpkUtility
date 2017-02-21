/*******************************************************************************
*
*  Filename    : GetHLTNames.cc
*  Description : Dumping HTLName of a file into a string array
*  Author      : Yi-Mu "Enoch" Chen [ ensc@hep1.phys.ntu.edu.tw ]
*
*******************************************************************************/
#include "bpkFrameWork/bprimeKit/interface/Types.h"

#include "DataFormats/FWLite/interface/Event.h"
#include "DataFormats/FWLite/interface/Handle.h"

#include "TFile.h"

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

vector<string>
GetHLTNames(
   const string& filename,
   const string& modulelabel,
   const string& productlabel,
   const string& processlabel
   )
{
   fwlite::Event ev( TFile::Open( filename.c_str() ) );
   fwlite::Handle<edm::TriggerResults> trigger_handle;

   vector<string> ans;

   for( ev.toBegin(); !ev.atEnd(); ++ev ){
      trigger_handle.getByLabel( ev, modulelabel.c_str(), productlabel.c_str(), processlabel.c_str() );
      const auto& trgnames = ev.triggerNames( *trigger_handle );

      for( unsigned i = 0; i < trgnames.size(); ++i ){
         ans.push_back( trgnames.triggerName( i ) );
      }

      std::sort( ans.begin(), ans.end() );
      ans.erase( std::unique( ans.begin(), ans.end() ), ans.end() );
   }

   return ans;
}
