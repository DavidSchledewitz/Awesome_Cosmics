#ifndef myParticle_H
#define myParticle_H

#include <TObject.h>

// define the class and make it inherit from TObject so that
// we can write it to a ROOT file
class myParticle : public TObject {
public:
  myParticle();
  myParticle(const myParticle &ev);
  virtual ~myParticle();

  void SetPx(Double_t px) { fPx=px; }

  Double_t GetPx() const { return fPx; }
private:
  Double_t fPx;                // x momentum of the particle
  
  // Define the class for the dictionary
  ClassDef(myParticle,1);      // particle information
};


#endif
