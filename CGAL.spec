# Min dependencies
%global boost_version 1.48
%global qt_version 5.3
%global cmake_version 2.8.11

# Various variables that defines the release
%global soname 11
%global soversion 11.0.2
%global alphatag %{nil}
#global alphatag beta1
%global alphaname %{nil}
#global alphaname -%{alphatag}

Name:           CGAL
Version:        4.8.1
Release:        2%{alphatag}%{?dist}
Summary:        Computational Geometry Algorithms Library

Group:          System Environment/Libraries
License:        LGPLv3+ and GPLv3+ and Boost
URL:            http://www.cgal.org/
Source0:        https://github.com/CGAL/cgal/releases/download/releases/%{name}-%{version}%{alphaname}/%{name}-%{version}%{alphaname}.tar.xz
Source10:       CGAL-README.Fedora

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Required devel packages.
BuildRequires: cmake >= %{cmake_version}
BuildRequires: gmp-devel
BuildRequires: boost-devel >= %{boost_version}
BuildRequires: qt5-qtbase-devel >= %{qt_version}
BuildRequires: qt5-qtsvg-devel >= %{qt_version}
BuildRequires: qt5-qtscript-devel >= %{qt_version}
BuildRequires: qt5-qttools-devel >= %{qt_version}
BuildRequires: zlib-devel
BuildRequires: mpfr-devel

%description
Libraries for CGAL applications.
CGAL is a collaborative effort of several sites in Europe and
Israel. The goal is to make the most important of the solutions and
methods developed in computational geometry available to users in
industry and academia in a C++ library. The goal is to provide easy
access to useful, reliable geometric algorithms.


%package devel
Group:          Development/Libraries
Summary:        Development files and tools for CGAL applications
Requires:       cmake
Requires:       %{name} = %{version}-%{release}
Requires:       boost-devel%{?_isa} >= %{boost_version}
Requires:       qt5-qtbase-devel%{?_isa} >= %{qt_version}
Requires:       qt5-qtsvg-devel%{?_isa} >= %{qt_version}
Requires:       qt5-qtscript-devel%{?_isa} >= %{qt_version}
Requires:       qt5-qttools-devel%{?_isa} >= %{qt_version}
Requires:       zlib-devel%{?_isa} gmp-devel%{?_isa}
Requires:       mpfr-devel%{?_isa}
%description devel
The %{name}-devel package provides the headers files and tools you may need to 
develop applications using CGAL.


%package demos-source
Group:          Documentation
Summary:        Examples and demos of CGAL algorithms
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
%description demos-source
The %{name}-demos-source package provides the sources of examples and demos of
CGAL algorithms.


%prep
%setup -q -n %{name}-%{version}%{alphaname}

# Fix some file permissions
#chmod a-x include/CGAL/export/ImageIO.h

# Install README.Fedora here, to include it in %%doc
install -p -m 644 %{SOURCE10} ./README.Fedora

%build

mkdir build
pushd build
%cmake -DCGAL_INSTALL_LIB_DIR=%{_lib} -DWITH_CGAL_Qt3:BOOL=FALSE -DCGAL_INSTALL_DOC_DIR= ${CHANGE_SOVERSION} ..
make VERBOSE=1 %{?_smp_mflags}
popd


%install
rm -rf %{buildroot}

pushd build

make install DESTDIR=$RPM_BUILD_ROOT

popd

# Install demos and examples
mkdir -p %{buildroot}%{_datadir}/CGAL
touch -r demo %{buildroot}%{_datadir}/CGAL/
cp -a demo %{buildroot}%{_datadir}/CGAL/demo
cp -a examples %{buildroot}%{_datadir}/CGAL/examples

%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE LICENSE.FREE_USE LICENSE.LGPL LICENSE.GPL CHANGES README.Fedora
%{_libdir}/libCGAL*.so.%{soname}
%{_libdir}/libCGAL*.so.%{soversion}


%files devel
%defattr(-,root,root,-)
%{_includedir}/CGAL
%{_libdir}/libCGAL*.so
%{_libdir}/CGAL
%dir %{_datadir}/CGAL
%{_bindir}/*
%exclude %{_bindir}/cgal_make_macosx_app
%{_mandir}/man1/cgal_create_cmake_script.1.gz


%files demos-source
%defattr(-,root,root,-)
%dir %{_datadir}/CGAL
%{_datadir}/CGAL/demo
%{_datadir}/CGAL/examples
%exclude %{_datadir}/CGAL/*/*/skip_vcproj_auto_generation

