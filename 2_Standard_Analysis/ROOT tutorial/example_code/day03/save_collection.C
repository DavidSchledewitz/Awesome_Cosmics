void save_collection()
{
  // create a few histograms and add them
  // to a collection
  TH1F *h1 = new TH1F("h1","h1",10,0,10);
  TH1F *h2 = new TH1F("h2","h2",10,0,10);
  TH1F *h3 = new TH1F("h3","h3",10,0,10);
  TH1F *h4 = new TH1F("h4","h4",10,0,10);
  
  // crate a list and a TObjArray
  TList mylist;
  
  mylist.Add(h1);
  mylist.Add(h2);
  mylist.Add(h3);
  mylist.Add(h4);

  //open a file and save the collection
  // look at the contents
  TFile f("save_collection.root","recreate");
  mylist.Write();
  f.ls();
  f.Close();

  //open a file and save the collection
  //now with the option kSingleKey
  // look at the contents
  TFile f2("save_collection_singleKey.root","recreate");
  mylist.Write("myCollection",TObject::kSingleKey);
  f2.ls();
  f2.Close();
}


