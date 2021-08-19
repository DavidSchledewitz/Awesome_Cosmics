#include <TFile.h>
#include <TTree.h>
#include <TRandom.h>

#include <myEvent.h>
#include <myParticle.h>

/*
gSystem->Load("../../example_code/day05/libMyPackage.so")
gSystem->AddIncludePath("-I../../example_code/day05/code")
.L macros/simpleGenerate.C++
simpleGenerate(100,1000);
*/

//____________________________________________________________________________________________________
void simpleGenerate(Int_t nevents, Int_t nparticles)
{
  //
  // for testing purposes:
  // generate a number of events adding to each event a number of partiles
  //
  

  myParticle particle;
  myEvent    *event = new myEvent;

  TFile outputFile("testEvents.root","recreate");
  TTree eventTree("events","My generated events");
  eventTree.Branch("event",&event);

  for (Int_t ievent=0; ievent<nevents; ++ievent){
    event->SetVx(gRandom->Gaus(0,7));

    // add particles to the event
    for (Int_t iparticle=0; iparticle<nparticles; ++iparticle) {
      particle.SetPx(gRandom->Uniform(-10,10));
      event->AddParticle(particle);
    }
    eventTree.Fill();
    event->Reset();
  }

  outputFile.Write();
  outputFile.Close();
}
