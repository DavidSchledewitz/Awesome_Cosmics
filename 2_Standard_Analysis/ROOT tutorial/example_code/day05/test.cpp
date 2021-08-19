#include "myEvent.h"
#include <iostream>
/*

.L libMyPackage.so
gSystem->AddIncludePath("-I./code")
.L test.cpp++

*/


int createEvent()
{
  myEvent ev;
  ev.SetVx(2);
  std::cout<<ev.GetVx()<<std::endl;
  return 1;
}
