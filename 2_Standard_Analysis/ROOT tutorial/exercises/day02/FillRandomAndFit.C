void FillRandomAndFit()
{
  // fill histograms with random functions
  TH1F *h=new TH1F("h","histo with random numbers from two gaussians;x;counts",200,-10,10);
  // Gauss with mean at -1 and width 0.5
  TF1 fGauss1("fGauss1","gaus",-10,10);
  fGauss1.SetParameters(1., -1., 0.5);
  
  // Gauss with mean at +1.5 and width 2
  TF1 fGauss2("fGauss2","gaus",-10,10);
  fGauss2.SetParameters(1., 1.5, 2.);
  
  
  // Generate twice as many entries for the first gauss
  h->FillRandom("fGauss1", 20000);
  h->FillRandom("fGauss2", 10000);
  
  TCanvas *cRandom = new TCanvas("cRandomAndFit","Random numbers with fit");
  h->Draw("e");
  
  // gaus(x) means that the indices of the parameters for that gaussian start at x.
  // Since a gaussian has 3 parameters, the parameters of the second gaussian need to
  // start at index 3
  TF1 fFit("fFit", "gaus(0)+gaus(3)", -10, 10);
  
  // Set some reasonable start parameters (deliberately not perfectly the ones
  // used for random number generation!)
  // We don't know the yield and there normalisations involved, so let's put just 100 here
  Double_t yield1 = 100.; 
  Double_t yield2 = 100.;
  Double_t mean1 = -0.9;
  Double_t mean2 = 1.8;
  Double_t sigma1 = 0.3;
  Double_t sigma2 = 2.5;
  
  fFit.SetParameter(0, yield1);
  fFit.SetParameter(1, mean1);
  fFit.SetParameter(2, sigma1);
  fFit.SetParameter(3, yield2);
  fFit.SetParameter(4, mean2);
  fFit.SetParameter(5, sigma2);
  
  // Perform the fit
  h->Fit(&fFit);
}