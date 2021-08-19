/*

compile the code with

g++ functions.cpp -o functions -Wall

*/

// include a header file, needed for the cout command
#include <iostream>

// the cout command resides in a so-called namespace
// in order to use it globally we have to let the compiler know
using namespace std;

float average(float values[], int arraySize)
{
  //
  // this function calculates the average of all values in the array 'values'
  // the the number of values in the array is 'arraySize'
  //

  //sanity check if there is anything to calculate
  if (arraySize==0) return 0.;

  // sum up all values
  float sum=0;
  for (int iValue=0; iValue<arraySize; ++iValue) {
    sum+=values[iValue];
  }

  // build average
  sum/=arraySize;

  return sum;
}

int main()
{
  //define values
  float values[5]={1.,1.5,2.5,2.8,3.2};
  //get the average of the values using the function 'average'
  float valuesAverage = average(values,5);
  //print the result
  cout << "The average of the values: ";
  for (int iValue=0; iValue<5; ++iValue) cout << values[iValue] << ", ";
  cout << "is: "<< valuesAverage << endl;
  
  return 0;
}
