%global __requires_exclude perl\\(.*[.]pl\\)|^perl\\(vboxService\\)
%global __provides_exclude ^perl\\(vboxService\\)

Name:           RemoteBox
Version:        2.2
Release:        1%{?dist}
Summary:        Open Source VirtualBox Client with Remote Management
License:        GPLv2
URL:            http://remotebox.knobgoblin.org.uk/
Source0:        http://knobgoblin.org.uk/downloads/%{name}-%{version}.tar.bz2
Source1:        %{name}.desktop
BuildArch:      noarch
BuildRequires:  appdata-tools
BuildRequires:  desktop-file-utils
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(SOAP::Lite)
Requires:       perl-Gtk2
Requires:       perl-libwww-perl
Requires:       rdesktop
Requires:       xdg-utils

%description
VirtualBox is traditionally considered to be a virtualization solution aimed 
at the desktop as opposed to other solutions such as KVM, Xen and VMWare ESX 
which are considered more server oriented solutions. While it is certainly 
possible to install VirtualBox on a server, it offers few remote management 
features beyond using the vboxmanage command line. RemoteBox aims to fill 
this gap by providing a graphical VirtualBox client which is able to 
communicate with and manage a VirtualBox server installation. 

RemoteBox achieves this by using the vboxwebsrv feature of VirtualBox that 
allows its API to be accessed using a protocol called SOAP, even across a 
network. RemoteBox is very similar in look and feel to the native VirtualBox 
interface and allows you to perform most of the same tasks, including 
accessing the display of guests – completely remotely.

%prep
%setup -q

# We need to tell RemoteBox where to find it's files
sed -i 's|$Bin/docs|%{_pkgdocdir}|g' remotebox
sed -i 's|$Bin/share/remotebox|$Bin/share/%{name}|g' remotebox
sed -i 's|$Bin/|%{_prefix}/|g' remotebox share/remotebox/*.pl

%build
# Nothing to build.

%install
install -pd %{buildroot}%{_datadir}/%{name}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/pixmaps
cp -ar share/remotebox/* %{buildroot}%{_datadir}/%{name}/
install -pm755 remotebox %{buildroot}%{_bindir}

# Appdata file
mkdir -p %{buildroot}%{_datadir}/appdata
install -pm644 packagers-readme/remotebox.appdata.xml %{buildroot}%{_datadir}/appdata

# Desktop file
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{S:1}

# Icon for .desktop
install -pm644 share/remotebox/icons/remotebox.png %{buildroot}%{_datadir}/pixmaps

%check
appstream-util validate-relax %{buildroot}%{_datadir}/appdata/remotebox.appdata.xml

%files
%doc docs/*
%{_bindir}/remotebox
%{_datadir}/appdata/remotebox.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/remotebox.png
%{_datadir}/%{name}/

%changelog
* Tue Sep 06 2016 Adrian Sevcenco <adrian.sev@gmail.com>
- Rebuilt for 2.2 http://remotebox.knobgoblin.org.uk/
