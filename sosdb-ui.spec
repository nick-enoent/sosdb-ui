%define _topdir 	/home/nick/projects/sosdb-ui-package
%define buildroot	%{_topdir}/%{name}

BuildRoot:	%{buildroot}
Name:		sosdb-ui
Version:	1.3
Requires:	sosdb >= 3.4
Release:	1%{?dist}
Summary:	This is web GUI for monitoring OVIS.

Group:		%{_grp}
License:	GPLv2 or BSD
URL:		http://www.ogc.us
Source0:	%{name}.tar.gz

BuildRequires:	libtool swig python-devel
Prefix:		/var/www/sos_web_svcs

%description
Ovis Monitoring Web GUI

%prep
rm -rf $RPM_BULD_DIR/%{name}
%setup -n %{name}

%build
./autogen.sh
./configure --prefix=%{prefix}
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}


%files
%doc README.md
%defattr(-,root,root)
%{prefix}

%changelog

