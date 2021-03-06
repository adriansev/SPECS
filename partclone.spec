Name:         partclone
Version:      0.2.89
Release:      1%{?dist}
Group:        System/Filesystems
URL:          http://partclone.org/
License:      GPL
Summary:      File System Clone Utilities for xfs, ntfs, fat, exfat, and some other filesystems
Source:       %{name}-%{version}.tar.gz
#Patch:        %{name}-el6-ext2fslib.patch
Prefix:       /usr
BuildRequires: e2fsprogs-devel, xfsprogs-devel, ntfs-3g-devel
#BuildRequires: e2fsprogs-devel, libprogsreiserfs-devel-static, reiser4progs, xfsprogs-devel, ntfs-3g-devel, ncurses-static

%description
A set of file system clone utilities, including (depends on build):
ext2/3, ntfs, xfs, hfs, hfs+, fat, exfat and more...

Authors:
--------
    Thomas Tsai <Thomas _at_ nchc org tw>
    Jazz Wang <jazz _at_ nchc org tw>
    http://partclone.org

%prep
%setup -q
#%if 0%{?rhel} && %{rhel} < 7
#%{error: RHEL=%{rhel}, at least 7 is highly recommended}
#%patch
#%endif

%build
[ -d $RPM_BUILD_ROOT ] && rm -rf $RPM_BUILD_ROOT
./configure --prefix=%{prefix} --enable-extfs --enable-xfs --enable-hfsp --enable-fat --enable-exfat --enable-f2fs --enable-ntfs --enable-btrfs --enable-minix --enable-ncursesw
#./configure --prefix=%{prefix} --enable-all --enable-static --enable-ncursesw LIBS=-ltinfo 
make %{?_smp_mflags} CFLAGS="%{optflags}"

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

%post

%postun
ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS README.md TODO
%doc %{_mandir}/man?/*
%{_sbindir}/*
%{_datadir}/locale/*
%{_datadir}/%{name}/*

%changelog
* Thu Jun 16 2016 - Budy Wuysang <nguik.gnuik@gmail.com>
- Spec adaptation to version 0.2.88 (stable) and RHEL6 or later.
- Patch to enable build on system with ext2fs libs <= 1.41.
- Relocatable package by using prefix: directive.

* Fri May 01 2009 - Steven Shiau <steven _at_ nchc org tw> 0.1.0-10
- New upstream 0.1.0-10.

* Sun Apr 26 2009 - Steven Shiau <steven _at_ nchc org tw> 0.1.0-9
- New upstream 0.1.0-9.

* Fri Apr 24 2009 - Steven Shiau <steven _at_ nchc org tw> 0.1.0-8
- New upstream 0.1.0-8.

* Thu Apr 23 2009 - Steven Shiau <steven _at_ nchc org tw> 0.1.0-7
- New upstream 0.1.0-7.

* Tue Apr 21 2009 - Steven Shiau <steven _at_ nchc org tw> 0.1.0-6
- New upstream 0.1.0-6.

* Fri Apr 17 2009 - Steven Shiau <steven _at_ nchc org tw> 0.1.0-5
- New upstream 0.1.0-5.

* Tue Apr 14 2009 - thomas _at_ nchc.org.tw 0.1.0-2
- update configure for FC10

* Sun Apr 12 2009 - Steven Shiau <steven _at_ nchc org tw> 0.1.0-2
- New upstream 0.1.0.

* Tue Dec 30 2008 - Steven Shiau <steven _at_ nchc org tw> 0.0.9-4
- A bug about FAT12 was fixed by Thomas Tsai.

* Wed Dec 25 2008 - Steven Shiau <steven _at_ nchc org tw> 0.0.9-3
- New upstream 0.0.9-3.

* Mon Dec 22 2008 - Steven Shiau <steven _at_ nchc org tw> 0.0.9-2
- New upstream 0.0.9-2.

* Sun Jun 16 2008 - Steven Shiau <steven _at_ nchc org tw> 0.0.8-3
- New upstream 0.0.8-3.

* Mon May 26 2008 - Steven Shiau <steven _at_ nchc org tw> 0.0.8-2
- New upstream 0.0.8-2.

* Sun May 25 2008 - Steven Shiau <steven _at_ nchc org tw> 0.0.8-1
- New upstream 0.0.8-1.

* Thu Feb 21 2008 - Steven Shiau <steven _at_ nchc org tw> 0.0.6-3
- Bug fixed: clone.fat was not compiled.

* Thu Feb 21 2008 - Steven Shiau <steven _at_ nchc org tw> 0.0.6-1
- New upstream 0.0.6-1.

* Sat Feb 16 2008 - Steven Shiau <steven _at_ nchc org tw> 0.0.5-16
- New upstream 0.0.5-16.

* Mon Feb 04 2008 - Steven Shiau <steven _at_ nchc org tw> 0.0.5-15
- New upstream 0.0.5-15.

* Thu Jan 24 2008 - Steven Shiau <steven _at_ nchc org tw> 0.0.5-10
- New upstream 0.0.5-10.

* Fri Jan 04 2008 - Steven Shiau <steven _at_ nchc org tw> 0.0.5-1
- New upstream 0.0.5-1.

* Thu Jan 03 2008 - Steven Shiau <steven _at_ nchc org tw> 0.0.4-4
- Sync the version number with Debian package.
- Enable static linking.

* Mon Dec 31 2007 - Steven Shiau <steven _at_ nchc org tw> 0.0.1-2
- Some doc and debian rules were added by Thomas Tsai.

* Mon Dec 10 2007 - Steven Shiau <steven _at_ nchc org tw> 0.0.1-1
- Initial release for partclone.
