#
# Conditional build:
%bcond_without	static_libs	# static library
# these functionalities require kernel patches to work (check defines in <linux/if_alg.h>)
%bcond_with	kernel_asym	# ALG_OP_SIGN/ALG_OP_VERIFY interfaces
%bcond_with	kernel_kpp	# ALG_OP_KEYGEN/ALG_OP_SSGEN interfaces
#
Summary:	Linux Kernel Crypto API User Space Interface Library
Summary(pl.UTF-8):	Biblioteka interfejsu przestrzeni użytownika do API kryptograficznego jądra Linuksa
Name:		libkcapi
Version:	1.2.1
Release:	1
License:	BSD or GPL v2
Group:		Libraries
#Source0Download: https://www.chronox.de/libkcapi.html
Source0:	https://www.chronox.de/libkcapi/%{name}-%{version}.tar.xz
# Source0-md5:	a1fb22270ac8ed3b0f8b5a561f26607d
URL:		https://www.chronox.de/libkcapi.html
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	libtool >= 2:2
BuildRequires:	tar >= 1:1.22
BuildRequires:	xmlto
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libkcapi allows user-space to access the Linux kernel crypto API.

libkcapi uses this Netlink interface and exports easy to use APIs so
that a developer does not need to consider the low-level Netlink
interface handling.

The library does not implement any cipher algorithms. All consumer
requests are sent to the kernel for processing. Results from the
kernel crypto API are returned to the consumer via the library API.

The kernel interface and therefore this library can be used by
unprivileged processes.

%description -l pl.UTF-8
libkcapi pozwala na dostęp z przestrzeni użytkownika do API
kryptograficznego jądra Linuksa.

libkcapi wykorzystuje ten interfejs Netlink i eksportuje łatwe w
użyciu API, dzięki czemu programista nie musi obsługiwać
niskopoziomowego interfejsu Netlink.

Biblioteka nie implementuje żadnych algorytmów szyfrów. Wszystkie
żądania konsumenckie są wysyłane do przetworzenia przez jądro.
Wyniki z API kryptograficznego jądra są zwracane do konsumenta
poprzez API biblioteki.

Interfejs jądra, a więc także ta biblioteka, może być używana przez
procesy nieuprzywilejowane.

%package devel
Summary:	Header files for libkcapi library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libkcapi
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libkcapi library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libkcapi.

%package static
Summary:	Static libkcapi library
Summary(pl.UTF-8):	Statyczna biblioteka libkcapi
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libkcapi library.

%description static -l pl.UTF-8
Statyczna biblioteka libkcapi.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	--enable-kcapi-dgstapp \
	--enable-kcapi-encapp \
	--enable-kcapi-rngapp \
	%{?with_kernel_asym:--enable-lib-asym} \
	%{?with_kernel_kpp:--enable-lib-kpp} \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libkcapi.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES.md COPYING COPYING.bsd README.md TODO
%attr(755,root,root) %{_bindir}/kcapi-dgst
%attr(755,root,root) %{_bindir}/kcapi-enc
%attr(755,root,root) %{_bindir}/kcapi-rng
%attr(755,root,root) %{_libdir}/libkcapi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libkcapi.so.1
%{_mandir}/man1/kcapi-dgst.1*
%{_mandir}/man1/kcapi-enc.1*
%{_mandir}/man1/kcapi-rng.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libkcapi.so
%{_includedir}/kcapi.h
%{_pkgconfigdir}/libkcapi.pc
%{_mandir}/man3/kcapi_*.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libkcapi.a
%endif
