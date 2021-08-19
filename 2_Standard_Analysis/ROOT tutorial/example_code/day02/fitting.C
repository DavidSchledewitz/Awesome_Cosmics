/*


.L fitting.C

// the histogram examples:
fitHistogram();
fitHistogram2();


// the graph example:
fitGraph();



*/

void PrintFunctionParameters(const TF1 *myFun)
{
  //
  // print the values und errors of all parameters of the function
  //

  cout << " The fit parameters and errors of function '" << myFun->GetName() <<"' are:" << endl;
  for (Int_t ipar=0; ipar<myFun->GetNpar(); ++ipar){
    cout << "Parameter " << ipar << ": " << myFun->GetParameter(ipar) << " +- " << myFun->GetParError(ipar) << endl;
  }
  
}

//__________________________________________________________________________________
void fitHistogram()
{
  //
  // example that show how to fit a Histogram with a predefined function
  //

  TH1F *histo = new TH1F("histo","A histogram",10,0,10);
  histo->Fill(4,2);
  histo->Fill(5,6);
  histo->Fill(6,4);

  // do the fit with a predefined function.
  // This list can be found in the FitPanal of the GUI
  histo->Fit("gaus");
}

//__________________________________________________________________________________
void fitHistogram2()
{
  //
  // example that show how to fit a Histogram with a predefined function
  //
  
  TH1F *histo = new TH1F("histo","A histogram",10,0,10);
  histo->Fill(4,2);
  histo->Fill(5,6);
  histo->Fill(6,4);

  // define the function yourself
  TF1 *myFun = new TF1("myGaus","[0]*exp( -(x-[1])**2/([2]**2) )",-10,10);
  // you will need to give some initial parameters, this can be tedious ...
  myFun->SetParameters(1,1,1);

  histo->Fit(myFun);
  PrintFunctionParameters(myFun);
}

//__________________________________________________________________________________
void fitGraph()
{
  TGraph *gr = new TGraph;
  gr->SetTitle("My first graph;x-values;y-values");
  gr->SetPoint(0,1.,2.);
  gr->SetPoint(1,2.,4.);
  gr->SetPoint(2,5.,6.);
  gr->SetPoint(3,6.,9.);
  gr->Draw("alp");

  // define a linear function
  TF1 *myLine = new TF1("myLine","[0]+[1]*x",0.,10.);
  myLine->SetLineColor(kRed);

  // fit the graph
  gr->Fit(myLine);
  PrintFunctionParameters(myLine);
  
}