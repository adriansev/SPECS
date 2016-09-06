#
# spec file for package clhep
#
# Copyright (c) 2012 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           clhep
Version:        2.3.3.2
Release:        1
Summary:        A class library for high energy physics
License:        GPL-3.0
Group:          Development/Libraries/C and C++
Url:            http://proj-clhep.web.cern.ch/proj-clhep/
Source:         http://proj-clhep.web.cern.ch/proj-clhep/DISTRIBUTION/tarFiles/%{name}-%{version}.tgz
BuildRequires:  gcc-c++ >= 4.8
BuildRequires:  cmake >= 2.8
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
CLHEP is intended to be a set of high energy physics specific foundation and utility classes such as random generators, physics vectors, geometry and linear algebra. CLHEP is structured in a set of packages independent of any external package (interdependencies within CLHEP are allowed under certain conditions). 

%package -n clhep-devel
Summary:        A class library for high energy physics
Group:          Development/Libraries/C and C++
Requires:       clhep = %{version}

%description -n clhep-devel
CLHEP is intended to be a set of high energy physics specific foundation and utility classes such as random generators, physics vectors, geometry and linear algebra. CLHEP is structured in a set of packages independent of any external package (interdependencies within CLHEP are allowed under certain conditions). 

This package provides the header files and libraries for development of applications using CLHEP.

%prep
%setup -q -n %{version}/CLHEP
#FIX doc permissions
chmod 0644 README.md ChangeLog

%build
# CMake version 3.2 is not really required, 2.8 is sufficient (at least for version 2.3.22)
sed -i -e "s/cmake_minimum_required(VERSION 3.2)/cmake_minimum_required(VERSION 2.8)/" %{_builddir}/%{version}/CLHEP/CMakeLists.txt
sed -i -e 's/project/cmake_policy(SET CMP0048 NEW)\nproject/' %{_builddir}/%{version}/CLHEP/CMakeLists.txt

mkdir -p %{_builddir}/%{name}.%{version}/build

cd %{_builddir}/%{name}.%{version}/build

%cmake %{_builddir}/%{version}/CLHEP
make %{?_smp_mflags}

%install
cd %{_builddir}/%{name}.%{version}/build
make install DESTDIR=%{buildroot}

# leave static libraries in the package until installed cmake files are fixed
#rm %{buildroot}%{_libdir}/*.a

%clean
%{?buildroot:%__rm -rf "%{buildroot}"}

%post -n clhep -p /sbin/ldconfig

