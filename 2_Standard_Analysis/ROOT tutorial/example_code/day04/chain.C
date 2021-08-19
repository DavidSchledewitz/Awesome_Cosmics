#include <TChain.h>
#include <TFile.h>
#include <TF1.h>
#include <TLorentzVector.h>
#include <TMath.h>
#include <TString.h>
#include <TTree.h>
#include <TRandom.h> // needed for gRandom

/*

// load with
.L chain.C+

// first create the trees to be chained:
createData();

//Then make a chain out of the trees and draw something
TChain *tree=chain();
TCanvas c;
c.Divide(2,2);
c.cd(1);
gPad->SetLogy();
tree->Draw("particle.Pt()");
c.cd(2);
TH1F hEta("hEta","Eta distribution;#eta;entries",30,-1.5,1.5);
tree->Draw("particle.Eta()>>hEta");
c.cd(3);
tree->Draw("particle.Pt():particle.Eta()>>hPtEta(25,-1.25,1.25,30,0,6)","","colz");
c.cd(4);
//draw using directly the data members
tree->Draw("particle.fP.fY:particle.fP.fX");


*/

TChain* chain(Int_t nFiles=10)
{
  //
  // it is possible to 'chain' root file with trees which contain the same structure
  // The class use is a TChain which interits from TTree and thus has the same
  // functionality. A chain can be used like a tree
  //

  // create a chain and add all files which contain the particleTrees
  // NOTE: then name of the chain must be the name of the tree!
  //       otherwise the tree is not found inside the file
  TChain *c=new TChain("particleTree");
  // add all files to the chain
  for (Int_t ifile=0; ifile<nFiles; ++ifile){
    TString fileName("particleTree");
    fileName+=ifile;
    fileName+=".root";
    c->AddFile(fileName.Data());
  }

  return c;
}

//_____________________________________________________________
void writeTree(Int_t fileNumber, Int_t nparticles)
{
  // write a tree into a file with fileNumber
  // create nparticles in this tree

  // First open the file to associate the tree with the file
  TString fileName("particleTree");
  fileName+=fileNumber;
  fileName+=".root";

  TFile f(fileName.Data(),"recreate");
  
  TTree t("particleTree","A tree with particles");
  TLorentzVector *v=new TLorentzVector;
  // create a branch to hold the TLorentzVector
  t.Branch("particle",&v);
  // crate a function that parametrises the transverse momentum distributions of pions
  TF1 fpt("fpt",Form("x*(1+(sqrt(x*x+%f^2)-%f)/([0]*[1]))^(-[0])*[2]",0.14,0.14),0.3,100);
  fpt.SetParameters(7.24,0.120,3);
  fpt.SetNpx(200);
  
  // create the particles and fill them in the tree
  for (Int_t i=0; i<nparticles; ++i) {
    Double_t phi = gRandom->Uniform(0.0, 2*TMath::Pi());
    Double_t eta = gRandom->Uniform(-1, 1);
    Double_t pt  = fpt.GetRandom();
    v->SetPtEtaPhiE(pt,eta,phi,.14);
    t.Fill();
  }

  f.Write();
  f.Close();

  delete v;
}

//_____________________________________________________________
void createData(Int_t nFiles=10)
{
  //
  // create 'nFiles' root files with particles trees
  //

  for (Int_t ifile=0; ifile<nFiles; ++ifile){
    writeTree(ifile,gRandom->Uniform(10000,100000));
  }
}
