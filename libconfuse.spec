#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
%define		_name confuse
Summary:	libConfuse - a library for parsing configuration files
Summary(pl.UTF-8):	libConfuse - biblioteka do analizy plików konfiguracyjnych
Name:		libconfuse
Version:	2.7
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://savannah.nongnu.org/download/%{_name}/%{_name}-%{version}.tar.gz
# Source0-md5:	45932fdeeccbb9ef4228f1c1a25e9c8f
Patch0:		%{name}-no_tests.patch
URL:		http://www.nongnu.org/confuse/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake > 1.6.3
BuildRequires:	gettext-devel >= 0.16.1
BuildRequires:	libtool > 1.4.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libConfuse is a configuration file parser library written in C. It
supports sections and (lists of) values (strings, integers, floats,
booleans or other sections), as well as some other features (such as
single/double-quoted strings, environment variable expansion,
functions and nested include statements).

It makes it very easy to add configuration file capability to a
program using a simple API. libConfuse aims to be easy to use and
quick to integrate with your code.

%description -l pl.UTF-8
Biblioteka libConfuse jest analizatorem plików konfiguracyjnych.
Napisana została w języku C. Plik konfiguracyjny może zawierać sekcje
i listę wartości następujących typów: napisy, liczby całkowite,
zmiennoprzecinkowe, wartości logiczne. Napisy mogą być z pojedynczym
lub podwójnym cudzysłowem. Zmienne środowiskowe są rozwijane. Można
używać funkcji i zagnieżdżać wyrażenia.

Biblioteka umożliwia w prosty sposób dodanie do programu obsługę
plików konfiguracyjnych używając prostego API. libConfuse ma być
biblioteką prostą w użyciu i pozwalać na szybką integrację z kodem
programu.

%package devel
Summary:	Header files for libConfuse library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libConfuse
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This is the package containing the header files for libConfuse
library.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe biblioteki libConfuse.

%package static
Summary:	Static libConfuse library
Summary(pl.UTF-8):	Statyczna biblioteka libConfuse
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libConfuse library.

%description static -l pl.UTF-8
Statyczna biblioteka libConfuse.

%prep
%setup -q -n %{_name}-%{version}
# %patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
CPPFLAGS="-DYY_NO_INPUT"
%configure \
	%{!?with_static_libs:--disable-static} \
	--enable-shared

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_examplesdir}/%{name}-%{version},%{_mandir}/man3,%{_pkgconfigdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install doc/man/man3/* $RPM_BUILD_ROOT%{_mandir}/man3

rm -rf examples/{ftpconf,reread,simple,*.o}
install examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%find_lang %{_name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{_name}.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
%attr(755,root,root) %{_libdir}/libconfuse.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libconfuse.so.0

%files devel
%defattr(644,root,root,755)
%doc doc/html doc/tutorial-html
%attr(755,root,root) %{_libdir}/libconfuse.so
%{_libdir}/libconfuse.la
%{_includedir}/confuse.h
%{_pkgconfigdir}/libconfuse.pc
%{_mandir}/man3/cfg_*.3*
%{_mandir}/man3/confuse.h.3*
%{_examplesdir}/%{name}-%{version}

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libconfuse.a
%endif
