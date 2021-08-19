void legend()
{
  //
  // draw 2 histograms and a graph and add a legend
  //

  TH1F *h1 = new TH1F("h1","first",10,0,10);
  h1->Fill(1,2);
  h1->Fill(2,4);
  h1->Fill(3,3);
  h1->Fill(4,1);
  
  TH1F *h2 = new TH1F("h2","second",10,0,10);
  h2->Fill(3,2);
  h2->Fill(4,4);
  h2->Fill(5,3);
  h2->Fill(6,1);
  h2->SetLineColor(kRed);
  
  h1->Draw("HIST");
  h2->Draw("HIST same");

  TGraph *gr = new TGraph;
  gr->SetPoint(0,1,1);
  gr->SetPoint(1,5,1.5);
  gr->SetPoint(2,9,3.5);
  gr->SetMarkerStyle(21);
  gr->SetMarkerSize(1);
  gr->SetMarkerColor(kBlue);
  gr->SetLineColor(kBlue);
  gr->Draw("lp");

  TLegend *leg = new TLegend(.7,.2,.9,.5);
  leg->SetFillColor(10);
  leg->SetBorderSize(1);
  leg->AddEntry(h1,"histo 1","l");
  leg->AddEntry(h2,"histo 2","l");
  leg->AddEntry(gr,"grah","lp");
  leg->Draw();
}
