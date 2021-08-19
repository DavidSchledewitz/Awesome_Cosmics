/*

compile the code with

g++ variables.cpp -o variables -Wall
 
*/

// include a header file, needed for the cout command
#include <iostream>

// the cout command resides in a so-called namespace
// in order to use it globally we have to let the compiler know
using namespace std;

int main()
{
  // type name
  // not initialised -> compiling with -Wall will give a warning
  int myvar;

  // variables should always be initialised:
  int myvar2=2;

  // another possibility for initialisation is the so-called 'constructor initialisation'
  // both are equivalent and a matter of taste imo
  int myvar3(3);

  //in c++11 one can use also the following: 
  // int myvar4{4};
  //to test it include the -std=c++11 option in the compilation
  
  cout << "myvar:  " << myvar  << endl;
  cout << "myvar2: " << myvar2 << endl;
  cout << "myvar3: " << myvar3 << endl;
  // cout << "myvar4: " << myvar4 << endl;
  return 0;
}
