void histo_style()
{
  // Attention the histogram below will not show up in
  // the canvas, because at the end of the function
  // it goes out of scope and is deleted
  TH1F histo("histo","A histogram",10,0,10);
  histo.Fill(4,2);
  histo.Fill(5,6);
  histo.Fill(6,4);

  histo.SetLineColor(kRed);
  histo.SetFillStyle(3008);
  histo.SetFillColor(kBlue-2);
  histo.Draw("HIST");


  // In order to get a histogram which will stay on the canvas
  // you need to create it with 'new'
  // NOTE: the acess operator changed
  TH1F *histo2 = new TH1F("histo2","A histogram 2",10,0,10);
  histo2->Fill(4,2);
  histo2->Fill(5,6);
  histo2->Fill(6,4);
  
  histo2->SetLineColor(kRed);
  histo2->SetLineWidth(4);
  histo2->SetFillStyle(3008);
  histo2->SetFillColor(kBlue-2);
  histo2->Draw("HIST");
}




