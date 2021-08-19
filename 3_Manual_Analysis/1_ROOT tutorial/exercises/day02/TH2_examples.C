void TH2_examples()
{
  // create a 2D histogram
  TH2F *h2f = new TH2F("h2f","2D hist;x;y;entries",100,-2,4,100,-1,1);

  //a 2D gaussian
  TF2 f2d("f2d","100*TMath::Gaus(x,1,1) * TMath::Gaus(y,0,0.2)");

  //fill the histogram
  h2f->FillRandom("f2d",100000);

  // create a canvas with 2 pads
  TCanvas *c=new TCanvas("c","Canvas for 2D histograms",1000,500);
  c->Divide(2);
  c->cd(1);
  h2f->DrawCopy("colz");
  c->cd(2);
  h2f->DrawCopy("surf2");

}
