

#include "myParticle.h"

ClassImp(myParticle)

myParticle::myParticle()
: TObject()
, fPx(0.)
{
  // default constructor
}

//______________________________________________________________
myParticle::myParticle(const myParticle &ev)
: TObject(ev)
, fPx(ev.fPx)
{
  // copy constructor
}

//______________________________________________________________
myParticle::~myParticle()
{
  // destructor
}

