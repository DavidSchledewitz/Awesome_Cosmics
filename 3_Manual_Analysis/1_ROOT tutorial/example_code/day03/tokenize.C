void tokenize()
{
  TString sToTokenize="Hi, this, is, how, to, tokenize";

  //Tokenize the string at ',' and ' '
  TObjArray *arr=sToTokenize.Tokenize(", ");

  //the array now contains the tokenized words
  //loop over them
  TIter nextWord(arr);
  TObject *o=0x0;

  while ( (o=nextWord()) ){
    cout << o->GetName() << endl;
  }

  // In reality the array contains objects of type
  // TObjString. There is also another way to access
  // the string inside the array

  // first reset the iterator
  nextWord.Reset();

  TObjString *ostr=0x0;
  while ( (ostr=static_cast<TObjString*>(nextWord())) ){
    TString &internalString=ostr->String();
    cout << internalString.Data() << endl;
  }
  
}