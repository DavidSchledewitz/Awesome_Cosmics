void Histograms(){

  //histogram with uniforn distribution 
  TH1F *uniHist = new TH1F("uniHist","uniHist",100,-10,10);
  uniHist->FillRandom("pol0",10000);

  //histogram with gaussian distribution
  TH1F *gausHist = new TH1F("gausHist","gausHist",100,-10,10);
  gausHist->FillRandom("gaus",1000);

  //histograms for the sum 
  TH1F *sumHist = new TH1F("sumHist","sumHist",100,-10,10);

  //this is needed to properly evaluate the errors
  uniHist->Sumw2();
  gausHist->Sumw2();

  //summ the two histograms and put them in the sum histogram
  sumHist -> Add(uniHist,gausHist);

  //scale to unity the sum histogram
  sumHist->Scale(1./sumHist->GetEntries());

  //draw
  TCanvas *c1 = new TCanvas();
  sumHist->Draw("E");
  // check the errors, e.g.
  // using the zoom option from the TBrowser
  // printing few values using TH1F::GetBinError(Int_t bin)


}
