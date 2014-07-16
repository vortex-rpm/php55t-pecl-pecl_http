%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}
%{!?pecl_phpdir: %{expand: %%global pecl_phpdir  %(%{__pecl} config-get php_dir  2> /dev/null || echo undefined)}}
%{?!pecl_xmldir: %{expand: %%global pecl_xmldir %{pecl_phpdir}/.pkgxml}}

%{!?php_extdir: %{expand: %%global php_extdir %(php-config --extension-dir)}}
%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)

%global php_base php55t
%global pecl_name pecl_http
%global real_name pecl_http

Summary: HTTP extension
Name: %{php_base}-pecl-pecl_http
Version: 2.0.7
Release: 2.vortex%{?dist}
License: PHP
Group: Development/Languages
Vendor: Vortex RPM
URL: http://pecl.php.net/package/%{pecl_name}

Source: http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

Requires: php55t-pecl-raphf, php55t-pecl-propro

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: %{php_base}-devel, %{php_base}-cli, %{php_base}-pear, zlib-devel, php55t-pecl-raphf-devel, php55t-pecl-propro-devel
Requires(post): %{__pecl}
Requires(postun): %{__pecl}

%if %{?php_zend_api}0
Requires: php(zend-abi) = %{php_zend_api}
Requires: php(api) = %{php_core_api}
%else
Requires: %{php_base}-api = %{php_apiver}
%endif

%description
This HTTP extension aims to provide a convenient and powerful
set of functionality for one of PHPs major applications.

It eases handling of HTTP urls, headers and messages, provides
means for negotiation of a client's preferred content type,
language and charset, as well as a convenient way to send any
arbitrary data with caching and resuming capabilities.

It provides powerful request functionality with support for
parallel requests.


%package devel
Group: Development/Languages
Summary: files needed to build PHP extensions
Provides: %{name}-devel = %{version}-%{release}
Provides: %{real_name}-devel = %{version}-%{release}

%description devel
Development files for pecl_http.


%prep
%setup -c -n %{real_name}-%{version} -q


%build
cd %{pecl_name}-%{version}
phpize
%configure
%{__make} %{?_smp_mflags}


%install
cd %{pecl_name}-%{version}
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__cat} > %{buildroot}%{_sysconfdir}/php.d/%{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=raphf.so
extension=propro.so
extension=http.so

EOF

# Install XML package description
# use 'name' rather than 'pecl_name' to avoid conflict with pear extensions
%{__mkdir_p} %{buildroot}%{pecl_xmldir}
%{__install} -m 644 ../package.xml %{buildroot}%{pecl_xmldir}/%{pecl_name}.xml


%clean
%{__rm} -rf %{buildroot}


%post
%{__pecl} install --nodeps --soft --force --register-only --nobuild %{pecl_xmldir}/%{pecl_name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ]; then
%{__pecl} uninstall --nodeps --ignore-errors --register-only %{pecl_name} >/dev/null || :
fi


%files
%defattr(-, root, root, -)
%doc %{pecl_name}-%{version}/CREDITS %{pecl_name}-%{version}/Exceptions.txt %{pecl_name}-%{version}/KnownIssues.txt %{pecl_name}-%{version}/LICENSE %{pecl_name}-%{version}/ThanksTo.txt
%config(noreplace) %{_sysconfdir}/php.d/%{pecl_name}.ini
%{php_extdir}/http.so
%{pecl_xmldir}/%{pecl_name}.xml


%files devel
%defattr(-, root, root, -)
%{_includedir}/php/ext/http/*

%changelog
* Wed Jul 16 2014 Ilya Otyutskiy <ilya.otyutskiy@icloud.com> - 2.0.7-2.vortex
- I officialy hate all the people involved in the PHP project.

* Wed Jul 16 2014 Ilya Otyutskiy <ilya.otyutskiy@icloud.com> - 2.0.7-1.vortex
- Initial packaging.
