%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

%if %{?fedora}%{!?fedora:0} >= 21 || %{?rhel}%{!?rhel:0} >= 7
%global use_systemd 1
%else
%global use_systemd 0
%endif

Summary:	MonALISA Application Monitoring API 
Name:		ApMon_cpp
Version:	2.2.8
Epoch:		1
Release:	4%{?dist}
License:	none
Group:		System Environment/Daemons

Source0: 	%{name}-%{version}.tar.gz
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%ifarch x86_64
  %define __lib lib64
%else
  %define __lib lib
%endif

%define __prefix /usr/
%define __libdir /usr/%{__lib}/
%define __incdir /usr/include/

%description
ApMon is a set of flexible APIs that can be used by any application to send monitoring information to MonALISA services.

%prep
%setup -q

%build
./configure --prefix=%{__prefix} --libdir=%{__libdir} --includedir=%{__incdir}
make %{?_smp_mflags}
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/usr/share/perl5/ApMon
mkdir -p $RPM_BUILD_ROOT/usr/sbin
cp -av bin/* $RPM_BUILD_ROOT/usr/sbin
cp -av perl/* $RPM_BUILD_ROOT/usr/share/perl5/ApMon/

find $RPM_BUILD_ROOT \( -type f -o -type l \) -print | sed "s#^$RPM_BUILD_ROOT/*#/#" > RPM-FILE-LIST

%clean
rm -rf $RPM_BUILD_ROOT

%files -f RPM-FILE-LIST
%defattr(-,root,root)

%changelog

* Thu May 5 2016 adrian <adrian.sevcenco@cern.ch> - apmon-2.2.8-4
- corrections/improvements to servMon.sh script
- updating of pm modules

* Tue Apr 4 2016 adrian <adrian.sevcenco@cern.ch> - apmon-2.2.8-3
- single location for pm modules /usr/share/perl5/ApMon
- corrections to servMon.sh script

* Tue Sep 24 2015 adrian <adrian.sevcenco@cern.ch> - apmon-2.2.8
- ProcInfo.pm /proc/net/dev regex improved

* Tue Jun 16 2015 adrian <adrian.sevcenco@cern.ch> - apmon-2.2.8
- Initial build.

