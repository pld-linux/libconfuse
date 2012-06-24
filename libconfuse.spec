#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
%define		_name confuse

Summary:	libConfuse - a library for parsing configuration files
Summary(pl):	libConfuse - biblioteka do parsowania plik�w konfiguracyjnych
Name:		libconfuse
Version:	2.5
Release:	0.2
License:	LGPL
Group:		Development/Libraries
Source0:	http://download.savannah.gnu.org/releases/confuse/%{_name}-%{version}.tar.gz
# Source0-md5:	4bc9b73d77ebd571ac834619ce0b3582
Patch0:		%{name}-no_tests.patch
URL:		http://www.nongnu.org/confuse/
BuildRequires:	autoconf
BuildRequires:	automake > 1.6.3
BuildRequires:	gettext-devel >= 0.14.1
BuildRequires:	libtool > 1.4.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libConfuse is a configuration file parser library, licensed under the
terms of the LGPL, and written in C. It supports sections and (lists
of) values (strings, integers, floats, booleans or other sections), as
well as some other features (such as single/double-quoted strings,
environment variable expansion, functions and nested include
statements).

It makes it very easy to add configuration file capability to a
program using a simple API. The goal of libConfuse is not to be *the*
configuration file parser library with a gazillion of features.
Instead, it aims to be easy to use and quick to integrate with your
code.

%description -l pl
Biblioteka libConfuse jest parserem plik�w konfiguracyjnych. Napisana
zosta�a w j�zyku C na licencji LGPL. Plik konfiguracyjny mo�e zawiera�
sekcje i list� warto�ci nast�puj�cych typ�w: napisy, liczby ca�kowite,
zmiennoprzecinkowe, warto�ci logiczne. Napisy mog� by� z pojedynczym
lub podw�jnym cudzys�owem. Zmienne �rodowiskowe s� rozwijane. Mo�na
u�ywa� funkcji i zagnie�d�a� wyra�enia.

Biblioteka umo�liwia w prosty spos�b dodanie do programu obs�ug�
plik�w konfiguracyjnych u�ywaj�c prostego API. Celem libConfuse nie
jest stworzenie parsera plik�w z milionem funkcji, ale prostej
biblioteki umo�liwiaj�cej szybk� integracj� z kodem programu.

%package devel
Summary:	Header files for libConfuse library
Summary(pl):	Pliki nag��wkowe biblioteki libConfuse
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This is the package containing the header files for libConfuse
library.

%description devel -l pl
Ten pakiet zawiera pliki nag��wkowe biblioteki libConfuse.

%package static
Summary:	Static libConfuse library
Summary(pl):	Statyczna biblioteka libConfuse
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libConfuse library.

%description static -l pl
Statyczna biblioteka libConfuse.

%prep
%setup -q -n %{_name}-%{version}
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--%{?with_static_libs:en}%{!?with_static_libs:dis}able-static \
	--enable-shared

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_examplesdir}/%{name}-%{version},%{_mandir}/man3}

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
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%doc doc/html doc/tutorial-html
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/*.h
%{_pkgconfigdir}/*
%{_mandir}/man3/*
%{_examplesdir}/%{name}-%{version}

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%endif
