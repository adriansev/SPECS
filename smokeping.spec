%{?filter_setup:
%filter_provides_in %{_datadir}/%{name}/
%filter_from_requires /perl(Authen::.*)/d; /perl(Net::OpenSSH)/d; /Smokeping/d
%filter_setup
}

Summary:          Latency Logging and Graphing System
Name:             smokeping
Version:          2.7.3
Release:          1%{?dist}
License:          GPLv2+
URL:              https://oss.oetiker.ch/smokeping/
Source0:          https://oss.oetiker.ch/smokeping/pub/smokeping-%{version}.tar.gz
Source1:          smokeping.service
Source2:          smokeping-httpd.conf.d
Source3:          http://oss.oetiker.ch/smokeping-demo/img/smokeping.png
Source4:          http://oss.oetiker.ch/smokeping-demo/img/rrdtool.png
Source5:          README.fedora
Source6:          smokeping-tmpfs.conf
Source7:          smokeping-httpd24.conf.d
Patch0:           smokeping-2.7.0-paths.patch
Patch1:           smokeping-2.7.0-config.patch
Patch2:           smokeping-2.6.7-silence.patch
Patch3:           smokeping-2.7.0-no-3rd-party.patch
Patch4:           smokeping-2.6.9-remove-date.patch
BuildRequires:    glibc-common
BuildRequires:    systemd-units
BuildRequires:    perl-generators
BuildRequires:    perl(Authen::Radius)
BuildRequires:    perl(CGI)
BuildRequires:    perl(CGI::Fast)
BuildRequires:    perl(Config::Grammar)
BuildRequires:    perl(Digest::HMAC_MD5)
BuildRequires:    perl(ExtUtils::Manifest)
BuildRequires:    perl(ExtUtils::MakeMaker)
BuildRequires:    perl(FCGI)
BuildRequires:    perl(File::Basename)
BuildRequires:    perl(Getopt::Long)
BuildRequires:    perl(IO::Pty)
BuildRequires:    perl(IO::Socket::SSL)
BuildRequires:    perl(LWP)
BuildRequires:    perl(Net::Telnet)
BuildRequires:    perl(Net::OpenSSH)
BuildRequires:    perl(Net::SNMP)
BuildRequires:    perl(Net::LDAP)
BuildRequires:    perl(Net::DNS)
BuildRequires:    perl(Pod::Usage)
BuildRequires:    perl(POSIX)
BuildRequires:    perl(RRDs)
BuildRequires:    perl(Socket6)
BuildRequires:    perl(SNMP_Session)
BuildRequires:    perl(SNMP_util) >= 1.13
BuildRequires:    perl(strict) 
BuildRequires:    perl(Sys::Hostname)
BuildRequires:    perl(Sys::Syslog)
BuildRequires:    perl(URI::Escape)
BuildRequires:    perl(vars)
BuildRequires:    /usr/bin/pod2man
BuildRequires:    automake
BuildRequires:    autoconf
Requires:         perl-interpreter >= 5.6.1
Requires:         rrdtool >= 1.0.33
Requires:         fping >= 2.4b2
Requires:         traceroute
# Not picked up for some reason
Requires:         perl(Config::Grammar)
Requires:         perl(SNMP_util) >= 1.13
# only httpd supported without config changes
Requires:         httpd
Requires:         mod_fcgid
BuildArch:        noarch

%description
SmokePing is a latency logging and graphing system. It consists of a
daemon process which organizes the latency measurements and a CGI
which presents the graphs.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

install -p -m 0644 %{SOURCE5} .
iconv -f ISO-8859-1 -t utf-8 -o CHANGES.utf8 CHANGES
touch -r CHANGES CHANGES.utf8 
mv CHANGES.utf8 CHANGES

# remove some external modules
rm -f lib/{SNMP_Session,SNMP_util,BER}.pm
rm -rf thirdparty/
[ -e VERSION ] || echo %{version} > VERSION

%build
autoreconf --force --install --verbose --make

%configure --with-htdocs-dir=%{_datadir}/%{name}/htdocs \
           --disable-silent-rules

%install
make install DESTDIR=%{buildroot}

# Some additional dirs and files
install -d %{buildroot}%{_localstatedir}/lib/%{name}/{rrd,images} \
                %{buildroot}%{_localstatedir}/run/%{name} \
                %{buildroot}%{_datadir}/%{name}/cgi
install -Dp -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
%if 0%{?fedora} >= 18
install -Dp -m 0644 %{SOURCE7} %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf
%else
install -Dp -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf
%endif
install  -p -m 0644 %{SOURCE3} %{SOURCE4} %{buildroot}%{_datadir}/%{name}/htdocs
install -Dp -m 0644 %{SOURCE6} %{buildroot}%{_tmpfilesdir}/%{name}.conf

# Fix some files
for f in config basepage.html smokemail tmail smokeping_secrets ; do
    mv %{buildroot}%{_sysconfdir}/%{name}/$f.dist \
       %{buildroot}%{_sysconfdir}/%{name}/$f