%changelog
* Thu Jan 14 2016 Jonathan Wakely <jwakely@redhat.com> - 4.7-2
- Rebuilt for Boost 1.60

* Tue Oct 20 2015 Laurent Rineau <lrineau@renoir.geometryfactory.com> - 4.7-1
- New upstream release: 4.7
- New source URL scheme

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 4.7-0.2.beta1
- Rebuilt for Boost 1.59

* Fri Aug  7 2015 Laurent Rineau <lrineau@renoir.geometryfactory.com> - 4.7-0.1beta1
- New upstream release
- Drop the support of Qt3

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 4.6.1-2
- rebuild for Boost 1.58

* Tue Jun 30 2015 Laurent Rineau <lrineau@renoir.geometryfactory.com> - 4.6.1-1
- New upstream release
- Remove Patch0, already in CGAL-4.6.1.

* Mon Jun 22 2015 Laurent Rineau <lrineau@renoir.geometryfactory.com> - 4.6-3
- Add Patch0: support for CMake-3.3 in Rawhide/F23

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Apr 10 2015 Laurent Rineau <lrineau@renoir.geometryfactory.com> - 4.6-1
- New upstream release

* Tue Feb 24 2015 Laurent Rineau <lrineau@renoir.geometryfactory.com> - 4.6-0.1.beta1
- New upstream beta release

* Tue Feb 17 2015 Laurent Rineau <lrineau@renoir.geometryfactory.com> - 4.5.2-1
- New upstream release, bug-fix

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 4.5.1-2
- Rebuild for boost 1.57.0

* Tue Dec 23 2014 Laurent Rineau <lrineau@renoir.geometryfactory.com> - 4.5.1-1
- New upstream release (bug-fix 4.5.1)

* Mon Nov  3 2014 Laurnent Rineau <Laurent.Rineau__fedora@normalesup.org> - 4.5-1
- New upstream release

* Sat Aug 16 2014 Laurent Rineau <lrineau@renoir.geometryfactory.com> - 4.5-0.1.beta1
- New upstream release

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Petr Machata <pmachata@redhat.com> - 4.4-2
- Rebuild for boost 1.55.0

* Mon Apr  7 2014 Laurent Rineau <lrineau@renoir.geometryfactory.com> - 4.4-1
- New upstream release.

* Fri Mar 14 2014 Laurent Rineau <lrineau@renoir.geometryfactory.com> - 4.4-0.1.beta1
- New upstream beta release
- No longer use BLAS/LAPACK

* Tue Oct 22 2013 Laurent Rineau <lrineau@renoir.geometryfactory.com> - 4.3-1
- New upstream release

* Tue Aug 27 2013 Laurent Rineau <Laurent.Rineau__fedora@normalesup.org> - 4.3-beta1-0.1.beta1
- New upstream release

* Tue Jul 30 2013 Petr Machata <pmachata@redhat.com> - 4.2-4
- Rebuild for boost 1.54.0

* Mon Jul 29 2013 Ville Skyttä <ville.skytta@iki.fi> - 4.2-3
- Fix build with unversioned %%{_docdir_fmt}.

* Sat Jul 27 2013 pmachata@redhat.com - 4.2-2
- Rebuild for boost 1.54.0

* Mon Apr 15 2013 Laurent Rineau <Laurent.Rineau__fedora@normalesup.org> - 4.2-1
- New upstream release 4.2

* Sun Feb 10 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 4.1-3
- Rebuild for Boost-1.53.0

* Sat Feb 09 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 4.1-2
- Rebuild for Boost-1.53.0

* Thu Oct 25 2012 Laurent Rineau <Laurent.Rineau__fedora@normalesup.org> - 4.1-1
- New upstream release 4.1

* Fri Aug 10 2012 Laurent Rineau <Laurent.Rineau__fedora@normalesup.org> - 4.0.2-3
- Rebuild for Boost version bump

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul  4 2012 Laurent Rineau <Laurent.Rineau__fedora@normalesup.org> - 4.0.2-1
- New upstream release: bug-fix release CGAL-4.0.2
- Remove the patch CGAL-4.0-gcc47.patch (upstreamed)

