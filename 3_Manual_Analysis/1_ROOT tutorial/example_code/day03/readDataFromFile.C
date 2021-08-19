
#include <iostream>
#include <fstream>
using namespace std;

void readDataFromFile(){

  //class to read an input file
   ifstream in;
   //open an existing file to read 
   in.open("data.dat");

   Float_t x,y,z;
   while (1) {
     //insert the values of each line in the variables x y z
     in >> x >> y >> z;
     // when the file finishes, exit the loop 
      if (!in.good()) break;
      //print the values
      cout<<x <<" "<<y<<" "<<z<<endl;
   }
   //close the file
   in.close();
}

  
