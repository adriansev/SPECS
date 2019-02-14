Name: lm_sensors
Version: 3.3.5
Release: 0%{?dist}
URL: http://www.lm-sensors.org/
Source: http://dl.lm-sensors.org/lm-sensors/releases/%{name}-%{version}.tar.bz2
Source1: lm_sensors.sysconfig
# these 2 were taken from PLD-linux, Thanks!
Source2: sensord.sysconfig
Source3: sensord.init
Source4: sensors-detect
Source5: lm_sensors-README.redhat
Summary: Hardware monitoring tools
Group: Applications/System
License: GPLv2+
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%ifarch %{ix86} x86_64
Requires: /usr/sbin/dmidecode
%endif
Requires(preun): chkconfig
Requires(post): chkconfig
Requires(post): /sbin/ldconfig
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
BuildRequires: kernel-headers >= 2.2.16, bison, libsysfs-devel, flex, gawk
BuildRequires: rrdtool-devel

%description
This package includes a collection of modules for general SMBus
access and hardware monitoring.


%package libs
Summary: Linux hardware monitoring core libraries
Group: System Environment/Libraries

%description libs
Core libraries for Linux hardware monitoring applications.


%package devel
Summary: Development files for sensors development
Group: Development/System
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
This package includes a header files and libraries for use
when building applications that make use of sensor data.


%package sensord
Summary: Daemon that periodically logs sensor readings
Group: System Environment/Daemons
Requires: %{name}%{?_isa} = %{version}-%{release}

%description sensord
Daemon that periodically logs sensor readings to system log daemon
or a round-robin database, and warns of sensor alarms.


%prep
%setup -q
mv prog/init/README prog/init/README.initscripts
chmod -x prog/init/fancontrol.init


%build
export CFLAGS="%{optflags}"
make PREFIX=%{_prefix} LIBDIR=%{_libdir} MANDIR=%{_mandir} EXLDFLAGS= \
  PROG_EXTRA=sensord user


%install
rm -fr $RPM_BUILD_ROOT
make PREFIX=%{_prefix} LIBDIR=%{_libdir} MANDIR=%{_mandir} PROG_EXTRA=sensord \
  DESTDIR=$RPM_BUILD_ROOT user_install
rm $RPM_BUILD_ROOT%{_libdir}/libsensors.a

ln -s sensors.conf.5.gz $RPM_BUILD_ROOT%{_mandir}/man5/sensors3.conf.5.gz
install -d -m 0755 $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}
cp -r CHANGES CONTRIBUTORS COPYING doc README* \
    prog/init/fancontrol.init prog/init/README.initscripts \
    $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}
install -m 0644 %{SOURCE5} \
    $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}/README.redhat

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/lm_sensors
install -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/sensord
install -p -m 755 prog/init/sysconfig-lm_sensors-convert \
  $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_initrddir}
install -p -m 755 prog/init/lm_sensors.init \
  $RPM_BUILD_ROOT%{_initrddir}/lm_sensors
install -p -m 755 %{SOURCE3} $RPM_BUILD_ROOT%{_initrddir}/sensord
install -p -m 755 %{SOURCE4} $RPM_BUILD_ROOT%{_sbindir}/sensors-detect

%clean
rm -fr $RPM_BUILD_ROOT


# For conversion of sensors.conf on upgrades from 2.10.x to 3.x.x
# First mv any /etc/sensors.conf.rpmsave from previous updates out of the way
# Then after uninstall check if /etc/sensors.conf.rpmsave is created, if it
# is the user was using a non pristine /etc/sensors.conf, so convert it

%triggerun -- lm_sensors <= 2.10.999
if [ -f /etc/sensors.conf.rpmsave ]; then
  mv /etc/sensors.conf.rpmsave /etc/sensors.conf.rpmsave.old
fi

%triggerpostun -- lm_sensors <= 2.10.999
if [ -f /etc/sensors.conf.rpmsave ]; then
  mv /etc/sensors3.conf /etc/sensors3.conf.rpmnew
  %{_bindir}/sensors-conf-convert < /etc/sensors.conf.rpmsave > \
    /etc/sensors3.conf
  rm /etc/sensors.conf.rpmsave
fi
if [ -f /etc/sensors.conf.rpmsave.old ]; then
  mv /etc/sensors.conf.rpmsave.old /etc/sensors.conf.rpmsave
fi

# for conversion of /etc/sysconfig/lm_sensors format change
%triggerpostun -- lm_sensors <= 3.0.3
%{_bindir}/sysconfig-lm_sensors-convert 

%pre
if [ -f /var/lock/subsys/sensors ]; then
    mv -f /var/lock/subsys/sensors /var/lock/subsys/lm_sensors
fi

%post
/sbin/chkconfig --add lm_sensors

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%preun
if [ $1 = 0 ]; then
    /sbin/chkconfig --del lm_sensors
fi

%post sensord
/sbin/chkconfig --add sensord

%preun sensord
if [ $1 = 0 ]; then
    /sbin/chkconfig --del sensord
fi

%files
%defattr(-,root,root,-)
%dir %{_defaultdocdir}/%{name}-%{version}
%doc %{_defaultdocdir}/%{name}-%{version}/*
%config(noreplace) %{_sysconfdir}/sensors3.conf
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_sbindir}/*
%{_initrddir}/lm_sensors
%config(noreplace) %{_sysconfdir}/sysconfig/lm_sensors
%exclude %{_sbindir}/sensord
%exclude %{_mandir}/man8/sensord.8.gz

%files libs
%defattr(-,root,root,-)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/sensors
%{_libdir}/lib*.so
%{_mandir}/man3/*

%files sensord
%defattr(-,root,root,-)
%doc prog/sensord/README
%{_sbindir}/sensord
%{_initrddir}/sensord
%{_mandir}/man8/sensord.8.gz
%config(noreplace) %{_sysconfdir}/sysconfig/sensord


%changelog
* Mon May 04 2015 - 3.3.5-0
latest 3.3.5 version - see CHANGES file