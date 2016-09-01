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

%prep
%setup -q -n %{version}/CLHEP
chmod 0644 README.md ChangeLog

%build
# CMake version 3.2 is not really required, 2.8 is sufficient (at least for version 2.3.22)
sed -i -e "s/cmake_minimum_required(VERSION 3.2)/cmake_minimum_required(VERSION 2.8)/" %{_builddir}/%{version}/CLHEP/CMakeLists.txt
sed -i -e 's/project/cmake_policy(SET CMP0048 NEW)\nproject/' %{_builddir}/%{version}/CLHEP/CMakeLists.txt

mkdir -p %{_builddir}/%{name}.%{version}/build
cd %{_builddir}/%{name}.%{version}/build
cmake -DCMAKE_INSTALL_PREFIX=$RPM_BUILD_ROOT \
      -DCMAKE_BUILD_TYPE=RelWithDebInfo \
%ifarch x86_64
      -DLIB_SUFFIX=64 \
%endif
       %{_builddir}/%{version}/CLHEP

make %{?_smp_mflags}

%install
cd %{_builddir}/%{name}.%{version}/build
make install DESTDIR=%{buildroot}

#%makeinstall
# leave static libraries in the package until installed cmake files are fixed
#rm %{buildroot}%{_libdir}/*.a

%files
%defattr(-,root,root)
%doc ChangeLog README COPYING
%{_bindir}/*
%{_includedir}/*
%{_libdir}/*

##%{_libdir}/libCLHEP*.so
##%{_libdir}/CLHEP-%{version}/
##%{_libdir}/pkgconfig/*.pc
##%{_libdir}/libCLHEP*.a

%clean
%{?buildroot:%__rm -rf "%{buildroot}"}

%post -n clhep -p /sbin/ldconfig

%postun -n clhep -p /sbin/ldconfig


%changelog
* Thu Sep 1 2016 adrian.sev@gmail.com
- 2.3.3.2 version from OpenSUSE
