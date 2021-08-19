{

  TString sdir("/data/run2/histos/2016/09/15/");
  cout<<"directory name: "<<sdir<<endl;
  TObjArray *dirObj = sdir.Tokenize("/");
  cout<<"The date associated to the directory is "<<dirObj->At(3)->GetName()<<"-"<<dirObj->At(4)->GetName()<<"-"<<dirObj->At(5)->GetName()<<endl;
  sdir.ReplaceAll("histos","graphs");
  cout<<"new directory name: "<<sdir<<endl;
}
