/*

compile the code with

g++ variables_valid.cpp -o variables_valid -Wall
 
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

  {
    //myvar2 is only valid inside this code block enclosed by {}
    int myvar2=2;

    // myvar is valid here, since this code block is enclosed in the code block
    // of the main function
    cout << "myvar:  " << myvar  << endl;
    cout << "myvar2: " << myvar2 << endl;
  }
  
  cout << "myvar:  " << myvar  << endl;

  // this line will give a compiler error, since myvar2 is not valid here
  cout << "myvar2: " << myvar2 << endl;
  return 0;
}
