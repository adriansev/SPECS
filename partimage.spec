%bcond_without login
%bcond_without pam
%bcond_without ssl

%define image_place  %{_localstatedir}/partimaged

%if %{with login}
%define lstat enabled
%else
%define lstat disabled
%endif

Summary: Partition imaging utility, much like Ghost
Name:    partimage
Version: 0.6.9
Release: 12%{?dist}
License: GPLv2+
Group:   Applications/System
URL:     http://www.partimage.org/
Source0: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Source1: %{name}-man.tar.gz
Source2: %{name}-scripts.tar.gz
Source3: README.partimage.html
Source4: partimaged.service
Patch0:  partimage-0.6.9-gzFile.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gettext
BuildRequires: autoconf 
BuildRequires: bzip2-devel
BuildRequires: libmcrypt-devel 
BuildRequires: newt-devel 
BuildRequires: parted-devel
BuildRequires: zlib-devel
%{?with_pam:BuildRequires: pam-devel}
%{?with_ssl:BuildRequires: openssl-devel}

Requires(post):   chkconfig, systemd-units, systemd-sysv
Requires(postun): chkconfig, shadow-utils, systemd-units
Requires(preun):  chkconfig, initscripts, systemd-units
Requires(pre):    shadow-utils

%description
Partimage is a Linux/UNIX partition imaging utility,
which saves partitions, having a supported filesystem, to an image file.
Partimage will only copy data from the used portions of the partition.
The image file can be compressed with gzip or bzip2 to save space, 
and can be split into multiple files to be copied on CDs/DVDs.

Partimage was compiled with login %{lstat}, 
and supporting the following filesystems:

  ext2fs, ext3fs, fat, fat16, fat32, hfs, hpfs, jfs,
  ntfs, reiserfs, reiserfs-3.5, reiserfs-3.6, ufs, xfs.

%package server
Summary: Server daemon for remote imaging, much like Ghost
Group: System Environment/Daemons
%{?with_pam:Requires: db4-utils}

%description server
Partimage is a Linux/UNIX partition imaging utility,
which saves partitions, having a supported filesystem, to an image file.
Partitions can be saved across the network, by using the partimage 
network support, or using Samba / NFS. 

This package contains the server daemon for remote imaging.

%prep
%setup -q -a1 -a2
%patch0 -p1 -b .gzFile
for i in ./README ./ChangeLog ./THANKS ./README.partimaged; do
        iconv -f iso-8859-1 -t utf-8 < "$i" > "${i}_"
        mv "${i}_" "$i"
done

# Disable chowning of files
%{__perl} -pi.orig -e 's|^\tchown partimag:root.*$|\\|' Makefile.in

# Fix mkinstalldirs during 'make install' in po/
%{__perl} -pi.orig -e 's|^(mkinstalldirs) = .+$|$1 = %{__mkdir_p}|' po/Makefile.in.in

%{__cat} <<EOF >partimaged.sysconfig
# See partimaged --help for more information on these options.
#
# NOTE: The client has always to be run as root.
# For the server being able to authenticate, the client has to be compiled 
# with login enabled. Otherwise, a "version mismatch" error occurs.
# Use --nossl, and restart partimaged, to disable ssl encription.
#
%if %{with ssl}
OPTIONS="--port=4025 --dest %{image_place}"
%else
OPTIONS="--port=4025 --nossl --dest %{image_place}"
%endif
EOF

%if %{with pam}
%{__cat} <<EOF >partimaged.pam
#%PAM-1.0

# Log access to partimaged
auth     required     pam_warn.so

# partimaged user database
auth     sufficient   pam_userdb.so db=%{_sysconfdir}/partimaged/passwd

# Only allow local users listed in partimagedusers to connect to partimaged
auth     required     pam_listfile.so onerr=fail item=user sense=allow file=%{_sysconfdir}/partimaged/partimagedusers

# partimaged user database
account  sufficient   pam_userdb.so debug db=%{_sysconfdir}/partimaged/passwd
EOF
%endif