done
mv %{buildroot}%{_sysconfdir}/%{name}/examples __examples
mv %{buildroot}%{_bindir}/%{name}_cgi %{buildroot}%{_datadir}/%{name}/cgi
ln -s %{name}_cgi %{buildroot}%{_datadir}/%{name}/cgi/%{name}.fcgi
rm -f %{buildroot}%{_datadir}/%{name}/htdocs/smokeping.fcgi.dist

%post
%systemd_post smokeping.service

%preun
%systemd_preun smokeping.service

%postun
%systemd_postun_with_restart smokeping.service

%files
%license COPYRIGHT LICENSE
%doc CHANGES CONTRIBUTORS README TODO README.fedora
%doc __examples/*
%{_sbindir}/%{name}
%{_bindir}/smokeinfo
%{_bindir}/tSmoke
%{_unitdir}/%{name}.service
%dir %{_sysconfdir}/%{name}
%attr(0640, root, apache) %config(noreplace) %{_sysconfdir}/%{name}/config
%config(noreplace) %{_sysconfdir}/%{name}/basepage.html
%config(noreplace) %{_sysconfdir}/%{name}/smokemail
%attr(0640, root, root) %config(noreplace) %{_sysconfdir}/%{name}/smokeping_secrets
%config(noreplace) %{_sysconfdir}/%{name}/tmail
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%{_tmpfilesdir}/%{name}.conf
%{_datadir}/%{name}
%dir %{_localstatedir}/lib/%{name}
%{_localstatedir}/lib/%{name}/rrd
%{_localstatedir}/run/%{name}
%attr(0755, apache, root) %{_localstatedir}/lib/%{name}/images
%{_mandir}/man1/%{name}*.1*
%{_mandir}/man1/tSmoke.1*
%{_mandir}/man3/Smokeping_*.3*
%{_mandir}/man5/%{name}_*.5*
%{_mandir}/man7/%{name}_*.7*

%changelog
* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Apr 16 2018 Terje Rosten <terje.rosten@ntnu.no> - 2.7.2-1
- 2.7.2

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Feb 05 2018 Terje Rosten <terje.rosten@ntnu.no> - 2.7.1-1
- 2.7.1

* Tue Oct 24 2017 Terje Rosten <terje.rosten@ntnu.no> - 2.6.11-7
- Update docs, resolving rhbz#1500881

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 13 2017 Petr Pisar <ppisar@redhat.com> - 2.6.11-5
- perl dependency renamed to perl-interpreter
  <https://fedoraproject.org/wiki/Changes/perl_Package_to_Install_Core_Modules>

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.6.11-4
- Rebuild due to bug in RPM (RHBZ #1468476)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 13 2017 Ville Skyttä <ville.skytta@iki.fi> - 2.6.11-2
- Move tmpfiles.d config to %%{_tmpfilesdir}

* Tue Oct 25 2016 Terje Rosten <terje.rosten@ntnu.no> - 2.6.11-1
- 2.6.11
- fix service file (rhbz#1388583)

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Oct 30 2014 Terje Rosten <terje.rosten@ntnu.no> - 2.6.10-1
- 2.6.10

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 26 2014 Terje Rosten <terje.rosten@ntnu.no> - 2.6.9-3
- Fix build

* Wed Mar 26 2014 Terje Rosten <terje.rosten@ntnu.no> - 2.6.9-2
- Let MTA add date header (bz #1080949)

* Mon Aug 05 2013 Terje Rosten <terje.rosten@ntnu.no> - 2.6.9-1
- 2.6.9

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 26 2013 Petr Pisar <ppisar@redhat.com> - 2.6.8-5
- Perl 5.18 rebuild
- Build-require Smokeping.pm dependencies as it is run when generating
  documentation
- Escape solidus in POD link

* Wed Feb 20 2013 Terje Rosten <terje.rosten@ntnu.no> - 2.6.8-4
- Fix buildreq.

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Dec 15 2012 Terje Rosten <terje.rosten@ntnu.no> - 2.6.8-2
- httpd 2.4 in FC 18 needs care (bz #871480)

* Thu Sep 06 2012 Terje Rosten <terje.rosten@ntnu.no> - 2.6.8-1
- 2.6.8
- Fix fping issue (bz #854572)
- Explicit dep on httpd (not just webserver) (bz #854804)

* Tue Aug 28 2012 Terje Rosten <terje.rosten@ntnu.no> - 2.6.7-4
- Convert to new set of macros for scripts

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 09 2012 Terje Rosten <terje.rosten@ntnu.no> - 2.6.7-2
- Fix perl filtering

* Sun Feb 05 2012 Terje Rosten <terje.rosten@ntnu.no> - 2.6.7-1
- Switch to mod_fcgid as default
- Refresh patchset
- 2.6.7

* Sun Jan 22 2012 Terje Rosten <terje.rosten@ntnu.no> - 2.4.2-16
- Add patch to fix CVE-2012-0790 (#783584)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep 9 2011 Tom Callaway <spot@fedoraproject.org> - 2.4.2-14
- Add missing systemd scriptlets

* Fri Sep 9 2011 Tom Callaway <spot@fedoraproject.org> - 2.4.2-13
- Convert to systemd

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 Terje Rosten <terje.rosten@ntnu.no> - 2.4.2-11
- Add tmpfiles.d file to fix #656690

* Sun Aug 16 2009 Terje Rosten <terje.rosten@ntnu.no> - 2.4.2-10
- Add patch to fix #497746

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Oct 27 2008 Terje Rosten <terje.rosten@ntnu.no> - 2.4.2-7
- Add some SELinux information, thanks to wolfy for help
  with this and other improvements.

* Sat Oct 18 2008 Terje Rosten <terje.rosten@ntnu.no> - 2.4.2-6
- Fix README.fedora

* Sun Oct  5 2008 Terje Rosten <terje.rosten@ntnu.no> - 2.4.2-5
- move Qooxdoo::JSONRPC to separate package

* Tue Sep 16 2008 Terje Rosten <terje.rosten@ntnu.no> - 2.4.2-4
- Use mv macro
- Fix cut-n-paste error in rm lines
- Remove perl as buildreq

* Mon Sep 15 2008 Terje Rosten <terje.rosten@ntnu.no> - 2.4.2-3
- Fix perms on writeable dir for apache
- More sane handling of external perl modules
- Add smoketrace instructions and patches

* Sat Aug 23 2008 Terje Rosten <terje.rosten@ntnu.no> - 2.4.2-2
- Fix README.fedora
- New rpm is picky, fixed

* Sat Aug 23 2008 Terje Rosten <terje.rosten@ntnu.no> - 2.4.2-1
- 2.4.2

* Thu Jul  3 2008 Terje Rosten <terje.rosten@ntnu.no> - 2.4.1-1
- 2.4.1

* Mon Apr  7 2008 Terje Rosten <terje.rosten@ntnu.no> - 2.3.5-1
- 2.3.5
- More or less a complete rewrite

* Sun Jan 14 2007 Wil Cooley <wcooley@nakedape.cc> - 2.0.9-2
- Disable internal dependency generator; I was doing this in my ~/.rpmmacros,
  which probably isn't a good idea.

* Tue Dec 05 2006 Wil Cooley <wcooley@nakedape.cc> - 2.0.9-1
- Updated to 2.0.9.
- Use 'dist' variable like Fedora Extras instead of vendor_tag and dist_tag.
- Do chkconfig/service in the correct places with appropriate checks.

* Wed Nov 09 2005 Wil Cooley <wcooley@nakedape.cc> - 2.0.4-0.0
- Updated to 2.0.4.
- Filter requirements for some internally-provided or optional modules.

* Tue Jun 21 2005 Wil Cooley <wcooley@nakedape.cc> - 2.0-0.2rc5
- Added chkconfig in post and preun sections.
- Changed some permissions to make rpmlint less unhappy.

* Thu Jun 16 2005 Wil Cooley <wcooley@nakedape.cc> - 2.0-2.nac.0.5
- Updated for 2.0rc5.

* Wed Mar 17 2004 Wil Cooley <wcooley@nakedape.cc> 1.28-2.nac
- Rebuilt for 1.28.
- Removed unnecessary stuff for setting up Apache.

* Fri Mar 12 2004 Curtis Doty <Curtis@GreenKey.net>
- [1.27] rebuilt without issue

* Sun Jan 25 2004 Curtis Doty <Curtis@GreenKey.net>
- [1.25] merge with upstream and hanecak
- add dependency on new perl-PersistentPerl (SpeedyCGI)
- use working config in the right location
- more rabid decrufting of hard-coded references to rrdtool

* Mon Oct 06 2003 Curtis Doty <Curtis@GreenKey.net>
- [1.24] merge with upstream
- change default config and doc to reflect loss coloring accurately
- rebuild man pages and html to reflect above, but forget txt
- remove IfModule mod_alias.c since apache2 cannot handle

* Thu Oct  2 2003 Peter Hanecak <hanecak@megaloman.sk> 1.23-1
- changed group from Networking/Utilities to Applications/Internet

* Wed Jul 30 2003 Curtis Doty <Curtis@GreenKey.net>
- [1.23] bump and build
- fix on Shrike since libnet subsumed by perl-5.8 and we really only
  need Net:SNMP out of it anyways
- quick hacks to make apache 2 compatible

* Tue Dec 17 2002 Curtis Doty <Curtis@GreenKey.net>
- [1.18] with some cosmetic changes
- add perl-libnet dependency neede for at least Net::SMTP
- maxhight patch so apache puts temp files in imgcache dir not datadir
- prefer my config.dist

* Sat Nov 02 2002 Curtis Doty <Curtis@GreenKey.net>
- [1.16] with updated specfile
- fix perms on /var/smokeping so apache cannot write
- fork and distribute my own defailt config instead of patching the
  screwey one that comes in the tarball

* Tue Mar 12 2002 Curtis Doty <Curtis@GreenKey.net>
- [1.5] with a bunch of my additions including SysV init script

* Tue Feb 19 2002 Curtis Doty <Curtis@GreenKey.net>
- new rpm package [1.1]
