Name: libmodbus
Version: 3.1.4
Release: 1%{?dist}
Summary: A Modbus library
Group: Applications/System
License: LGPLv2+
URL: http://www.libmodbus.org/
Source0: https://github.com/downloads/stephane/libmodbus/libmodbus-%{version}.tar.gz
BuildRequires: autoconf, automake, libtool, xmlto, asciidoc

%description
libmodbus is a C library designed to provide a fast and robust implementation of
the Modbus protocol. It runs on Linux, Mac OS X, FreeBSD, QNX and Windows.

This package contains the libmodbus shared library.

%package devel
Summary: Development files for libmodbus
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
libmodbus is a C library designed to provide a fast and robust implementation of
the Modbus protocol. It runs on Linux, Mac OS X, FreeBSD, QNX and Windows.

This package contains libraries, header files and developer documentation needed
for developing software which uses the libmodbus library.

%prep
%setup -q

./autogen.sh

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}/%{_libdir}/*.la

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)

%doc AUTHORS MIGRATION NEWS COPYING* README.md

%{_libdir}/libmodbus.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/modbus/

%{_libdir}/pkgconfig/libmodbus.pc
%{_libdir}/libmodbus.so

%{_mandir}/man7/*.7.*
%{_mandir}/man3/*.3.*

%changelog
