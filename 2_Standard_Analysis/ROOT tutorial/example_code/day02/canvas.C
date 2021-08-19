void canvas()
{
  // create a few histograms
  TH1F *h1 = new TH1F("h1","first histogram",10,0,10);
  h1->Fill(1,2);
  h1->Fill(2,4);
  h1->Fill(3,3);

  TH1F *h2 = new TH1F("h2","second histogram",10,0,10);
  h2->Fill(2,2);
  h2->Fill(3,4);
  h2->Fill(4,3);

  TH1F *h3 = new TH1F("h3","third histogram",10,0,10);
  h3->Fill(3,2);
  h3->Fill(4,4);
  h3->Fill(5,3);

  TH1F *h4 = new TH1F("h4","fourth histogram",10,0,10);
  h4->Fill(4,2);
  h4->Fill(5,4);
  h4->Fill(6,3);
  
  TH1F *h5 = new TH1F("h5","fifth histogram",10,0,10);
  h5->Fill(7,2);
  h5->Fill(8,4);
  h5->Fill(9,3);

  // create first canvas
  TCanvas *c1 = new TCanvas("c1","my first canvas");
  c1->Divide(2,2);

  c1->cd(1);
  h1->Draw();
  h1->Fit("gaus");

  c1->cd(2);
  gPad->SetLeftMargin(0.3);
  h2->Draw();
  h2->Fit("gaus");

  c1->cd(3);
  gPad->SetTopMargin(0.3);
  h3->Draw();

  c1->cd(4);
  gPad->SetBottomMargin(0.3);
  h4->Draw();
  
  // create second canvases
  TCanvas *c2 = new TCanvas("c2","my second canvas");
  c2->SetFillColor(kBlue);
  h5->Draw();
}