/*******************************************************************************
 *
 *  Filename    : obj_probe.cc
 *  Description : Main function for dumping file contents by FWlite
 *  Author      : Yi-Mu "Enoch" Chen [ ensc@hep1.phys.ntu.edu.tw ]
 *
*******************************************************************************/
#include "DataFormats/FWLite/interface/Event.h"
#include "DataFormats/FWLite/interface/Handle.h"
#include "DataFormats/PatCandidates/interface/Photon.h"

#include "TFile.h"

#include <iostream>
using namespace std;

int main(int argc, char* argv[] )
{
   fwlite::Event ev( TFile::Open("./signal.root") );
   fwlite::Handle<std::vector<pat::Photon> >  photon_handle;

   unsigned i = 0 ;
   for( ev.toBegin(); !ev.atEnd() && i < 100 ; ++ev , i++){
      cout << "At event" << i << flush;
      photon_handle.getByLabel( ev, "slimmedPhotons");
      const auto& photon_list = *photon_handle;

      cout << ", Photon list size: " << photon_list.size() << endl;
   }

   return 0;
}
