

void SaveOneHistogram()
{
  // function to demonstrate how to save a histogram

  TH1F *h1 = new TH1F("h1","first",10,0,10);
  h1->Fill(1,2);
  h1->Fill(2,4);
  h1->Fill(3,3);
  h1->Fill(4,1);
  
  TFile f("myFirstRootFile.root","recreate");
  h1->Write();
  f.ls();
  f.Close();
}