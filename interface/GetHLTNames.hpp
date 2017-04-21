/*******************************************************************************
 *
 *  Filename    : GetHLTNames.hpp
 *  Description : Simple function for Dumping HLT Names by FWLite
 *  Author      : Yi-Mu "Enoch" Chen [ ensc@hep1.phys.ntu.edu.tw ]
 *
*******************************************************************************/
#ifndef BPKFRAMEWORK_BPKUTILITY_GETHLTNAMES_HPP
#define BPKFRAMEWORK_BPKUTILITY_GETHLTNAMES_HPP

#include<vector>
#include<string>
#include <map>

extern std::vector<std::string> GetHLTNames(
   const std::string& edmfilename,
   const std::string& modulelabel,
   const std::string& productlabel="",
   const std::string& processlabel=""
);

#include <boost/python.hpp>

//------------------------------------------------------------------------------
//   Help class for vector construction
//   Note: Do note add `const` keyword, CMSSW has too many type restrictions
//------------------------------------------------------------------------------
void IndexError() { PyErr_SetString( PyExc_IndexError, "Index out of range" ); }

template<class T>
struct vector_item {
   typedef typename T::value_type V;

   static V& get( T& x, int i )
   {
      if( i < 0 ) { i += x.size(); }
      if( i >= 0 && (unsigned)i < x.size() ) { return x[i]; }
      else { IndexError(); return x[0]; }
   }
   static void set( T& x, int i, V& v )
   {
      if( i < 0 ) { i += x.size(); }
      if( i >= 0 && (unsigned)i < x.size() ) { x[i] = v; }
      else { IndexError(); }
   }
   static void del( T& x, int i )
   {
      if( i < 0 ) { i += x.size(); }
      if( i >= 0 && (unsigned)i < x.size() ) { x.erase( x.begin() + i ); }
      else { IndexError(); }
   }
   static void add( T& x, V& v )
   {
      x.push_back( v );
   }

   static bool in( T& x, V& v ) {
      return find_eq( x.begin, x.end, v ) != x.end();
   }
   static int index( T& x, V& v ) {
      int i = 0;
      for( typename T::const_iterator it = x.begin; it != x.end(); ++it, ++i )
         if( *it == v ) { return i; }
      return -1;
   }
};

//------------------------------------------------------------------------------
//   Helper class for map construction
//------------------------------------------------------------------------------
void KeyError() { PyErr_SetString( PyExc_KeyError, "Key not found" ); }

template<class T>
struct map_item {
   typedef typename T::key_type K;
   typedef typename T::mapped_type V;
   static V& get( T const& x, K const& i ) {
      if( x.find( i ) != x.end() ) { return x[i]; }
      KeyError();
   }
   static void set( T const& x, K const& i, V const& v ) {
      x[i] = v; // use map autocreation feature
   }
   static void del( T const& x, K const& i ) {
      if( x.find( i ) != x.end() ) { x.erase( i ); }
      else { KeyError(); }
   }
   static bool in( T const& x, K const& i ) {
      return x.find( i ) != x.end();
   }
};

//------------------------------------------------------------------------------
//   MACRO short hands
//------------------------------------------------------------------------------
#define MAKE_VECTOR_WRAPPER( CPP_NAME , PYTHON_NAME )                                        \
   boost::python::class_< CPP_NAME >( #PYTHON_NAME )                                         \
      .def("__len__"     , & CPP_NAME::size)                                                 \
      .def("clear"       , & CPP_NAME::clear)                                                \
      .def("append"      , & vector_item< CPP_NAME >::add                                    \
            , boost::python::with_custodian_and_ward<1, 2>())                                \
      .def("__setitem__" , & vector_item< CPP_NAME >::set                                    \
            , boost::python::with_custodian_and_ward<1, 2>())                                \
      .def("__getitem__" , & vector_item< CPP_NAME >::get                                    \
            , boost::python::return_value_policy<boost::python::copy_non_const_reference>()) \
      .def("__delitem__" , & vector_item< CPP_NAME >::del)                                   \
      .def("__iter__"    , boost::python::iterator< CPP_NAME >() )                           \
   ;


#define MAKE_MAP_WRAPPER( CPP_NAME , PYTHON_NAME )                                           \
   boost::python::class_<CPP_NAME>( #PYTHON_NAME )                                                     \
      .def("__len__", &Layer::size)                                                          \
      .def("clear", &Layer::clear)                                                           \
      .def("__getitem__", &map_item<Layer>::get                                              \
            , boost::python::return_value_policy<boost::python::copy_non_const_reference>()) \
      .def("__setitem__", &map_item<Layer>::set                                              \
            , boost::python::with_custodian_and_ward<1,2>())                                 \
      .def("__delitem__", &map_item<Layer>::del)                                             \
   ;

#endif /* end of include guard: BPKFRAMEWORK_BPKUTILITY_GETHLTNAMES_HPP */
