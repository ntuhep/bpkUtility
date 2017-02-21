/*******************************************************************************
 *
 *  Filename    : dump_hlt.cc
 *  Description : Helper class for dumping hlt information
 *  Author      : Yi-Mu "Enoch" Chen [ ensc@hep1.phys.ntu.edu.tw ]
 *
*******************************************************************************/
#include "bpkFrameWork/bprimeKit/interface/Types.h"

#include "DataFormats/FWLite/interface/Event.h"
#include "DataFormats/FWLite/interface/Handle.h"

#include "TFile.h"

#include <vector>
#include <string>
#include <iostream>
using namespace std;

int main(int argc , char* argv[] )
{
   fwlite::Event ev( TFile::Open(argv[1]) );
   fwlite::Handle<edm::TriggerResults>        trigger_handle;

   for( ev.toBegin(); !ev.atEnd() ; ++ev ){
      trigger_handle.getByLabel( ev, "TriggerResults", "", "HLT" );
      const auto& trgnames = ev.triggerNames( *trigger_handle );
      for( unsigned i = 0 ; i < trgnames.size() ; ++i ){
         const string trgname = trgnames.triggerName(i);
         unsigned trgidx = trgnames.triggerIndex( trgname );
         cout << trgidx << " " << trgname << " "
            << trigger_handle->wasrun(trgidx) << " "
            << trigger_handle->accept(trgidx) << " "
            << trigger_handle->error(trgidx) << endl;
      }

   }
}
