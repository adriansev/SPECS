%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

%if %{?fedora}%{!?fedora:0} >= 21 || %{?rhel}%{!?rhel:0} >= 7
%global use_systemd 1
%else
%global use_systemd 0
%endif

Summary: XrdcpApmonPlugin
Name:    xrootd-xrdcpapmonplugin
Version: 1.1.1
Release: 1%{?dist}
License: none
Group: ALICE Offline

Source0:  %{name}-%{version}.tar.gz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%ifarch x86_64
  %define __lib lib64
%else
  %define __lib lib
%endif

%define __prefix /usr
%define __libdir /usr/%{__lib}
%define __incdir /usr/include
%define __xrootddir /usr
%define __sslincdir /usr/include
%define __apmondir /usr

Requires: xrootd-server >= 4.1.0
Requires: ApMon_cpp
## Requires: xrootd-server >= 4.0.0 , xrootd-client >= 4.0.0 , tokenauthz , openssl

BuildRequires: xrootd-private-devel >= 4.1.0
BuildRequires: xrootd-devel >= 4.1.0
BuildRequires: xrootd-server-devel >= 4.1.0
BuildRequires: ApMon_cpp

%description
This file implements an instance of the XrdClientAbsMonIntf abstract class,
to be used to send data from xrdcp to Monalisa in the Alice environment

%prep
%setup -q
./bootstrap.sh

%build
./configure --prefix=%{__prefix} --libdir=%{__libdir} --with-xrootd-location=%{__xrootddir} --with-apmon-location=%{__apmondir}

make %{?_smp_mflags}
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT \( -type f -o -type l \) -print | sed "s#^$RPM_BUILD_ROOT/*#/#" > RPM-FILE-LIST

%clean
rm -rf $RPM_BUILD_ROOT

%files -f RPM-FILE-LIST
%defattr(-,root,root,-)
%doc

%changelog
* Tue May 17 2016 - xrdcpapmonplugin
- Initial build.
