Summary:	SBLIM CMPI Service instrumentation
Summary(pl.UTF-8):	Przyrządy pomiarowe usług dla SBLIM CMPI
Name:		sblim-cmpi-service
Version:	0.8.2
Release:	1
License:	CPL v1.0
Group:		Libraries
Source0:	http://downloads.sourceforge.net/sblim/%{name}-%{version}.tar.bz2
# Source0-md5:	5a6f26f316334b5d221f2780959dc410
URL:		http://sblim.sourceforge.net/
BuildRequires:	sblim-cmpi-base-devel
BuildRequires:	sblim-cmpi-devel
Requires:	%{name}-libs = %{version}-%{release}
Requires:	sblim-cmpi-base
Requires:	sblim-sfcb
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SBLIM CMPI Service providers.

%description -l pl.UTF-8
Dostawcy informacji o usługach dla SBLIM CMPI.

%package libs
Summary:	SBLIM Service instrumentation library
Summary(pl.UTF-8):	Biblioteka pomiarowa SBLIM Service
Group:		Libraries

%description libs
SBLIM Service instrumentation library.

%description libs -l pl.UTF-8
Biblioteka pomiarowa SBLIM Service.

%package devel
Summary:	Header files for SBLIM Service instrumentation library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki pomiarowej SBLIM Service
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for SBLIM Service instrumentation library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki pomiarowej SBLIM Service.

%package static
Summary:	Static SBLIM Service instrumentation library
Summary(pl.UTF-8):	Statyczna biblioteka pomiarowa SBLIM Service
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static SBLIM Service instrumentation library.

%description static -l pl.UTF-8
Statyczna biblioteka pomiarowa SBLIM Service.

%prep
%setup -q

%build
%configure \
	CIMSERVER=sfcb \
	PROVIDERDIR=%{_libdir}/cmpi

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

# modules
%{__rm} $RPM_BUILD_ROOT%{_libdir}/cmpi/lib*.{la,a}
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_datadir}/%{name}/provider-register.sh \
	-r %{_datadir}/%{name}/Linux_Service.registration \
	-m %{_datadir}/%{name}/Linux_Service.mof >/dev/null

%preun
if [ "$1" = "0" ]; then
	%{_datadir}/%{name}/provider-register.sh -d \
		-r %{_datadir}/%{name}/Linux_Service.registration \
		-m %{_datadir}/%{name}/Linux_Service.mof >/dev/null
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README THANKS
%attr(755,root,root) %{_bindir}/listservices
%attr(755,root,root) %{_libdir}/cmpi/libcmpiOSBase_HostedServiceProvider.so*
%attr(755,root,root) %{_libdir}/cmpi/libcmpiOSBase_ServiceProcessProvider.so*
%attr(755,root,root) %{_libdir}/cmpi/libcmpiOSBase_ServiceProvider.so*
%dir %{_datadir}/sblim-cmpi-service
%{_datadir}/sblim-cmpi-service/Linux_Service.mof
%{_datadir}/sblim-cmpi-service/Linux_Service.registration
%attr(755,root,root) %{_datadir}/sblim-cmpi-service/provider-register.sh

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcimlxs.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcimlxs.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcimlxs.so
%{_libdir}/libcimlxs.la
# XXX: shared dir
%dir %{_includedir}/sblim
%{_includedir}/sblim/cimlxs.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libcimlxs.a
