TH1F *GetHistoGaus(const char* name)
{
  // create a simple histogram filled with random gaus numbers
  TH1F *h1 = new TH1F(name,"gauss;random gaus number; entries",100,-5,5);
  h1->FillRandom("gaus",100000);
  return h1;
}

//__________________________________________________________________________
TGraph* GetGraph()
{
  // fill a nice graph
  TGraph *gr=new TGraph;
  gr->SetTitle("My first graph;x-values;y-values");
  gr->SetPoint(0,1.,2.);
  gr->SetPoint(1,2.,4.);
  gr->SetPoint(2,5.,6.);
  gr->SetPoint(3,6.,9.);
  return gr;
}

//__________________________________________________________________________
void canvas_playing()
{
  // create a canvas and fill it with histograms with different styles

  TCanvas *c = new TCanvas("c","canvas");
  c->Divide(3,2);

  // create histograms and play with the style
  TH1F *h1=GetHistoGaus("h1");
  h1->SetLineWidth(4);
  h1->SetLineStyle(3);
  h1->SetLineColor(kMagenta);

  TH1F *h2=GetHistoGaus("h2");
  h2->SetLineWidth(4);
  h2->SetLineColor(kSpring);
  h2->SetFillStyle(3002);
  h2->SetFillColor(kOrange);
  
  TH1F *h3=GetHistoGaus("h3");
  h3->SetLineWidth(4);
  h3->SetLineColor(kMagenta);

  //create graphs. Use different draw options below
  TGraph *gr1=GetGraph();
  gr1->SetLineWidth(3);

  TGraph *gr2=GetGraph();
  gr2->SetLineWidth(3);

  TGraph *gr3=GetGraph();
  gr3->SetLineWidth(3);
  
  // draw the histograms
  c->cd(1);
  h1->Draw();
  c->cd(2);
  h2->Draw();
  c->cd(3);
  h3->Draw("c");

  //draw the graphs
  c->cd(4);
  //with solid lines bewteen the points
  gr1->Draw("alp");
  c->cd(5);
  // with smooth lines between the points
  gr2->Draw("acp");
  c->cd(6);
  // with the area filled
  gr3->Draw("alfp");

  c->SaveAs("canvas_playing.gif");
}