%{__cat} <<EOF >partimaged.logrotate
%{_localstatedir}/log/partimaged/partimage*.log {
        missingok
        copytruncate
        notifempty
}
EOF

%build

%configure \
        --program-prefix="%{?_program_prefix}" \
        --with-log-dir="%{_localstatedir}/log/partimaged" \
        --with-xinerama \
        %{!?with_ssl:--disable-ssl} \
        %{!?with_login:--disable-login} \
        %{?with_pam:--enable-pam} \
        --enable-gui-text \
        --enable-gui-newt \
        --enable-gui-qt
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%makeinstall
%find_lang %{name}

%{__install} -Dp -m0755 %{SOURCE4} %{buildroot}%{_unitdir}/partimaged.service
%{__install} -Dp -m0644 partimaged.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/partimaged
%{__install} -Dp -m0644 partimaged.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/partimaged

%{__install} -d -m0755 %{buildroot}%{_localstatedir}/log/partimaged
touch %{buildroot}%{_localstatedir}/log/partimaged/partimaged.log

%{__install} -d -m0755 %{buildroot}%{image_place}
%{__install} -Dp -m0644 partimage.1 %{buildroot}%{_mandir}/man1/partimage.1
%{__install} -Dp -m0644 partimaged.8 %{buildroot}%{_mandir}/man8/partimaged.8
%{__install} -Dp -m0644 partimagedusers.5 %{buildroot}%{_mandir}/man5/partimagedusers.5

%{__install} -Dp -m0644 partimage-certs.cnf %{buildroot}%{_sysconfdir}/partimaged/partimage-certs.cnf
%{__install} -Dp -m0744 partimage-create_certificates.sh %{buildroot}%{_datadir}/partimaged/create_certificates.sh
%{__install} -Dp -m0644 %{SOURCE3} %{_builddir}/%{name}-%{version}

%if %{with pam}
%{__install} -Dp -m0644 partimaged.pam %{buildroot}%{_sysconfdir}/pam.d/partimaged
%{__install} -Dp -m0644 partimaged-passwd.8 %{buildroot}%{_mandir}/man8/partimaged-passwd.8
%{__install} -Dp -m0744 partimaged-passwd %{buildroot}%{_datadir}/partimaged/partimaged-passwd
%endif


%pre server
getent group partimag >/dev/null || groupadd -r partimag
getent passwd partimag >/dev/null || \
/usr/sbin/useradd -r -g partimag -d %{image_place} -s /sbin/nologin \
-c "Partition imaging utility" partimag
exit 0

%post server
%systemd_post partimaged.service

%triggerun -- partimaged < 0.6.9-4
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply partimaged
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save partimaged >/dev/null 2>&1 ||:

# If the package is allowed to autostart:
/bin/systemctl --no-reload enable partimaged.service >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del partimaged >/dev/null 2>&1 || :
/bin/systemctl try-restart partimaged.service >/dev/null 2>&1 || :

%preun server
%systemd_preun partimaged.service

%postun server
%systemd_postun_with_restart partimaged.service 

%clean
%{__rm} -rf %{buildroot}

%files -f %{name}.lang
%defattr(-, root, root, 0755)
%doc AUTHORS BUGS ChangeLog COPYING FORMAT README* THANKS
%{_sbindir}/partimage
%{_mandir}/man1/partimage.1*
%exclude %{_docdir}/partimage

%files server
%defattr(-, root, root, 0755)
%doc AUTHORS BUGS ChangeLog COPYING FORMAT README* THANKS
%{_unitdir}/partimaged.service
%config(noreplace) %{_sysconfdir}/logrotate.d/partimaged
%config(noreplace) %{_sysconfdir}/sysconfig/partimaged
%dir %{_datadir}/partimaged
%if %{with pam}
%config(noreplace) %{_sysconfdir}/pam.d/partimaged
%{_datadir}/partimaged/partimaged-passwd
%{_mandir}/man8/partimaged-passwd.8*
%endif
%{_datadir}/partimaged/create_certificates.sh
%{_mandir}/man8/partimaged.8*
%{_mandir}/man5/partimagedusers.5*
%{_sbindir}/partimaged
%ghost %{_localstatedir}/log/partimaged/partimaged.log

