# include root definitions for the compiler $(CXX) and linker $(LD) to be used
ARCHFILE=$(wildcard $(ROOTSYS)/test/Makefile.arch)
ifeq ($(ARCHFILE),)
  ARCHFILE=$(ROOTSYS)/etc/Makefile.arch
endif
include $(ARCHFILE)

PACKAGE = MyPackage

default-target: lib$(PACKAGE).so

#include directories
INC      = -I. $(EINCLUDE)

#compiler flags
CXXFLAGS     += -W -Wall -Weffc++ -Woverloaded-virtual -fPIC -pipe -fmessage-length=0 -Wno-long-long  -Dlinux $(INC) -g

#include the definitions for this package
include lib$(PACKAGE).pkg

# add the root dictionary to the list of sources
SRCS_package := $(SRCS) G__$(PACKAGE).cxx
# build the list of objects (compiled code)
OBJS_package := $(SRCS_package:.cxx=.o)

# link the objects to a software library
lib$(PACKAGE).so: $(OBJS_package)
	@echo "Linking" $@ ...
	@/bin/rm -f $@
	$(LD) $(SOFLAGS) $(LDFLAGS) $^ -o $@
	@chmod a+x $@
	@echo "done"

# compile the code 
%.o:    %.cxx %.h
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	@rm -f $(OBJS_package) *.so G__$(PACKAGE).*

G__$(PACKAGE).cxx: $(HDRS) $(DHDR)
	@echo "Generating dictionary ..."
	rootcling -f $@ -c $(CLINGFLAGS) $(INC) $^

G__$(PACKAGE).h: ;
