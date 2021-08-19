/*
  .L macros/classesAndIO.cpp++
  classesAndIO()

  
  Once this file is executed, you can open the testClassesAndIO.root in the ROOT prompt and access p with the saved values,
   e.g. you can do p->GetX(); etc

   Remember to load the shared library : 
   gSystem->Load("macros/classesAndIO_cpp.so")

  
*/

// include  headers file
#include <iostream>
#include <cmath>
#include "TFile.h"


// the cout command resides in a so-called namespace
// in order to use it globally we have to let the compiler know
using namespace std;

class Point2D : public TObject { // Inherit from TObject to have I/O functionality
public:
  //default constructor
  Point2D()                 : TObject(), fx(0.), fy(0.) {;}
  //custom constructor
  Point2D(float x, float y) : TObject(), fx(x ), fy(y ) {;}
  
  Point2D(const Point2D &point) : TObject(point), fx(point.fx), fy(point.fy) {;}

  // setter functions
  void SetPoint(float x, float y) { fx=x; fy=y; }
  // getter functions
  void GetPoint(float &x, float &y) const { x=fx; y=fy; }
  float GetX() const { return fx; }
  float GetY() const { return fy; }

  // operations
  float DistanceToPoint(const Point2D &point);

private:
  float fx;      
  float fy;      

  //ID must be >=1 to have automatic generation of I/O capabilities!
  ClassDef(Point2D, 1); // Point2D class
};

// function implementations
float Point2D::DistanceToPoint(const Point2D &point)
{
  // calculate distance of this point to another 'point'
  float x=0.,y=0.;
  point.GetPoint(x,y);

  return sqrt( (x-fx)*(x-fx) + (y-fy)*(y-fy) );
}

void classesAndIO()
{
    Point2D* p = new Point2D(2,5);
    TFile* f = TFile::Open("testClassesAndIO.root", "RECREATE");
    f->cd();
    p->Write("myp");
    f->Close();
    delete p;
}
