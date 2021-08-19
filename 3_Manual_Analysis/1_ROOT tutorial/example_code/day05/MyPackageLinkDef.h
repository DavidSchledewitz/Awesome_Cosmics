#ifdef __ROOTCLING__
/* Copyright(c) 1998-1999, ALICE Experiment at CERN, All rights reserved. *
 * See cxx source for full Copyright notice                               */

//by default, rootcint should not generate the dictionary for all the classes:
#pragma link off all globals;
#pragma link off all classes;
#pragma link off all functions;

//classes for which the dictionary will be generated:
#pragma link C++ class myEvent+;
#pragma link C++ class myParticle+;
#endif
