void readFile(){
  
  TFile *file = new TFile("../../example_code/day03/vertex.root");
  TH2F * vertex2D = (TH2F *)file->Get("vertex2D");
  TH1D * Zvert_1 = (TH1D *)file->Get("Zvert_1");
  TH1D * Zvert_2 = (TH1D *)file->Get("Zvert_2");
  TCanvas *c1 = new TCanvas("canvas_vertex", "canvas vertex",11,80,1634,469);

  c1->Divide(3);
  c1->cd(1);
  vertex2D->Draw("colz");
  c1->cd(2);
  Zvert_1->Draw();
  c1->cd(3);
  Zvert_2->Draw();

  c1->SaveAs("canvas_vertex.root");
  file->Close();
}
 


//This part was used to create the file to read
void createFile(){

  TFile file("../../examples_code/day03/vertex.root","recreate");
  TH2F *vertex2DH = new TH2F("vertex2D","Interaction vertex Z vs x; Z(cm); x(cm)",200,-8,8,100,-0.6,0.6);
  //in Z uniform * smearing
  for (Int_t i=0; i<10000;++i){
    Float_t z = gRandom->Uniform(-5,5)*gRandom->Gaus(1,0.1);
    Float_t x = gRandom->Gaus(0,0.05);
    vertex2DH->Fill(z, x);
    
  }
  vertex2DH->Draw("colzs");
  vertex2DH->Write();
  
  TH1D *Zvert_1 = vertex2DH->ProjectionX("Zvert_1",0,200);
  Zvert_1->SetTitle("Z vertex coordinate");
  Zvert_1->Draw();
  Zvert_1->Write();

  TH1D *Zvert_2 = vertex2DH->ProjectionY("Zvert_2",0,200);
  Zvert_2->SetTitle("X vertex coordinate");
  Zvert_2->Draw();
  Zvert_2->Write();
 
  file.Close();
  }
