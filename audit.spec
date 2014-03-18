Summary:	Kernel auditing
Name:		audit
Version:	2.3.5
Release:	1
License:	GPL v2+
Group:		Daemons
Source0:	http://people.redhat.com/sgrubb/audit/%{name}-%{version}.tar.gz
# Source0-md5:	755ac2dbe766cc74aa6c7bd54be61b9f
URL:		http://people.redhat.com/sgrubb/audit/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libcap-ng-devel
BuildRequires:	libtool
Requires(post,preun,postun):	systemd-units
Requires:	%{name}-libs = %{version}-%{release}
Requires:	systemd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The audit package contains the user space utilities for storing and
processing the audit records generate by the audit subsystem in the
Linux 2.6 kernel.

%package libs
Summary:	Dynamic audit libraries
License:	LGPL v2.1+
Group:		Libraries

%description libs
The audit-libs package contains the dynamic libraries needed for
applications to use the audit framework.

%package devel
Summary:	Header files for audit libraries
License:	LGPL v2.1+
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
The audit-devel package contains the header files needed for
developing applications that need to use the audit framework library.

%prep
%setup -q

sed 's#swig/Makefile ##' -i configure.ac
sed 's/swig//' -i Makefile.am

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-static	\
	--enable-systemd=yes	\
	--with-python=no
%{__make}
%{__make} -C auparse

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_var}/log/audit,%{systemdunitdir}} \
	$RPM_BUILD_ROOT%{_sysconfdir}/audit/rules.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT	\
	auditrdir=%{_sysconfdir}/audit

%{__make} -C auparse install \
	DESTDIR=$RPM_BUILD_ROOT

install lib/libaudit.h $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%post
%systemd_post auditd.service

%preun
%systemd_preun auditd.service

%postun
%systemd_postun

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README THANKS TODO
%attr(750,root,root) %{_bindir}/aulast
%attr(750,root,root) %{_bindir}/aulastlog
%attr(750,root,root) %{_bindir}/ausyscall
%attr(750,root,root) %{_bindir}/auvirt

%attr(750,root,root) %{_sbindir}/audispd
%attr(750,root,root) %{_sbindir}/audispd-zos-remote
%attr(750,root,root) %{_sbindir}/auditctl
%attr(750,root,root) %{_sbindir}/auditd
%attr(750,root,root) %{_sbindir}/augenrules
%attr(750,root,root) %{_sbindir}/aureport
%attr(750,root,root) %{_sbindir}/ausearch
%attr(750,root,root) %{_sbindir}/autrace
%attr(755,root,root) %{_sbindir}/audisp-remote

%dir %{_sysconfdir}/audisp
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/audisp/zos-remote.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/audisp/audisp-remote.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/audisp/audispd.conf
%dir %{_sysconfdir}/audisp/plugins.d
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/audisp/plugins.d/af_unix.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/audisp/plugins.d/au-remote.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/audisp/plugins.d/audispd-zos-remote.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/audisp/plugins.d/syslog.conf
%dir %{_sysconfdir}/audit
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/audit/auditd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/audit/audit.rules

# placeholder
%dir %{_sysconfdir}/audit/rules.d

%{systemdunitdir}/auditd.service

%attr(750,root,root) %dir %{_var}/log/audit
%{_mandir}/man5/*.5*
%{_mandir}/man7/*.7*
%{_mandir}/man8/*.8*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libaudit.so.1
%attr(755,root,root) %ghost %{_libdir}/libauparse.so.0
%attr(755,root,root) %{_libdir}/libaudit.so.*.*.*
%attr(755,root,root) %{_libdir}/libauparse.so.*.*.*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libaudit.conf
%{_mandir}/man5/libaudit.conf.5*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/*.h
%{_mandir}/man3/*.3*

