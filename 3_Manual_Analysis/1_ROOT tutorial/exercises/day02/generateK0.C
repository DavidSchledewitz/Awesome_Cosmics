
{

  //this code was used to generate the histogram for the exercise drawK0
  TF1 *g = new TF1("g","[0]*TMath::Gaus(x,[1],[2])",0.35,0.65);
  g->SetParameters(1000,0.497,0.005);
  
  TH1F *h2=new TH1F("h2","K0 mass",100,0.35,0.65);
  h2->FillRandom("g",5000);
  
  TF1 *f = new TF1 ("f","[0]+pow(x,[1])",0.35,0.65);
  f->SetParameters(100,-6);
  h2->FillRandom("f",10000);
  h2->Draw();
  
 
  }