* Thu Jun 14 2012 Laurent Rineau <Laurent.Rineau__fedora@normalesup.org> - 4.0-3
- Add a patch to fix the compilation of an undocumented header with gcc-4.7

  Fix bug #831847

* Wed Mar 14 2012 Laurent Rineau <Laurent.Rineau__fedora@normalesup.org> - 4.0-2
- New upstream release: CGAL-4.0

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-1.3.beta1
- Rebuilt for c++ ABI breakage

* Thu Feb 23 2012 Laurent Rineau <Laurent.Rineau__fedora@normalesup.org> - 4.0-0.3.beta1
- Change the License tag, to add Boost.

* Mon Feb 13 2012 Laurent Rineau <Laurent.Rineau__fedora@normalesup.org> - 4.0-0.2.beta1
- New upstream release CGAL-4.0-beta1.
- Use arch-specific Requires:

* Tue Feb  7 2012 Laurent Rineau <Laurent.Rineau__fedora@normalesup.org> - 4.0-0.1.alpha4
- New upstream version.
  The beta release will be published 2012/02/10, and the official release
  is planned for 2012/03/10.

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jan  5 2012 Laurent Rineau <Laurent.Rineau__fedora@normalesup.org> - 3.8-5
- Mass rebuild for F17

* Mon Nov 21 2011 Laurent Rineau <Laurent.Rineau__fedora@normalesup.org> - 3.8-4
- rebuild with new Boost libraries
- Add a patch to be compatible with Boost-1.48.

* Thu Oct 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 3.8-3.2
- rebuild with new gmp without compat lib

* Mon Oct 10 2011 Peter Schiffer <pschiffe@redhat.com> - 3.8-3.1
- rebuild with new gmp

* Thu Jul 21 2011 Laurent Rineau <Laurent.Rineau__fedora@normalesup.org> - 3.8-3
- Rebuild (Boost new version landed in rawhide)

* Thu Apr 21 2011 Laurent Rineau <Laurent.Rineau__fedora@normalesup.org> - 3.8-2
- New upstream release

* Sat Apr  9 2011  <Laurent.Rineau__fedora@normalesup.org> - 3.8-1.1.beta1
- Rebuild after Boost sonames bump

* Tue Mar 15 2011 Laurent Rineau <Laurent.Rineau__fedora@normalesup.org> - 3.8-0.1.beta1
- New upstream release. This is a beta release. Final release is schedule end of March 2011.
- Use macros to define the alphatag (if any), the soname/soversion (checked
  in %%files), and the number of the download at gforge.inria.fr

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Feb 06 2011 Thomas Spura <tomspur@fedoraproject.org> - 3.6.1-3
- rebuild for new boost

* Tue Aug  3 2010 Laurent Rineau <Laurent.Rineau__fedora@normalesup.org> - 3.6.1-2
- Rebuild (because of Boost SONAME bump)

* Thu Jul  1 2010 Laurent Rineau <Laurent.Rineau__fedora@normalesup.org> - 3.6.1-1
- New upstream release
- Fix some file permissions (rpmlint warnings)
- Upstream version CGAL-3.6.1 has not modified the build number of the
  SOVERSION. Fix that with a CMake option -DCGAL_SOVERSION=...
- Fix changelog: use of macro is a single percent, instead of two, and add
  my real name so several changelog entries.

* Sat Mar  6 2010 Laurent Rineau <Laurent.Rineau__fedora@normalesup.org> - 3.6-0.1.beta1
- New upstream release

* Mon Jan 18 2010 Laurent Rineau <Laurent.Rineau__fedora@normalesup.org> - 3.5.1-2
- Rebuild after Boost upgrade (and soname bump)

* Thu Dec 24 2009 Laurent Rineau <Laurent.Rineau__fedora@normalesup.org> - 3.5.1-1
- New upstream release

* Tue Nov 24 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.5-3
- Rebuild for Qt 4.6.0 RC1 in F13 (was built against Beta 1 with unstable ABI)

* Mon Nov  2 2009 Laurent Rineau <Laurent.Rineau__fedora@normalesup.org> - 3.5-2
- Use system's FindBoost macro instead of a copy from CGAL (bug #532431).

