%define modname dbus
%define dirname %{modname}
%define soname %{modname}.so
%define inifile B14_%{modname}.ini

Summary:	Extension for interaction with DBUS busses
Name:		php-%{modname}
Version:	0.1.1
Release:	6
Group:		Development/PHP
License:	PHP
URL:		https://pecl.php.net/package/DBus
Source0:	http://pecl.php.net/get/dbus-%{version}.tgz
Source1:	B14_dbus.ini
BuildRequires:	pkgconfig
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	dbus-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This extension allows you to talk to DBUS services on a system, and also act as
a DBUS service.

%prep

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

cp %{SOURCE1} %{inifile}

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" config.m4

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}
%make
mv modules/*.so .

%install
rm -rf %{buildroot} 

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/
install -m0644 %{inifile} %{buildroot}%{_sysconfdir}/php.d/%{inifile}

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc package*.xml
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}



%changelog
* Thu May 03 2012 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-5mdv2012.0
+ Revision: 795422
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-4
+ Revision: 761213
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-3
+ Revision: 696406
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-2
+ Revision: 695379
- rebuilt for php-5.3.7

* Thu Jun 23 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-1
+ Revision: 686774
- 0.1.1

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-2
+ Revision: 646623
- rebuilt for php-5.3.6

* Tue Mar 01 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-1
+ Revision: 641088
- import php-dbus


* Tue Mar 01 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-1mdv2011.0
- initial Mandriva package
