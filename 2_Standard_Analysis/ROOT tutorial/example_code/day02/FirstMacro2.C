#include <iostream>

using namespace std;

void FirstMacro2()
{
  cout << "My first macro" << endl;
}

float myFunctionOne(float value, float multiplicator)
{
  float returnValue=value*multiplicator;
  cout << value << " * " << multiplicator << " = " << returnValue << endl;
  return returnValue;
}