* Sun Oct 18 2009 Laurent Rineau <Laurent.Rineau__fedora@normalesup.org> - 3.5-1
- New upstream release: finale version of CGAL-3.5.

* Thu Jul 30 2009 Laurent Rineau <Laurent.Rineau__fedora@normalesup.org> - 3.5-0.2.beta1
- No longer requires /etc/profile.d/

* Thu Jul 30 2009 Laurent Rineau <Laurent.Rineau__fedora@normalesup.org> - 3.5-0.1.beta1
- Update to CGAL-3.5-beta1.
- New compilation process: CMake.
- No longer any need for patches.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Laurent Rineau <Laurent.Rineau__fedora@normalesup.org> - 3.3.1-13
- noarch CGAL-demos-source, which is purely data.

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Apr  1 2008 Rex Dieter <rdieter@fedoraproject.org> - 3.3.1-11
- -devel: Requires: qt3-devel

* Tue Apr  1 2008 Laurent Rineau <laurent.rineau__fedora@normalesup.org> - 3.3.1-10
- Rebuild for Rawhide. BR: qt3-devel instead of qt-devel (which is now Qt-4.x).

* Mon Feb 11 2008 Laurent Rineau <laurent.rineau__fedora@normalesup.org> - 3.3.1-9
- Rebuild with g++-4.3.

* Mon Nov  5 2007 Laurent Rineau <laurent.rineau__fedora@normalesup.org> - 3.3.1-8
- Add Requires: mpfr-devel for CGAL-devel.

* Mon Oct 22 2007 Laurent Rineau <laurent.rineau__fedora@normalesup.org> - 3.3.1-6
- fix /etc/profile.d/cgal.*

