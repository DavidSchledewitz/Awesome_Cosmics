void loadlibs()
{
  // load ROOT external libraries
  // the '.so' can be omitted
  // NOTE: Root has to be started in the directory where the makefile is in order to make
  // this macro function properly (given that the same directory structure with "code/" and
  // "macros/" is used
  gSystem->Exec("export LD_LIBRARY_PATH=.:$LD_LIBRARY_PATH");
  gSystem->AddIncludePath("-Icode/");
  gSystem->Load("libCore");
  gSystem->Load("libRIO");
  gSystem->Load("libTree");
  gSystem->Load("libHist");
  gSystem->Load("libEG");
  gSystem->Load("libMyPackage");
  
}