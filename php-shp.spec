%define modname shp
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A54_%{modname}.ini

Summary:	A libshape wrapper extension for php
Name:		php-%{modname}
Version:	0.9.2
Release:	15
Group:		Development/PHP
License:	PHP License
URL:		https://pecl.php.net/package/shape
Source0:	http://pecl.php.net/get/shape-%{version}.tgz
Patch0:		shape-0.9.2-php54x.diff
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	libshapelib-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Extension that wraps libshape, provides the ability to write programs for
manipulating ESRI shapefiles.

%prep

%setup -q -n shape-%{version}
%patch0 -p0

%build
%serverbuild
export CFLAGS="$CFLAGS -I%{_includedir}/libshp"

phpize

%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}
%make

mv modules/*.so .

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

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
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
[ "../package.xml" != "/" ] && rm -f ../package.xml

%files 
%defattr(-,root,root)
%doc CREDITS README tests
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


%changelog
* Sun May 06 2012 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-14mdv2012.0
+ Revision: 797025
- fix build
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-13
+ Revision: 761291
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-12
+ Revision: 696467
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-11
+ Revision: 695462
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-10
+ Revision: 646682
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-9mdv2011.0
+ Revision: 629868
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-8mdv2011.0
+ Revision: 628182
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-7mdv2011.0
+ Revision: 600528
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-6mdv2011.0
+ Revision: 588866
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-5mdv2010.1
+ Revision: 514651
- rebuilt for php-5.3.2

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-4mdv2010.1
+ Revision: 485480
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-3mdv2010.1
+ Revision: 468251
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-2mdv2010.0
+ Revision: 451636
- fix build
- rebuild
- 0.9.2

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 0.9.1-18mdv2010.0
+ Revision: 397597
- Rebuild

* Mon May 18 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-17mdv2010.0
+ Revision: 377026
- rebuilt for php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-16mdv2009.1
+ Revision: 346607
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-15mdv2009.1
+ Revision: 341797
- rebuilt against php-5.2.9RC2

* Thu Jan 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-14mdv2009.1
+ Revision: 323071
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-13mdv2009.1
+ Revision: 310305
- rebuilt against php-5.2.7

* Fri Jul 18 2008 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-12mdv2009.0
+ Revision: 238429
- rebuild

* Fri May 02 2008 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-11mdv2009.0
+ Revision: 200268
- rebuilt for php-5.2.6

* Mon Feb 04 2008 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-10mdv2008.1
+ Revision: 162111
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Nov 11 2007 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-9mdv2008.1
+ Revision: 107717
- restart apache if needed

* Sat Sep 01 2007 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-8mdv2008.0
+ Revision: 77575
- rebuilt against php-5.2.4

* Thu Jun 14 2007 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-7mdv2008.0
+ Revision: 39523
- use distro conditional -fstack-protector

* Fri Jun 01 2007 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-6mdv2008.0
+ Revision: 33876
- rebuilt against new upstream version (5.2.3)

* Thu May 03 2007 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-5mdv2008.0
+ Revision: 21356
- rebuilt against new upstream version (5.2.2)


* Thu Feb 08 2007 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-4mdv2007.0
+ Revision: 117631
- rebuilt against new upstream version (5.2.1)

* Wed Nov 08 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-3mdv2007.1
+ Revision: 78103
- rebuilt for php-5.2.0
- Import php-shp

* Mon Aug 28 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-2
- rebuilt for php-5.1.6

* Fri Aug 04 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-1mdv2007.0
- initial Mandriva package

