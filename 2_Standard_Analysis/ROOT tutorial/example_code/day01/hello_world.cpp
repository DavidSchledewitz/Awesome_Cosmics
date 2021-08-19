/*

compile the code with

g++ hello_world.cpp -o hello_world -Wall
 
*/

// include a header file, needed for the cout command
#include <iostream>

// the cout command resides in a so-called namespace
// in order to use it globally we have to let the compiler know
using namespace std;

int main()
{
  cout << "hello world" << endl;
  return 0;
}
