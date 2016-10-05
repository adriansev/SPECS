%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

%if %{?fedora}%{!?fedora:0} >= 21 || %{?rhel}%{!?rhel:0} >= 7
%global use_systemd 1
%else
%global use_systemd 0
%endif

Summary: Alice Token Authorization Acc plugin
Name: xrootd-alicetokenacc
Version: 1.3.0
Release: 2%{?dist}
License: none
Group: CERN IT-DSS-TD

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
%define __tkauthzlibdir /usr/%{__lib}
%define __tkauthzincdir /usr/include
%define __sslincdir /usr/include

AutoReqProv: no
Requires: xrootd-server >= 4.1.0
Requires: tokenauthz >= 1.1.8
## Requires: xrootd-server >= 4.0.0 , xrootd-client >= 4.0.0 , tokenauthz , openssl

BuildRequires: xrootd-private-devel >= 4.1.0
BuildRequires: xrootd-devel >= 4.1.0
BuildRequires: xrootd-server-devel >= 4.1.0
BuildRequires: tokenauthz >= 1.1.8

%description
An authorization plugin for xrootd using the Alice Token authorization envelope.

%prep
%setup -q
./bootstrap.sh

%build
./configure --prefix=%{__prefix} --libdir=%{__libdir} --includedir=%{__incdir} --with-xrootd-location=%{__xrootddir} --with-tkauthz-libdir=%{__tkauthzlibdir} --with-tkauthz-incdir=%{__tkauthzincdir} -with-openssl-incdir=%{__sslincdir}

make %{?_smp_mflags}
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT \( -type f -o -type l \) -print | sed "s#^$RPM_BUILD_ROOT/*#/#" > RPM-FILE-LIST

%clean
rm -rf $RPM_BUILD_ROOT

%files -f RPM-FILE-LIST
%defattr(-,root,root,-)
%doc

%changelog
* Fri Aug 22 2008 root <root@pcitsmd01.cern.ch> - alicetokenacc-1
- Initial build.
