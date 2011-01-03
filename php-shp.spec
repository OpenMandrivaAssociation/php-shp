%define modname shp
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A54_%{modname}.ini

Summary:	A libshape wrapper extension for php
Name:		php-%{modname}
Version:	0.9.2
Release:	%mkrel 8
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/shape
Source0:	http://pecl.php.net/get/shape-%{version}.tgz
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	libshapelib-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Extension that wraps libshape, provides the ability to write programs for
manipulating ESRI shapefiles.

%prep

%setup -q -n shape-%{version}

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
