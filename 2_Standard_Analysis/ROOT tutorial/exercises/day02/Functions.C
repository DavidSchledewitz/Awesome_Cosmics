void Functions()
{

  TF1 *f = new TF1("f","[0]*pow(x,[1])*sin(x)",0,3);
  f->SetParameters(3,2);
  f->Draw();


  cout<<"Value of f(x) in x=1: "<<f->Eval(1)<<endl;
  cout<<"Derivative of f(x)  in x=1: "<<f->Derivative(1)<<endl;
  cout<<"Integral of f(x)  between 0 and 3: "<<f->Integral(0,3)<<endl;


  
}
