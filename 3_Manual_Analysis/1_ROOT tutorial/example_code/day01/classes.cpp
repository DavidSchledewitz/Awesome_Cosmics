/*

compile the code with

g++ classes.cpp -o classes -Wall

*/

// include a header file, needed for the cout command
#include <iostream>
#include <cmath>

// the cout command resides in a so-called namespace
// in order to use it globally we have to let the compiler know
using namespace std;

class Point2D {
public:
  //default constructor
  Point2D()                 : fx(0.), fy(0.) {;}
  //custom constructor
  Point2D(float x, float y) : fx(x ), fy(y ) {;}
  //copy constructor
  Point2D(const Point2D &point) : fx(point.fx), fy(point.fy) {;}

  // setter functions
  void SetPoint(float x, float y) { fx=x; fy=y; }
  // getter functions
  void GetPoint(float &x, float &y) const { x=fx; y=fy; }
  float GetX() const { return fx; }
  float GetY() const { return fy; }

  // operations
  float DistanceToPoint(const Point2D &point);
  void  Print() { cout << "Point2D with coordinates (" << fx <<","<<fy<<")"<<endl; }

private:
  float fx;      // x-coordinate of the point
  float fy;      // y-coordinate of the point
};

// function implementations
float Point2D::DistanceToPoint(const Point2D &point)
{
  // calculate distance of this point to another 'point'
  float x=0.,y=0.;
  point.GetPoint(x,y);

  return sqrt( (x-fx)*(x-fx) + (y-fy)*(y-fy) );
}

int main()
{
  Point2D p1(2,5);
  Point2D p2(3,4);
  float distance=p1.DistanceToPoint(p2);
  
  cout << "The distance between" << endl << "  ";
  p1.Print();
  cout << "  and" << endl << "  ";
  p2.Print();
  cout << "  is: " << distance << endl << endl;

  cout << "The distance between" << endl << "  ";
  p1.Print();
  cout << "  and the origin (0,0)" << endl;
  cout << "  is: " << p1.DistanceToPoint( Point2D(0,0) ) << endl    ;
       
  return 0;
}
