void FillRandom()
{
  // fill histograms with random functions
  TH1F *h1=new TH1F("h1","histo 1;random number (gaus)",100,-5,5);
  h1->FillRandom("gaus");

  TF1 fLine("fLine","[0]+[1]*x",0,100);
  fLine.SetParameters(0,1);
  TH1F *h2=new TH1F("h2","histo 2;random number",100,0,100);
  h2->FillRandom("fLine");

  fLine.SetParameters(10,.2);
  TH1F *h3=new TH1F("h3","histo 3;random number",100,0,100);
  h3->FillRandom("fLine");
  
  TH1F *h4=new TH1F("h4","histo 4;random number",100,-5,5);
  h4->FillRandom("landau");


  TCanvas *cRandom = new TCanvas("cRandom","Random numbers");
  cRandom->Divide(2,2);
  cRandom->cd(1);
  h1->Draw();

  cRandom->cd(2);
  h2->Draw();

  cRandom->cd(3);
  h3->Draw();

  cRandom->cd(4);
  h4->Draw();
  
}