/*

 compile the code with

 g++ data_types.cpp -o data_types -Wall

*/

// include headers
#include <iostream>
#include <limits.h>
#include <float.h>

// the cout command resides in a so-called namespace in order
//   to use it globally we have define it
using namespace std;


int main()
{

  //
  //Basic data types
  //

  // inteter types with different capacity
  // type exists in a singned and unsigned version
  // if nothing is specified 'signed' is assumed by default
  // NOTE: the only exception to this the the char type.
  //       here signed has to be specified explicitly
  
    signed char  achar   = -1 ;
  unsigned char  auchar  =  10;
  
           short ashort  = -5000;
 unsigned short aushort =   5000;

           int   anint   = -128000;
  unsigned int   auint   =  256000;

           long  along   = -1000000000;
  unsigned long  aulong  = 1000000;
  
  // limits and sizes of the different variables
  // limits are defined in 'limits.h'
  cout << "=====| Integer types |=================================" << endl;
  cout << endl;
  cout << "size of char:   " << sizeof(char) << " byte" << endl;
  cout << "Limits of char:          " << SCHAR_MIN << " .. " << SCHAR_MAX << endl;
  cout << "Limits of unsigned char: " << 0 << " .. " << UCHAR_MAX << endl;
  cout << endl;

  cout << "size of short:   " << sizeof(short) << " byte" << endl;
  cout << "Limits of short:          " << SHRT_MIN << " .. " << SHRT_MAX << endl;
  cout << "Limits of unsigned short: " << 0 << " .. " << USHRT_MAX << endl;
  cout << endl;

  cout << "size of int:   " << sizeof(int) << " byte" << endl;
  cout << "Limits of int:          " << INT_MIN << " .. " << INT_MAX << endl;
  cout << "Limits of unsigned int: " << 0 << " .. " << UINT_MAX << endl;
  cout << endl;
  
  cout << "size of long:   " << sizeof(long) << " byte" << endl;
  cout << "Limits of long:          " << LONG_MIN << " .. " << LONG_MAX << endl;
  cout << "Limits of unsigned long: " << 0 << " .. " << ULONG_MAX << endl;
  cout << endl << endl;

  // floating point types with different capacity
  float  afloat = 3.1415926;
  
  double adouble = 5.2e-30;
  
  cout << "=====| Floating point types |============================" << endl;
  cout << endl;
  cout << "size of float:       " << sizeof(float) << " byte" << endl;
  cout << "Limits of float:     " << FLT_MIN << " .. " <<FLT_MAX << endl;
  cout << "Precision of float:     " <<FLT_EPSILON << endl;
  cout << endl;
  
  cout << "size of double:      " << sizeof(double) << " byte" << endl;
  cout << "Limits of double:    " << DBL_MIN << " .. " << DBL_MAX << endl;
  cout << "Precision of double:     " <<DBL_EPSILON << endl;
  cout << endl;
  
  return 0;
}
