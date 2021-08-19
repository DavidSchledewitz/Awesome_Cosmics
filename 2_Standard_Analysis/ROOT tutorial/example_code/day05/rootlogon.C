void rootlogon()
{
  
  cout<<"Welcome back "<<endl;
  const Int_t NCont=255;
  TStyle *st = new TStyle("mystyle","mystyle");
  gROOT->GetStyle("Plain")->Copy((*st));
  st->SetTitleX(0.1);
  st->SetTitleW(0.8);
  st->SetTitleH(0.08);
  st->SetStatX(.9);
  st->SetStatY(.9);
  st->SetNumberContours(NCont);
  st->SetPalette(1,0);
  st->SetOptStat("erm");
  st->SetOptFit(0);
  st->SetGridColor(kGray+1);
  st->SetPadGridX(kTRUE);
  st->SetPadGridY(kTRUE);
  st->SetPadTickX(kTRUE);
  st->SetPadTickY(kTRUE);
  st->SetMarkerStyle(20);
  st->SetMarkerSize(.5);
  st->cd();
  
}
