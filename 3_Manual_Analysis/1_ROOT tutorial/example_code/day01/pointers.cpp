/*

compile the code with

g++ pointers.cpp -o pointers -Wall

*/

// include a header file, needed for the cout command
#include <iostream>

// the cout command resides in a so-called namespace
// in order to use it globally we have to let the compiler know
using namespace std;

void printPtrInfo(int *ptr)
{
  //
  // print pointer information:
  // the address the pointer is pointing to and the value at this address
  //
  
  cout << "The memory address is " << ptr << endl;

  // check if the pointer is pointing to a valid address
  if (ptr==0x0) return;
  cout << "The value stored is " << *ptr << endl;
}

int main()
{
  
  // === | pointers | ==============================
  //
  int myInt1 = 2;
  int myInt2 = 8;

  int * myIntPtr = 0x0;

  // using the reference operator (&)
  // assign the memory address of myInt1 to myIntPtr
  myIntPtr = &myInt1;
  printPtrInfo(myIntPtr);

  // assign the memory address of myInt1 to myIntPtr
  myIntPtr = &myInt2;
  printPtrInfo(myIntPtr);

  // using the dereference operator (*)
  // assign a value to myInt2 via the pointer
  *myIntPtr = 4;
  cout << "New value of myInt2 is " << myInt2 << endl;
  printPtrInfo(myIntPtr);

  // === | references | ==============================
  // similar to pointers

  int myInt3     = 7;
  // create a reference to myInt3
  int & myInt3Ref = myInt3;

  //print the values of myInt3 and the reference to it
  // references are accessed like simple variables
  cout << "The value of myInt3 is " << myInt3 << endl;
  cout << "The value of the reference is " << myInt3Ref << endl;

  // change the value of myInt3 via its reference
  myInt3Ref=1000;
  //print the values of myInt3 and the reference to it
  cout << "The value of myInt3 is " << myInt3 << endl;
  cout << "The value of the reference is " << myInt3Ref << endl;
  
  return 0;
}
