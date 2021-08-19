/*

compile the code with

g++ meanSigma.cpp -o meanSigma -Wall

*/

// include a header file, needed for the cout command
#include <iostream>
#include <cmath>

// the cout command resides in a so-called namespace
// in order to use it globally we have to let the compiler know
using namespace std;

void meanSigma(double values[], int arraySize, double &mean, double &sigma)
{
  //
  // this function calculates the mean and sigma of all values in the array 'values'
  // the the number of values in the array is 'arraySize'
  //
  // NOTE: In ROOT, the name "RMS" is often misused in histograms!
  // The RMS in ROOT is not the "real" root-mean-square (:= sqrt( 1/n sum_i ( x_i^2 ) )), but rather
  // the sigma (:= sqrt( 1/n sum_i ( x_i - mean )^2 ) = sqrt( 1/n sum_i ( x_i^2 ) - mean^2  )

  // reset the variables
  mean=0;
  sigma=0;
  
  //sanity check if there is anything to calculate
  if (arraySize==0) return;

  // sum up all values
  for (int iValue=0; iValue<arraySize; ++iValue) {
    mean+=values[iValue];
    sigma+=values[iValue]*values[iValue];
  }

  // build average and sigma
  mean/=arraySize;
  sigma/=arraySize;
  sigma=sqrt(abs( sigma - mean*mean));
}

int main()
{
  //define values
  double values[5]={1.,1.5,2.5,2.8,3.2};
  //get the average of the values using the function 'average'
  double mean=0;
  double sigma=0;

  meanSigma(values,5,mean,sigma);
  //print the result
  cout << "The mean and sigma of the values: ";
  for (int iValue=0; iValue<5; ++iValue) cout << values[iValue] << ", ";
  cout << "are: "<< mean << " and " << sigma << endl;
  
  return 0;
}
