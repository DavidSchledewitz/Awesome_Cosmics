/*

compile the code with

g++ Rectangle.cpp -o Rectangle -Wall

*/

// include a header file, needed for the cout command
#include <iostream>
#include <cmath>

// the cout command resides in a so-called namespace
// in order to use it globally we have to let the compiler know
using namespace std;

// -----| Point2D class |----------------------------------------
// store x and y coordinates of a point in 2D space
//
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
  float DistanceToPoint(const Point2D &point) const;
  void  Print() { cout << "Point2D with coordinates (" << fx <<","<<fy<<")"<<endl; }

private:
  float fx;      // x-coordinate of the point
  float fy;      // y-coordinate of the point
};

// ---| function implementations | ----
float Point2D::DistanceToPoint(const Point2D &point) const
{
  // calculate distance of this point to another 'point'
  float x=0.,y=0.;
  point.GetPoint(x,y);
  
  return sqrt( (x-fx)*(x-fx) + (y-fy)*(y-fy) );
}

// -----| class rectangle |----------------------------------------
// class describing a rectangle using the Point2D class
//
class Rectangle {
public:
  Rectangle();
  Rectangle(const Rectangle& rectangle);
  Rectangle(float x1, float y1, float x2, float y2);
  Rectangle(float x1, float y1, float squareWidth);
  Rectangle(const Point2D &p1, const Point2D &p2);

  void SetCorners(float x1, float y1, float x2, float y2);
  void SetCornerWidthHeight(float x1, float y1, float width, float height);
  const Point2D& GetBottomLeft() const { return fPointBottomLeft; }
  const Point2D& GetTopRight() const { return fPointTopRight; }

  float GetWidth()    const { return abs(fPointBottomLeft.GetX()-fPointTopRight.GetX()); }
  float GetHeight()   const { return abs(fPointBottomLeft.GetY()-fPointTopRight.GetY()); }
  float GetArea()     const { return GetWidth()*GetHeight();                             }
  float GetDiagonal() const { return fPointBottomLeft.DistanceToPoint(fPointTopRight);   }

  bool  IsSquare()  const { return abs(GetWidth()-GetHeight()) < 1e-38; }

  void Print() const;
private:
  Point2D fPointBottomLeft;         // Top left point of the rectangle
  Point2D fPointTopRight;     // Bottom right point of the rectangle

  
};

// ---| function implementations | ----
Rectangle::Rectangle()
: fPointBottomLeft()
, fPointTopRight()
{
  // default constructor
}

//____________________________________________________________________
Rectangle::Rectangle(const Rectangle& rectangle)
: fPointBottomLeft(rectangle.fPointBottomLeft)
, fPointTopRight(rectangle.fPointTopRight)
{
  // copy constructor
}

//____________________________________________________________________
Rectangle::Rectangle(float x1, float y1, float x2, float y2)
: fPointBottomLeft(x1,y1)
, fPointTopRight(x2,y2)
{
  // default constructor using x and y coordinates of the two points
}

//____________________________________________________________________
Rectangle::Rectangle(float x1, float y1, float squareWidth)
: fPointBottomLeft(x1,y1)
, fPointTopRight(x1+squareWidth,y1+squareWidth)
{
  // default constructor
}

//____________________________________________________________________
Rectangle::Rectangle(const Point2D &p1, const Point2D &p2)
: fPointBottomLeft(p1)
, fPointTopRight(p2)
{
  // default constructor
}

//____________________________________________________________________
void Rectangle::SetCorners(float x1, float y1, float x2, float y2)
{
  // Set corners of both points
  fPointBottomLeft.SetPoint(x1,y1);
  fPointTopRight.SetPoint(x2,y2);
}

//____________________________________________________________________
void Rectangle::SetCornerWidthHeight(float x1, float y1, float width, float height)
{
  // set corner of bottom left point
  // together with the width and heigt of the square
  fPointBottomLeft.SetPoint(x1,y1);
  fPointTopRight.SetPoint(x1+width, y1+height);
}

//____________________________________________________________________
void Rectangle::Print() const
{
  // print all properties of the rectangle
  cout << "======= Rectangle properties ======" << endl;
  cout << "Bottom left coordinates: (" << fPointBottomLeft.GetX() << "," << fPointBottomLeft.GetY() << ")" << endl;
  cout << "Top right coordinates: ("   << fPointTopRight.GetX()   << "," << fPointTopRight.GetY()   << ")" << endl;
  
  cout << "Width:           " << GetWidth()    << endl;
  cout << "Height:          " << GetHeight()   << endl;
  cout << "Area:            " << GetArea()     << endl;
  cout << "Diagonal length: " << GetDiagonal() << endl;
  const char* yesno = IsSquare()?"Yes":"No";
  cout << "Is a square:     " << yesno << endl;
}

// -----| main function |----------------------------------------
//
//
int main()
{
  Rectangle rec1;
  rec1.SetCornerWidthHeight(1,2,5,10);
  rec1.Print();

  Rectangle rec2(Point2D(1,1), Point2D(10,2));
  rec2.Print();

  Rectangle rec3(3,3,4);
  rec3.Print();
  
  return 0;
}
