#include <TF1.h>
#include <TTree.h>
#include <TFile.h>
#include <TRandom.h>
#include <TGraph.h>
#include <TCanvas.h>

/*
To load nd compile the macro: 
.L trees.C+  

Now you can call the functions inside the ROOT prompt

*/

// ------- Functions to read and write existing data ------
void writeDataToTree(){

  //open a ROOT file to write 
  TFile f("fileData.root","recreate");

  //create a TTree and store the content of vertex.dat into it
  TTree t("mytree","mytree");
  t.ReadFile("../../example_code/day04/vertex.dat","x:y:z");
  
  //write the TTree into the ROOT file
  t.Write();
  
  //close the ROOT file
  f.Close();
  
}

void readDataFromTree(){
  
  //call writeDataToTree() before this function
  
  //open the ROOT file to read
  TFile *f = new TFile("fileData.root");
  if (!f->IsOpen()) {cout<<"problems with file, exiting"<<endl; return;}
  //retrieve the TTree inside using a casting
  TTree *t = (TTree *)f->Get("mytree");
  if(!t) {cout<<"no TTree found"<<endl; return;}
  //print the content of the TTree
  t->Print();

  //Examples of Drawing
  TCanvas *c1 = new TCanvas();
  c1->Divide(2);
  c1->cd(1);
  t->Draw("x:y","x>0","colz");
  c1->cd(2);
  t->Draw("x:z:y","","colz");
  c1->SaveAs("data.png");
  //close the ROOT file
  f->Close();

}

// ------- Functions to create data and read them back ------

void createComplexTree(){

// Create a tree with two branches	
// One branch is a simple number (random from a gaussian distribution)
// One Branch holding TGraphs (only few points)
// Draw data using the 'draw' function
// Read back both branches using the branch address

  TFile f("fileDataComplex.root","recreate");
  //create a tree
  TTree t("myComplexTree","myComplexTree");

  // One branch is a simple number 
  Float_t ranGaus = 0;
  t.Branch("ranGaus",&ranGaus);

  //One Branch holds TGraphs 
  TGraph *myGraph = new TGraph();
  t.Branch("ranGraph",&myGraph);

  Int_t numEntries = 1;
  //fill 100 branches
  for( Int_t i = 0 ; i < 100; ++i ) {
    //first branch
    ranGaus = gRandom -> Gaus();

    // generate the number of entries for one graph:
    // in this example each graph can have between 1 and 10 points
    numEntries = (int)1+10*gRandom -> Uniform();
    //second branch
    for( Int_t j = 0 ; j < numEntries ; ++j ) { 
      myGraph->SetPoint(j, gRandom -> Uniform(), gRandom -> Uniform());
    }
    t.Fill();
  }

  
  t.Print();
  t.Write();
  f.Close();
}

void readComplexTree(){

  //open the ROOT file and get the TTree
  TFile f("fileDataComplex.root");
  if (!f.IsOpen()) {cout<<"problems with file, exiting"<<endl; return;}
  TTree *t = (TTree *)f.Get("myComplexTree");
  if(!t) {cout<<"no TTree found"<<endl; return;}

  //create the variables for the branches and set their address
  Float_t ranGaus = 0;
  t->SetBranchAddress("ranGaus",&ranGaus);
  TGraph *myGraph = new TGraph();
  t->SetBranchAddress("ranGraph",&myGraph);

  // loop over all the entries of the TTree
   for( Int_t i = 0 ; i < t ->GetEntries(); ++i ) {
     //load the entry
     t->GetEntry(i);
     //print the value
     cout<<ranGaus<<" ";
     // draw the graph -
     // note that in this example only the last one
     // will be displayed in the canvas
     myGraph->Draw("*ap");
    }
  
   cout<<" "<<endl;
   f.Close();
    
}
