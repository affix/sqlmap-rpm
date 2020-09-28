# binaries are exploits, intended to be used on remote systems
%define _binaries_in_noarch_packages_terminate_build 0

# exclude binaries from dependencies computing
%global __requires_exclude_from ^%{_datadir}/%{name}/udf/.*$
%global __provides_exclude_from ^%{_datadir}/%{name}/udf/.*$

Name:           sqlmap
Version:        1.3.4.44
Release:        dev
Summary:        Automatic SQL injection and database takeover tool
Group:          Security
License:        GPL
URL:            http://sqlmap.org/
Source0:        %{name}-%{version}.tar.gz 
BuildArch:      noarch
Requires:       python3-requests

%description
sqlmap is an open source penetration testing tool that automates the process
of detecting and exploiting SQL injection flaws and taking over of database
servers. It comes with a powerful detection engine, many niche features for
the ultimate penetration tester and a broad range of switches lasting from
database fingerprinting, over data fetching from the database, to accessing
the underlying file system and executing commands on the operating system
via out-of-band connections.

%prep
%setup -q -n sqlmapproject-sqlmap-c1bf36b

%install
install -d -m 755 %{buildroot}%{_datadir}/%{name}
install -m 755 sqlmap.py %{buildroot}%{_datadir}/%{name}
cp -pr extra %{buildroot}%{_datadir}/%{name}
cp -pr lib %{buildroot}%{_datadir}/%{name}
cp -pr plugins %{buildroot}%{_datadir}/%{name}
cp -pr data %{buildroot}%{_datadir}/%{name}
cp -pr thirdparty %{buildroot}%{_datadir}/%{name}

install -d -m 755 %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/sqlmap <<'EOF'
#!/bin/sh
cd %{_datadir}/%{name}
./sqlmap.py "$@"
EOF
chmod +x %{buildroot}%{_bindir}/sqlmap

sed -i 's|/usr/bin/env python$|/usr/bin/python3|' %{buildroot}%{_datadir}/%{name}/*.py %{buildroot}%{_datadir}/%{name}/*/*/*.py

install -d -m 755 %{buildroot}%{_sysconfdir}
install -m 644 sqlmap.conf %{buildroot}%{_sysconfdir}
pushd %{buildroot}%{_datadir}/%{name}
ln -s ../../..%{_sysconfdir}/sqlmap.conf .

%files
%doc doc/*
%{_datadir}/%{name}
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}.conf

%changelog
* Mon Sep 28 2020 Keiran Smith <contact@keiran.scot> 1.3.4.44-dev
- new package