%defattr(-, partimag, partimag, 0755)
%config(noreplace) %{_sysconfdir}/partimaged/
%dir %{_localstatedir}/log/partimaged
%dir %{image_place}

%changelog
* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.9-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.9-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.6.9-10
- Rebuilt for GCC 5 C++11 ABI change

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Sep 01 2012 Paulo Roma <roma@lcg.ufrj.br> - 0.6.9-5
- Using new systemd macros.
- Changed Requires compat-db for db4-utils.
- Fix incorrect usage only detected with zlib-1.2.6 and later
  gzFile *" should be "gzFile".

* Sun Jul 15 2012 Paulo Roma <roma@lcg.ufrj.br> - 0.6.9-4
- Using native systemd.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 05 2010 Paulo Roma <roma@lcg.ufrj.br> - 0.6.9-1
- Updated to 0.6.9.
- Fixed user creation.
- Removed gcc4 patch.
- No more deleting partimag user upon package removal.

* Thu Nov 26 2009 Paulo Roma <roma@lcg.ufrj.br> - 0.6.8-2
- Patched for gcc44 (Fedora 12).

* Mon Nov 23 2009 Paulo Roma <roma@lcg.ufrj.br> - 0.6.8-1
- Updated 0.6.8
- Removed all patches.
- Enabled ssl to match SystemRescueCD's client.

* Thu Feb 26 2009 Paulo Roma <roma@lcg.ufrj.br> - 0.6.7-7
- Patched for gcc-4.4.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild 

* Mon Dec 02 2008 Paulo Roma <roma@lcg.ufrj.br> - 0.6.7-5
- Owning %%{_datadir}/partimaged.
- Corrected Source URL.
- Removed macro home.
- Changed script permissions to 0744.
- Removed unneeded usermod.
- Deleted the created user in the %%postun section.

* Mon Dec 01 2008 Paulo Roma <roma@lcg.ufrj.br> - 0.6.7-4
- Changed default build to login and pam enabled.
- Added short explanation on how to use partimaged-passwd.

* Wed Nov 26 2008 Paulo Roma <roma@lcg.ufrj.br> - 0.6.7-3
- Added README.partimage.html
- Added BR zlib-devel.
- Added Requires compat-db for pam support.

* Wed Feb 06 2008 Paulo Roma <roma@lcg.ufrj.br> - 0.6.7-2
- Converted files to utf8.
- Patched for gcc-4.3.
- Added missing man pages.
- Using Source1 for creating %%{_initrddir}/partimaged
- Changed license.
- Created %%{image_place}.
- Conditional login, pam and ssl support.
- Changed pam.warn.so for pam_warn.so
- Added certificate generation and password script creation. 

* Wed Feb 06 2008 Paulo Roma <roma@lcg.ufrj.br> - 0.6.7-1
- Updated to release 0.6.7.
- Using find lang.
- Removed %%exclude %%{_infodir}

* Thu Aug 16 2007 Dag Wieers <dag@wieers.com> - 0.6.6-1
- Updated to release 0.6.6.

* Mon Dec 18 2006 Dag Wieers <dag@wieers.com> - 0.6.5-1
- Updated to release 0.6.5.

* Sat Mar 06 2004 Dag Wieers <dag@wieers.com> - 0.6.4-1
- Updated to release 0.6.4.

* Tue Jul 31 2003 Dag Wieers <dag@wieers.com> - 0.6.2-1
- Added seperate server package.

* Wed Jul 30 2003 Dag Wieers <dag@wieers.com> - 0.6.2-0
- Initial package. (using DAR)
