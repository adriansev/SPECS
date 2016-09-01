Summary: FTS overlay OFS plugin
Name: xrootd-ftsofs
Version: 2.2.2
Release: 1
License: none
Group:   Applications/xrootd
Source0: xrootd-ftsofs-2.2.2.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: xrootd-server >= 4.0.0 , xrootd-server-devel  >= 4.0.0 , xrootd-client >= 4.0.0 , xrootd-client-devel  >= 4.0.0 , xrootd-private-devel >= 4.0.0, libuuid-devel

Requires: xrootd-server >= 4.0.0 , xrootd-client >= 4.0.0

%ifarch x86_64
  %define __lib lib64
%else
  %define __lib lib
%endif

%define __prefix /usr/
%define __libdir /usr/%{__lib}/
%define __incdir /usr/include/
%define __xrootddir /usr/

%description
FTS overlay OFS plugin

%prep
%setup -n xrootd-ftsofs-2.2.2

%build
./bootstrap.sh
./configure --prefix=%{__prefix} --libdir=%{__libdir} --with-xrootd-location=%{__xrootddir}
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
/usr/*
%doc


%changelog
* Wed Dec  2 2009 Andreas Joachim Peters <peters@pcitsmd01.cern.ch> - ftsofs-1
- Initial build.

