#ifndef myEvent_H
#define myEvent_H

#include <TObject.h>
#include <TClonesArray.h>

#include "myParticle.h"

class myParticle;

class myEvent : public TObject {
public:
  myEvent();
  myEvent(const myEvent &ev);
  virtual ~myEvent();

  void SetVx(Double_t vx) { fVx = vx; }
  Double_t GetVx() const { return fVx; }

  void Reset();
  
  Int_t GetNumberOfParticles() const { return fParticles.GetEntriesFast(); }
  
  myParticle* AddParticle(const myParticle &particle);
  const myParticle& GetParticle(Int_t iparticle) const { return *static_cast<const myParticle*>(fParticles.At(iparticle)); }
  
private:
  Double_t fVx;                // x vertex of the event

  TClonesArray fParticles;     // array of particles

  // Define the class for the dictionary
  ClassDef(myEvent,1);         // event information
};


#endif