* Sun Oct 21 2007 Laurent Rineau <laurent.rineau__fedora@normalesup.org> - 3.3.1-3
- gawk and coreutils are not required in BR (see exceptions list)
- fix multilib issues (bug #340821):
  - rename %%{_datadir}/CGAL/cgal.mk to %%{_datadir}/CGAL/cgal-%%{_arch}.mk
  - remove the arch-specific comment from %%{_includedir}/CGAL/compiler_config.h

* Mon Sep  3 2007 Laurent Rineau <laurent.rineau__fedora@normalesup.org> - 3.3.1-2
- Fix soversion.

* Mon Sep  3 2007 Laurent Rineau <laurent.rineau__fedora@normalesup.org> - 3.3.1-1
- New upstream bug-fixes release.

* Fri Aug 24 2007 Laurent Rineau <laurent.rineau__fedora@normalesup.org> - 3.3-7
- Add BR: mpfr since F-8.

* Fri Aug 24 2007 Laurent Rineau <laurent.rineau__fedora@normalesup.org> - 3.3-6
- Add BR: gawk

* Thu Aug 23 2007 Laurent Rineau <laurent.rineau__fedora@normalesup.org> - 3.3-5
- License: tag fixed.

* Thu Jun  7 2007 Laurent Rineau <laurent.rineau__fedora_extras@normalesup.org> - 3.3-4
- Move the makefile back to %%{_datadir}/CGAL, and rename it cgal.mk (sync
  with Debian package). That file is not a config file, but just an example
  .mk file that can be copied and adapted by users.
- Fix the %%{_sysconfdir}/profile.d/cgal.* files (the csh one was buggy).
- CGAL-devel now requires all its dependancies.

* Sat Jun  2 2007 Laurent Rineau <laurent.rineau__fedora_extras@normalesup.org> - 3.3-2
- Official CGAL-3.3 release
- Skip file named "skip_vcproj_auto_generation"

* Wed May 30 2007 Laurent Rineau <laurent.rineau__fedora_extras@normalesup.org> - 3.3-0.1.RC1
- New upstream version: 3.3-RC1
- Obsolete patches CGAL-3.2.1-build-libCGALQt-shared.patch,
                   CGAL-3.2.1-build-no-static-lib.patch,
                   CGAL-3.2.1-config.h-endianness_detection.patch.
  These patchs have been merged and adapted by upstream.
- New option --disable-static
- Shipped OpenNL and CORE have been renamed by upstream:
    - %%{_includedir}/OpenNL is now %%{_includedir}/CGAL/OpenNL
    - %%{_includedir}/CORE is now %%{_includedir}/CGAL/CORE
    - libCORE has been rename libCGALcore++
  Reasons:
    - CGAL/OpenNL is a special version of OpenNL, rewritten for CGAL 
      in C++ by the OpenNL author,
    - CGAL/CORE is a fork of CORE-1.7. CORE-1.7 is no longer maintained by 
      its authors, and CORE-2.0 is awaited since 2004.
  In previous releases of this package, CORE was excluded from the package, 
  because %%{_includedir}/CORE/ was a name too generic (see comment #8 of
  #bug #199168). Since the headers of CORE have been moved to
  %%{_includedir}/CGAL/CORE, CORE is now shipped with CGAL.
- move %%{_datadir}/CGAL/make/makefile to %%{_sysconfdir}/CGAL/makefile
(because it is a config file).

* Thu Nov  2 2006 Laurent Rineau <laurent.rineau__fedora_extras@normalesup.org> - 3.2.1-19
- Fix CGAL-3.2.1-build-libCGALQt-shared.patch (bug #213675)

* Fri Sep 15 2006 Laurent Rineau <laurent.rineau__fedora_extras@normalesup.org> - 3.2.1-18
- Move LICENSE.OPENNL to %%doc CGAL-devel (bug #206575).

* Mon Sep 11 2006 Laurent Rineau <laurent.rineau__fedora_extras@normalesup.org> - 3.2.1-17
- libCGALQt.so needs -lGL
- remove %%{_bindir}/cgal_make_macosx_app

* Mon Sep 11 2006 Laurent Rineau <laurent.rineau__fedora_extras@normalesup.org> - 3.2.1-16
- Remove CORE support. Its acceptance in Fedora is controversial (bug #199168).
- Exclude .vcproj files from the -demos-source subpackage.
- Added a patch to build *shared* library libCGALQt.
- Added a patch to avoid building static libraries.
- Fixed the License: tag.

* Thu Aug 17 2006 Laurent Rineau <laurent.rineau__fedora_extras@normalesup.org> - 3.2.1-15
- Change the permissions of %%{_sysconfdir}/profile.d/cgal.*sh
- Remove the meta package CGAL. CGAL-libs is renamed CGAL.
- Added two patchs:
  - CGAL-3.2.1-config.h-endianness_detection.patch which is an upstream patch
    to fix the endianness detection, so that is is no longer hard-coded in
    <CGAL/compiler_config.h>,
  - CGAL-3.2.1-install_cgal-no_versions_in_compiler_config.h.patch that
    removes hard-coded versions in <CGAL/compiler_config.h>.

* Wed Aug 16 2006 Laurent Rineau <laurent.rineau__fedora_extras@normalesup.org> - 3.2.1-14
- Simplified spec file, for Fedora Extras.

* Mon Jul 17 2006 Laurent Rineau <laurent.rineau__fedora_extras@normalesup.org> - 3.2.1-13
- Change CGAL-README.Fedora, now that Installation.pdf is no longer in the
tarball.

* Mon Jul 17 2006 Laurent Rineau <laurent.rineau__fedora_extras@normalesup.org> - 3.2.1-12
- Remove unneeded  -R/-L/-I flags from %%{_datadir}/CGAL/make/makefile

* Mon Jul 17 2006 Laurent Rineau <laurent.rineau__fedora_extras@normalesup.org> - 3.2.1-11
- Fix the soversion.
- Fix %%{cgal_prefix} stuff!!
- Quote 'EOF', so that the lines are not expanded by the shell.

* Tue Jul  4 2006 Laurent Rineau <laurent.rineau__fedora_extras@normalesup.org> - 3.2.1-10
- Fix makefile.sed so that %%{buildroot} does not appear in 
  %%{_datadir}/CGAL/make/makefile.

* Sun Jul  2 2006 Laurent Rineau <laurent.rineau__fedora_extras@normalesup.org> - 3.2.1-9
- Remove Obsoletes: in the meta-package CGAL.

* Sun Jul  2 2006 Laurent Rineau <laurent.rineau__fedora_extras@normalesup.org> - 3.2.1-8
- Fix the localisation of demo and examples.

* Sun Jul  2 2006 Laurent Rineau <laurent.rineau__fedora_extras@normalesup.org> - 3.2.1-6
- Set Requires, in sub-packages.

* Sun Jul  2 2006 Laurent Rineau <laurent.rineau__fedora_extras@normalesup.org> - 3.2.1-5
- CGAL-3.2.1
- Sub-package "demo" is now named "demos-source" (Fedora guidelines).
- Fix some rpmlint warnings
- Added README.Fedora, to explain why the documentation is not shipped, and how CGAL is divided in sub-packages.


* Sat Jul  1 2006 Laurent Rineau <laurent.rineau__fedora_extras@normalesup.org> - 3.2-4
- Use %%{_datadir}/CGAL instead of %%{_datadir}/%%{name}-%%{version}
- Fix %%{_datadir}/CGAL/makefile, with a sed script.
- Added a new option %%set_prefix (see top of spec file).

* Sat Jul  1 2006 Laurent Rineau <laurent.rineau__fedora_extras@normalesup.org> - 3.2-3
- Use less "*" in %%files, to avoid futur surprises.
- Remove %%{_sysconfdir}/profile.d/cgal.* from %%files if %%cgal_prefix is not empty.
- Fix %%build_doc=0 when %%fedora is set. New option macro: %%force_build_doc.

* Fri Jun 30 2006 Laurent Rineau <laurent.rineau__fedora_extras@normalesup.org> - 3.2-2
- Fix some end-of-lines in %%prep, to please rpmlint.

* Mon May 22 2006 Laurent Rineau <laurent.rineau__fedora_extras@normalesup.org> - 3.2-1
- Remove README from %%doc file: it describes the tarball layout.
- Updated to CGAL-3.2.
- Added examples in the -demo subpackage.
- Cleaning up, to follow Fedora Guidelines.
- The -doc subpackage cannot be build on Fedora (no license).
- Add ldconfig back.
- No prefix.

* Fri Apr 28 2006 Laurent Rineau <laurent.rineau__fc_extra@normalesup.org> - 3.2-0.447
- Update to CGAL-3.2-447.

* Fri Apr 21 2006 Laurent Rineau <laurent.rineau__fc_extra@normalesup.org> - 3.2-0.440
- Updated to CGAL-3.2-I-440.

* Wed Apr 19 2006 Laurent Rineau <laurent.rineau__fc_extra@normalesup.org> - 3.2-0.438
- Added a patch to install_cgal, to require support for BOOST, BOOST_PROGRAM_OPTIONS, X11, GMP, MPFR, GMPXX, CORE, ZLIB, and QT.
- Move scripts to %%{_bindir}
- %%{_libdir}/CGAL-I now belong to CGAL and CGAL-devel, so that it disappears when the packages are removed.

* Wed Apr 12 2006 Laurent Rineau <laurent.rineau__fc_extra@normalesup.org> - 3.2-0.431
- Updated to CGAL-3.2-I-431.
- Remove the use of ldconfig.
- Changed my email address.
- No longer need for patch0.
- Pass of rpmlint.
- Remove unneeded Requires: tags (rpm find them itself).
- Change the release tag.
- Added comments at the beginning of the file.
- Added custom ld flags, on 64bits archs (so that X11 is detected).

* Tue Apr 11 2006 Laurent Rineau <laurent.rineau__fc_extra@normalesup.org>
- Removed -g and -O2 from CUSTOM_CXXFLAGS, in the makefile only.
  They are kept during the compilation of libraries.
- Added zlib in dependencies.
- Added a patch to test_ZLIB.C, until it is merged upstream.

* Fri Mar 31 2006 Naceur MESKINI <nmeskini@sophia.inria.fr>
- adding a test in the setup section.

* Mon Mar 13 2006 Naceur MESKINI <nmeskini@sophia.inria.fr>
- delete the patch that fixes the perl path.
- add build_doc and build_demo flags.

* Fri Mar 10 2006 Naceur MESKINI <nmeskini@sophia.inria.fr>
- Adding new sub-packages doc(pdf&html) and demo.
- Add internal_release flag. 

* Thu Mar 09 2006 Naceur MESKINI <nmeskini@sophia.inria.fr>
- Cleanup a specfile.

