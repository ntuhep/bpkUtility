/*******************************************************************************
 *
 *  Filename    : HLTNames_Boost.cc
 *  Description : Require to expost HLT Names to python
 *  Author      : Yi-Mu "Enoch" Chen [ ensc@hep1.phys.ntu.edu.tw ]
 *
*******************************************************************************/
#include "bpkFrameWork/bpkUtility/interface/GetHLTNames.hpp"
#include <boost/python.hpp>

using namespace boost::python;

BOOST_PYTHON_MODULE(pluginHLTNames)
{
   def( "GetHLTNames" , GetHLTNames );
   MAKE_VECTOR_WRAPPER( std::vector<std::string> , std_vector_string );
   MAKE_VECTOR_WRAPPER( std::vector<double>      , std_vector_double );
};
