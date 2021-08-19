{
    
   TH1F *K0mass= new TH1F("K0mass","K0 mass",100,0.35,0.65);
   K0mass->SetBinContent(1,307);
   K0mass->SetBinContent(2,267);
   K0mass->SetBinContent(3,249);
   K0mass->SetBinContent(4,231);
   K0mass->SetBinContent(5,245);
   K0mass->SetBinContent(6,237);
   K0mass->SetBinContent(7,209);
   K0mass->SetBinContent(8,212);
   K0mass->SetBinContent(9,188);
   K0mass->SetBinContent(10,209);
   K0mass->SetBinContent(11,197);
   K0mass->SetBinContent(12,196);
   K0mass->SetBinContent(13,162);
   K0mass->SetBinContent(14,202);
   K0mass->SetBinContent(15,186);
   K0mass->SetBinContent(16,159);
   K0mass->SetBinContent(17,155);
   K0mass->SetBinContent(18,158);
   K0mass->SetBinContent(19,142);
   K0mass->SetBinContent(20,148);
   K0mass->SetBinContent(21,150);
   K0mass->SetBinContent(22,135);
   K0mass->SetBinContent(23,134);
   K0mass->SetBinContent(24,111);
   K0mass->SetBinContent(25,125);
   K0mass->SetBinContent(26,117);
   K0mass->SetBinContent(27,123);
   K0mass->SetBinContent(28,115);
   K0mass->SetBinContent(29,130);
   K0mass->SetBinContent(30,106);
   K0mass->SetBinContent(31,101);
   K0mass->SetBinContent(32,112);
   K0mass->SetBinContent(33,95);
   K0mass->SetBinContent(34,105);
   K0mass->SetBinContent(35,102);
   K0mass->SetBinContent(36,104);
   K0mass->SetBinContent(37,97);
   K0mass->SetBinContent(38,84);
   K0mass->SetBinContent(39,82);
   K0mass->SetBinContent(40,82);
   K0mass->SetBinContent(41,99);
   K0mass->SetBinContent(42,88);
   K0mass->SetBinContent(43,100);
   K0mass->SetBinContent(44,105);
   K0mass->SetBinContent(45,118);
   K0mass->SetBinContent(46,225);
   K0mass->SetBinContent(47,464);
   K0mass->SetBinContent(48,857);
   K0mass->SetBinContent(49,1205);
   K0mass->SetBinContent(50,1177);
   K0mass->SetBinContent(51,878);
   K0mass->SetBinContent(52,477);
   K0mass->SetBinContent(53,198);
   K0mass->SetBinContent(54,118);
   K0mass->SetBinContent(55,62);
   K0mass->SetBinContent(56,69);
   K0mass->SetBinContent(57,59);
   K0mass->SetBinContent(58,73);
   K0mass->SetBinContent(59,68);
   K0mass->SetBinContent(60,69);
   K0mass->SetBinContent(61,53);
   K0mass->SetBinContent(62,66);
   K0mass->SetBinContent(63,62);
   K0mass->SetBinContent(64,61);
   K0mass->SetBinContent(65,60);
   K0mass->SetBinContent(66,60);
   K0mass->SetBinContent(67,56);
   K0mass->SetBinContent(68,55);
   K0mass->SetBinContent(69,53);
   K0mass->SetBinContent(70,72);
   K0mass->SetBinContent(71,48);
   K0mass->SetBinContent(72,57);
   K0mass->SetBinContent(73,48);
   K0mass->SetBinContent(74,43);
   K0mass->SetBinContent(75,57);
   K0mass->SetBinContent(76,42);
   K0mass->SetBinContent(77,76);
   K0mass->SetBinContent(78,51);
   K0mass->SetBinContent(79,62);
   K0mass->SetBinContent(80,46);
   K0mass->SetBinContent(81,68);
   K0mass->SetBinContent(82,63);
   K0mass->SetBinContent(83,42);
   K0mass->SetBinContent(84,53);
   K0mass->SetBinContent(85,46);
   K0mass->SetBinContent(86,53);
   K0mass->SetBinContent(87,62);
   K0mass->SetBinContent(88,56);
   K0mass->SetBinContent(89,53);
   K0mass->SetBinContent(90,47);
   K0mass->SetBinContent(91,46);
   K0mass->SetBinContent(92,70);
   K0mass->SetBinContent(93,59);
   K0mass->SetBinContent(94,59);
   K0mass->SetBinContent(95,58);
   K0mass->SetBinContent(96,57);
   K0mass->SetBinContent(97,57);
   K0mass->SetBinContent(98,48);
   K0mass->SetBinContent(99,49);
   K0mass->SetBinContent(100,48);
   K0mass->SetEntries(15000);
   K0mass->GetXaxis()->SetTitle("m [GeV/c]");

   Int_t ci;      // for color index setting
   TColor *color; // for color definition with alpha
   ci = TColor::GetColor("#000099");
   K0mass->SetLineColor(ci);
   K0mass->GetXaxis()->SetLabelFont(42);
   K0mass->GetXaxis()->SetLabelSize(0.035);
   K0mass->GetXaxis()->SetTitleSize(0.035);
   K0mass->GetXaxis()->SetTitleFont(42);
   K0mass->GetYaxis()->SetLabelFont(42);
   K0mass->GetYaxis()->SetLabelSize(0.035);
   K0mass->GetYaxis()->SetTitleSize(0.035);
   K0mass->GetYaxis()->SetTitleFont(42);
   K0mass->GetZaxis()->SetLabelFont(42);
   K0mass->GetZaxis()->SetLabelSize(0.035);
   K0mass->GetZaxis()->SetTitleSize(0.035);
   K0mass->GetZaxis()->SetTitleFont(42);
   K0mass->Draw("");
   
 
   
   
   //define the fit function as sum of two function:
  // gaus(x) means that the indices of the parameters for that gaussian start at x.
  // Since a gaussian has 3 parameters, the parameters of the second function need to start at index 3
   TF1 fFit("fFit", "gaus(0)+[3]*pow(x,[4])", 0.35,0.65);

  // Set some reasonable start parameters 
  // in case the fit does not work, try to search the correct parameters for the two functions individually:
  // Fit of the peak region with a gaussian
  // Fit  the whole region with the second function
  Double_t yield1 = 1000.; 
  Double_t mean1 = 0.5;
  Double_t sigma1 = 0.005;
  Double_t exp0 = 7.;
  Double_t slope = -5.8;

  fFit.SetParameter(0, yield1);
  fFit.SetParameter(1, mean1);
  fFit.SetParameter(2, sigma1);
  fFit.SetParameter(3, exp0);
  fFit.SetParameter(4, slope);
  
 // Perform the fit
  K0mass->Fit(&fFit);

   
}
