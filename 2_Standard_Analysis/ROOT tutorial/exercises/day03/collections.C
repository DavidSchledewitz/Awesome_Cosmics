{

TH1F *h1 = new TH1F("h1","h1",100,-10,10);
TH1F *h2 = new TH1F("h2","h2",50,-5,5);
TH1F *h3 = new TH1F("h3","h3",10,0,10);
TH1F *h4 = new TH1F("h4","h4",10,0,10);

h1->FillRandom("gaus",2000);
h2->FillRandom("gaus",1000);
h3->FillRandom("pol1",1000);
h4->FillRandom("landau",10000);


TList histList;
histList.Add(h1);
histList.Add(h2);
histList.Add(h3);
histList.Add(h4);


TGraphErrors *gr1 = new TGraphErrors(10);
TGraphErrors *gr2 = new TGraphErrors(10);
TGraphErrors *gr3 = new TGraphErrors(10);
TGraphErrors *gr4 = new TGraphErrors(10);

for (Int_t i=0; i<10; ++i){
  gr1->SetPoint(i,i,i*2);
  gr1->SetPointError(i,0,0.05*i);
  gr1->SetName("gr1");
  gr2->SetPoint(i,i,i/2.);
  gr2->SetPointError(i,0,0.02);
  gr2->SetName("gr2");
  gr3->SetPoint(i,i,i);
  gr3->SetPointError(i,0,0.05);
  gr3->SetName("gr3");
  gr4->SetPoint(i,i,i*i);
  gr4->SetPointError(i,0,0.01*i);
  gr4->SetName("gr4");

  
 }

TObjArray arr;
arr.Add(gr1);
arr.Add(gr2);
arr.Add(gr3);
arr.Add(gr4);


TFile file("saveCollection.root","recreate");
histList.Write("hist",TObject::kSingleKey);
arr.Write("graphs",TObject::kSingleKey);
file.Close();

}
