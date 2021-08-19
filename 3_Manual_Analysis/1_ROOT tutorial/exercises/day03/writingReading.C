void firstGaus(){
  TFile file("saveGaus.root","recreate");
  TH1F *h=new TH1F("h","first gaussian;x;counts",200,0,4);
  // Gauss with mean at 2 and width 0.2
  TF1 fGauss1("fGauss1","gaus",0,4);
  fGauss1.SetParameters(1., 2., 0.2);
  h->FillRandom("fGauss1", 20000);
  h->Write();
  file.Close();

}

void secondGaus(){
  TFile file("saveGaus.root","update");
  TH1F *h2=new TH1F("h2","second gaussian;x;counts",200,0,4);
 // Gauss with mean at 3 and width 0.2
  TF1 fGauss2("fGauss2","gaus",0,4);
  fGauss2.SetParameters(1., 3., 0.2);
  h2->FillRandom("fGauss2", 10000);
  h2->Write();
  file.Close();

}

/*
//to read the histograms:
  TFile file("saveGaus.root","read");
  TH1F *h1=(TH1F *)file.Get("h");
  TH1F *h2=(TH1F *)file.Get("h2");
  //  TCanvas *cRandom = new TCanvas("Random gaussians","Random gaussians");
  h1->Draw();
  h2->SetLineColor(2);
  h2->Draw("same");
 
  gStyle->SetOptStat(false) ;//turn off the stat box
  
  //draw the legend:
  TLegend *leg = new TLegend(0.6,0.7,0.9,0.9);
  leg->AddEntry(h1,"first Gaussian");
  leg->AddEntry(h2,"Second Gaussian");
  leg->Draw();
*/
