Summary: ALICE xrootd plugins meta-package
Name: alicexrdplugins
Version: 0.1
Release: 1
License: none
Group:   Applications/xrootd

Requires: ApMon_cpp >= 2.2.8
Requires: tokenauthz >= 1.1.9
Requires: xrootd-aggregatingname2name >= 1.0.1
Requires: xrootd-alicetokenacc >= 1.2.5
Requires: xrootd-ftsofs >= 2.2.2
Requires: xrootd-xrdcpapmonplugin >= 1.1.1

%description
ALICE xrootd plugins meta-package

%prep
%setup -c -T

%install

%build

%files

%changelog
* Fri Jun 19 2015 Adrian Sevcenco <adrian.sevcenco@cern.ch> 0.1
- Initial package
