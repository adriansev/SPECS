%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

%if %{?fedora}%{!?fedora:0} >= 21 || %{?rhel}%{!?rhel:0} >= 7
%global use_systemd 1
%else
%global use_systemd 0
%endif

Summary:	xrdcp monitoring plugin 
Name:		xrootd-xrdcpapmonplugin
Version:	1.1.1
Epoch:		1
Release:	1%{?dist}
License:	none
Group:		System Environment/Daemons

Source0: 	%{name}-%{version}.tar.gz
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-root

%ifarch x86_64
  %define __lib lib64
%else
  %define __lib lib
%endif

%define __prefix /usr/
%define __libdir /usr/%{__lib}/
%define __incdir /usr/include/
%define __apmondir /usr/
%define __xrootddir /usr/

Requires: xrootd-client >= 4.0.0 , ApMon_cpp

%description
xrdcp monitoring plugin

%prep
%setup -q

%build
./configure --with-xrootd-location=%{__xrootddir} --with-apmon-location=%{__apmondir} --prefix=%{__prefix} --libdir=%{__libdir} --includedir=%{__incdir}
make %{?_smp_mflags}

make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT \( -type f -o -type l \) -print | sed "s#^$RPM_BUILD_ROOT/*#/#" > RPM-FILE-LIST

%clean
rm -rf $RPM_BUILD_ROOT

%files -f RPM-FILE-LIST
%defattr(-,root,root)

%changelog
* Tue Jun 16 2015 adrian <adrian.sevcenco@cern.ch> - xrdcpmonplugin
- Initial build.
