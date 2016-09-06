Name: htop
Version: 2.0.2
Release: 1%{?dist}
Summary: Interactive process viewer
Group: Applications/System
License: GPL+
URL: http://hisham.hm/htop/
Source0: http://hisham.hm/htop/releases/%{version}/%{name}-%{version}.tar.gz

BuildRequires: desktop-file-utils
BuildRequires: ncurses-devel
BuildRequires: python
BuildRequires: libtool

%description
htop is an interactive text-mode process viewer for Linux, similar to
top(1).

%prep
%setup -q
sed -i s#"INSTALL_DATA = @INSTALL_DATA@"#"INSTALL_DATA = @INSTALL_DATA@ -p"# Makefile.in

%build
autoreconf -v -f -i

%configure \
  --enable-proc \
	--enable-openvz \
	--enable-vserver \
	--enable-taskstats \
	--enable-unicode \
	--enable-native-affinity \
	--enable-cgroup \
	--enable-oom

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

#remove empty direcories
rm -rf $RPM_BUILD_ROOT%{libdir}
rm -rf $RPM_BUILD_ROOT%{includedir}

# remove desktop file
rm -rf $RPM_BUILD_ROOT%{_datadir}/applications/

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog README
%{_bindir}/htop
%{_datadir}/pixmaps/htop.png
%{_mandir}/man1/htop.1*

%changelog
* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1.0.3-5
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 22 2014 Morten Stevens <mstevens@imt-systems.com> - 1.0.3-3
- Enable OOM column score support (BZ#1111922)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 28 2014 Morten Stevens <mstevens@imt-systems.com> - 1.0.3-1
- Update to 1.0.3
- Should resolve BZ#925557, BZ#987805, BZ#1091943 

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 09 2012 Miloš Jakubíček <xjakub@fi.muni.cz> - 1.0.2-1
- Update to 1.0.2
- Dropped libpagemap patch (conflicting with upstream)
- Removed BR: libpagemap-devel
- Should resolve BZ#859912, BZ#862039, BZ#864495, BZ#874879

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Miloš Jakubíček <xjakub@fi.muni.cz> - 1.0.1-1
- Update to 1.0.1
- Should resolve BZ#782272, BZ#815995, BZ#835221

* Tue Feb 07 2012 Miloš Jakubíček <xjakub@fi.muni.cz> - 1.0-1
- Update to 1.0
- Build with --enable-openvz --enable-vserver --enable-taskstats
  --enable-unicode --enable-native-affinity --enable-cgroup
- Drop htop-0.9-system-plpa.patch (no PLPA needed anymore)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Apr 08 2011 Miloš Jakubíček <xjakub@fi.muni.cz> - 0.9-3
- include patch by Petr Holasek (pholasek@redhat.com) that adds
  libpagemap support and introduces new -p cmd option and USS,
  PSS, SWAP columns

* Sat Mar 19 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.9-2
- Clean up spec to match current guidelines
- Drop desktop file. Resolves rhbz#689028

* Sat Mar 05 2011 Miloš Jakubíček <xjakub@fi.muni.cz> - 0.9-1
- Update to 0.9
- Clean specfile, remove Polish translations, unused patches

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Mar  4 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 0.8.3-3
- use plpa system copy instead of embedded one

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 23 2009 Rafał Psota <rafalzaq@gmail.com> - 0.8.3-1
- update to 0.8.3

* Fri Jun 12 2009 Rafał Psota <rafalzaq@gmail.com> - 0.8.2-2
- "htop aborts after hitting F6 key" fixed (#504795)

* Tue Jun 02 2009 Rafał Psota <rafalzaq@gmail.com> - 0.8.2-1
- update to 0.8.2

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 05 2009 Rafał Psota <rafalzaq@gmail.com> - 0.8.1-3
- "Tree view doesn't work with threads hidden" fixed (#481072)

* Tue Nov 18 2008 Rafał Psota <rafalzaq@gmail.com> - 0.8.1-2
- non-printable character filter patch (#504144)

* Tue Oct 14 2008 Rafał Psota <rafalzaq@gmail.com> - 0.8.1-1
- update to 0.8.1

* Thu Jul 31 2008 Rafał Psota <rafalzaq@gmail.com> - 0.8-1
- update to 0.8

* Sun Apr 27 2008 Rafał Psota <rafalzaq@gmail.com> - 0.7-2
- desktop file fix

* Mon Feb 11 2008 Rafał Psota <rafalzaq@gmail.com> - 0.7-1
- update to 0.7

* Sat Dec  9 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 0.6.5-1
- Update to 0.6.5

* Wed Oct  4 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 0.6.4-1
- Update to 0.6.4

* Sat Sep 16 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 0.6.3-2
- Rebuild for FE6

* Sun Jul 30 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 0.6.3-1
- Update to 0.6.3
- Correct e-mail address in ChangeLog
- Replace tabs with spaces

* Sat May 20 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 0.6.2-1
- Update to 0.6.2

* Wed May 10 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 0.6.1-2
- Add missing BR: desktop-file-utils

* Wed May 10 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 0.6.1-1
- Update to 0.6.1

* Tue Feb 14 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 0.6-3
- Rebuild for Fedora Extras 5

* Wed Dec 28 2005 Dawid Gajownik <gajownik[AT]gmail.com> - 0.6-2
- Rebuild with updated tarball

* Wed Dec 28 2005 Dawid Gajownik <gajownik[AT]gmail.com> - 0.6-1
- Version 0.6

* Fri Nov 11 2005 Dawid Gajownik <gajownik[AT]gmail.com> - 0.5.4-2
- Don't use superflous CFLAGS variable (Dmitry Butskoy)
- Don't include AUTHORS and NEWS files

* Thu Nov 10 2005 Dawid Gajownik <gajownik[AT]gmail.com> - 0.5.4-1
- Initial RPM release.
