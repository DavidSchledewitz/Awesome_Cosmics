/*

compile the code with

g++ control_structures.cpp -o control_structures -Wall
 
*/

// include a header file, needed for the cout command
#include <iostream>

// the cout command resides in a so-called namespace
// in order to use it globally we have to let the compiler know
using namespace std;

int main()
{
  //
  // ===| if, else if, else | ============================
  //

  // every condition other than '0' is interpreted as fulfilled (true)
  if (0) {
    cout << "This code will never be executed" << endl;
  }

  if (1) {
    cout << "This code will always be executed" << endl;
  }

  // it is recommended to use a code block {} after if
  // if this is not done, only the next line will be handled by if
  if (0)
    cout << "this line is handled by the if and will not be executed" << endl;
  cout << "this line is not handled by the if" << endl;

  int valueToBeCheckedInIf=10;

  if ( valueToBeCheckedInIf<10 ) {
    cout << "Value is smaller than 10" << endl;
  } else if ( valueToBeCheckedInIf>=10 && valueToBeCheckedInIf<20 ) {
    cout << "Value is between 10 and 20" << endl;
  } else {
    cout << "Value is larger than 20" << endl;
  }

  // ===| switch structure | ============================
  // this can only be used with integer values
  // the cases are caught with the 'case' keyword. everything after 'case' will
  //   be executed unless 'break' is issued.
  //   if none of the 'case'es are fulfilled everything after 'default' will
  //   be executed
  //
  
  int value=2;
  
  switch (value) {
    case 0:
      cout << "value is 0" << endl;
      break; // leave the switch structure
    case 1:
      cout << "value is 1" << endl;
    case 2:
      cout << "value is 1 or 2" << endl;
      break;
    default:
      cout << "value is none of 0,1,2" << endl;
  }
  
  //
  // ===| for loop | ============================
  //
  
  for (int i=0; i<10; ++i) {
    cout << "Iteration " << i << "inside the for loop" << endl;
  }

  // ===| while loop | ============================
  // the loop is only entered if the initial statement is true

  int counter=0;

  // this loop is not executed
  while ( counter>=2 && counter<10 ) {
    cout << "1st while loop counter: " << counter << endl;
    ++counter;
  }

  counter=2;
  // this loop is executed
  while ( counter>=2 && counter<10 ) {
    cout << "2nd while loop counter: " << counter << endl;
    ++counter;
  }
  
  // ===| do .. while loop | ============================
  // the loop is entered at least once
  // do .. while loops are used very rarely
  
  counter=0;
  
  do{
    cout << "do loop counter: " << counter << endl;
    ++counter;
  } while ( counter>=2 && counter<10 );
  
  // ===| break and continue | ============================
  // the break statement leaves the current loop
  // the continue statement goes into the next iteration of a loop

  counter=0;

  // without the break statement in the if clause, the loop would go up to 10
  while ( counter<10 ) {
    if (counter==5) break;
    cout << "while loop counter (with break): " << counter << endl;
    ++counter;
  }

  counter=0;
  
  // without the continue statement in the if clause,
  //   the loop would write all values up to 10
  while ( counter<10 ) {
    if ( counter>2 && counter<8 ) {
      ++counter; // we need to increase the counter here as well
                 // otherwise we would execute this loop infinitely
      continue;
    }
    cout << "while loop counter (with continue): " << counter << endl;
    ++counter;
  }
  
  
  return 0;
}
