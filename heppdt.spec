### RPM external heppdt 3.03.00
Source: http://lcgapp.cern.ch/project/simu/HepPDT/download/HepPDT-%{realversion}.tar.gz
Patch1: heppdt-2.03.00-nobanner
Patch2: heppdt-3.03.00-silence-debug-output 
%define keep_archives yes

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -O2 -std=c++0x
%endif

%prep
%setup -q -n HepPDT-%{realversion}
%patch1 -p1
%patch2 -p1

CXX="%cms_cxx" CXXFLAGS="%cms_cxxflags" ./configure  --prefix=%{i} 

%build
make 

%install
make install