%postun -n clhep -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc ChangeLog README.md COPYING
%{_bindir}/*
%{_libdir}/libCLHEP*.so

%files -n clhep-devel
%defattr(-,root,root)
%{_includedir}/CLHEP/
%{_libdir}/CLHEP-%{version}/
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libCLHEP*.a

%changelog
* Wed May 18 2016 bugs@vdm-design.de
- Downgrade required CMake version to 2.8 as 3.2 is not really required
* Wed May 18 2016 bugs@vdm-design.de
- Update to version 2.3.2.2
- Change from automake to cmake
* Sat Jan 30 2016 bugs@vdm-design.de
- Run ldconfig in post install of clhep and not clhep-devel
* Sat Mar 28 2015 bugs@vdm-design.de
- Update to version 2.2.0.5
  * Only build system changes
* Fri Dec 26 2014 bugs@vdm-design.de
- Update to version 2.2.0.4
  * Utility/Utility/memory.h: fix a type mismatch
  * GenericFunctions/src/DefiniteIntegral.cc: explicit initialization
  * Random/src/RanshiEngine.cc: use a pragma to ignore aggressive 32bit compiler warnings
  * Vector/Vector/ThreeVector.icc: inline Hep3Vector::operator () (int i)
* Fri Sep 12 2014 bugs@vdm-design.de
- Update to version 2.2.0.3
  * cmake/Modules/ClhepVariables.cmake: DO NOT use any -ftls-model flags.
    Except in very specialized cases, the compiler automatically does the right thing.
* Wed Aug 13 2014 bugs@vdm-design.de
- Update to version 2.2.0.2
  * Units/Units/SystemOfUnits.h, Units/Units/PhysicalConstants.h:
    move definition of pi into SystemOfUnits so it is not defined twice
    Note that PhysicalConstants.h includes SystemOfUnits.h.
* Tue Jun 24 2014 bugs@vdm-design.de
- Update to version 2.2.0.1
  * Geometry/test/testBasicVector3D.cc: pragma fix for modern clang
  * GenericFunctions/GenericFunctions/StepDoublingRKStepper.hh: fix wrapper name
  * Random/src/RanshiEngine.cc: use explicit 32bit mask to avoid compiler warnings
  * Random/src/MTwistEngine.cc: make sure we don't go past the end of the
    array in MTwistEngine::showStatus
  * Random/src/Random.cc: remove unnecessary inline
  * In Random package convert statics and globals to const, thread
    local or atomic to improve thread safety.
* Wed May 14 2014 bugs@vdm-design.de
- Update to version 2.1.4.2
  * bug http://savannah.cern.ch/bugs/?104289
  * Vector, Random, Matrix: remove register declaration of ints and doubles
    use of register is now redundant and ignored by modern compilers
  * GenericFunctions, Geometry/test, Utility/test, Vector/test:
    protect against warnings about variables that are used inside asserts
* Mon Nov 18 2013 bugs@vdm-design.de
- Update to version 2.1.4.1
  * Random: including RandExpZiggurat and RandGaussZiggurat
  * Matrix: change the names of more internal variables so -Wshadow does not complain
  * Units/Units/SystemOfUnits.h: adding definitions for curies
  * configure.ac: change for unsupported Darwin build with autotools
* Thu Nov 15 2012 bugs@vdm-design.de
- Update to version 2.1.3.1
  * Vector: clean up naming overlap between Units and internal variables
* Fri Nov  9 2012 bugs@vdm-design.de
- Update to version 2.1.3.0
  * creation of symbolic links now respects DESTDIR
  * MATRIX/DiagMatrix, MATRIX/GenMatrix, MATRIX/SymMatrix:
    Added two methods to [-,Diag,Sym]Matrix to carry out the matrix
    inversion without the users needing to provide an ierr flag.
    These methods are all inline and called invert() and inverse(),
    so they overload the existing inversion routines for the relevant class.
    If an error occurs, then an std::runtime_error is thrown.
  * clhep-config: fix for Mountain Lion
* Fri Aug 17 2012 bugs@vdm-design.de
- Update to version 2.1.2.5
  * GenericFunctions: latest changes from Joe Boudreau
  * GenericFunctions: change the names of internal variables so -Wshadow does not complain
  * cmake/Modules: use OUTPUT_STRIP_TRAILING_WHITESPACE with execute_process commands
  * CMakeLists.txt, cmake/Modules: enable -DLIB_SUFFIX=64
  * Vector/LorentzVector.h: make the HepLorentzVector(double t) constructor explicit
* Thu Jul 12 2012 bugs@vdm-design.de
- Update to version 2.1.2.4
- Changes since 2.1.2.2
  * cmake/Modules: enclose CMAKE_COMMAND in quotes when inside execute_process
  * test shell scripts: make sure any paths are enclosed in quotes
  * cmake/Modules: Use newer execute_process instead of exec_program
    Try to cope with special characters in path
  * Random: fix for shadowing when global units used
  * Vector: fix for shadowing when global units used
    USING_VISUAL code blocks are no longer needed
  * GenericFunctions: latest changes from Joe Boudreau
  * Matrix: cleanup for -Wextra
  * Vector, Evaluator, Random, Geometry: use explicit std:: with math functions
* Wed May 16 2012 badshah400@gmail.com
- Update to version 2.1.2.2:
  + Make sure config files are executable add
    clhep_package_config_no_lib()
- Changes since previosuly packaged version 2.1.0.1:
  + Too many: see ChangeLog file packaged in
    /usr/share/doc/packages/clhep
- Use upstream compressed tarball now
- Do not use cmake for building though it is the recommended way
  to install according to upstream because the cmake build system
  does not allow setting the library directory easily leading to
  libraries being installed in /usr/lib even for x86_64 builds.
* Sun Feb 26 2012 scorot@free.fr
- fix build for SLE-11
* Sat Nov 19 2011 werner.ho@gmx.de
- updated to version 2.1.1.0
* Sun Apr 24 2011 badshah400@gmail.com
- Initial package (version 2.1.0.1)
