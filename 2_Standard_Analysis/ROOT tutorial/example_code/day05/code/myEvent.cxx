// root include files

// include files of this package
// #include "myParticle.h"

#include "myEvent.h"

ClassImp(myEvent)

myEvent::myEvent()
: TObject()
, fVx(0.)
, fParticles("myParticle")
{
  // default constructor
}

//______________________________________________________________
myEvent::myEvent(const myEvent &ev)
: TObject(ev)
, fVx(ev.fVx)
, fParticles(ev.fParticles)
{
  // copy constructor
}

//______________________________________________________________
myEvent::~myEvent()
{
  // destructor
}

//______________________________________________________________
void myEvent::Reset()
{
  // reset the current event information
  // clean the particle buffer
  // and reset variables
  fParticles.Clear("C");
  fVx=0.;
}

//______________________________________________________________
myParticle* myEvent::AddParticle(const myParticle &particle)
{
  // add a particle to the particle array
  // check before if the size of the array is large enough
  // and expand it if necessary
  if (fParticles.GetEntriesFast()>=fParticles.Capacity()) fParticles.Expand(2*fParticles.Capacity());
  return new(fParticles[fParticles.GetEntriesFast()]) myParticle(particle);
  
}

