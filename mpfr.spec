%define major 4
%define libname	%mklibname %{name} %{major}
%define devname	%mklibname %{name} -d
%define statname %mklibname %{name} -d -s
%bcond_with	crosscompile
%bcond_without	uclibc

Summary:	Multiple-precision floating-point computations with correct rounding
Name:		mpfr
Version:	3.1.2
Release:	12
License:	LGPLv3+
Group:		System/Libraries
Url:		http://www.mpfr.org/
Source0:	http://www.mpfr.org/mpfr-current/mpfr-%{version}.tar.xz
BuildRequires:	gmp-devel
%if %{with uclibc}
# macro not in released rpm yet..
%define lib_soname() %(\
[ -e %{?!2:%{_libdir}}%{?2}/lib%{1}.so ] && \
objdump -p %{?!2:%{_libdir}}%{?2}/lib%{1}.so | grep -e SONAME | sed -e 's#.*\\\(lib.*\\\)\$#\\\1#g'\
)
# for bootstrapping...
BuildRequires:	uclibc-%(echo %{lib_soname gmp} | sed -e 's#lib#%{_lib}#' -e 's#\.so\.##')
BuildRequires:	uClibc-devel
%endif

%description
The MPFR library is a C library for multiple-precision
floating-point computations with correct rounding. 

%package -n %{libname}
Summary:	Multiple-precision floating-point computations with correct rounding
Group:		System/Libraries

%description -n %{libname}
The MPFR library is a C library for multiple-precision
floating-point computations with correct rounding. 

%package -n uclibc-%{libname}
Summary:	Multiple-precision floating-point computations with correct rounding (uClibc)
Group:		System/Libraries

%description -n uclibc-%{libname}
The MPFR library is a C library for multiple-precision
floating-point computations with correct rounding. 

%package -n %{devname}
Summary:	Development headers and libraries for MPFR
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
The development headers and libraries for the MPFR library.

%package -n %{statname}
Summary:	Static libraries for MPFR
Group:		Development/C
Requires:	%{devname} = %{EVRD}
Provides:	%{name}-static-devel = %{EVRD}

%description -n %{statname}
Static libraries for the MPFR library.

%prep
%setup -q

%build
CONFIGURE_TOP=$PWD

%if %{with uclibc}
mkdir -p uclibc
pushd uclibc
%uclibc_configure \
	--enable-shared \
	--enable-static \
%if %{with crosscompile}
	--with-gmp-lib=%{_prefix}/%{_target_platform}/sys-root%{_libdir} \
%endif
	--enable-thread-safe
%make
popd
%endif

mkdir -p glibc
pushd glibc
%configure \
	--enable-shared \
	--enable-static \
%if %{with crosscompile}
	--with-gmp-lib=%{_prefix}/%{_target_platform}/sys-root%{_libdir} \
%endif
	--enable-thread-safe
%make
popd

%install
%if %{with uclibc}
%makeinstall_std -C uclibc
rm -r %{buildroot}%{uclibc_root}%{_docdir}/%{name}
%endif

%makeinstall_std -C glibc

rm -rf installed-docs
mv %{buildroot}%{_docdir}/%{name} installed-docs

%check
make -C glibc check

%files -n %{libname}
%{_libdir}/libmpfr.so.%{major}*

%if %{with uclibc}
%files -n uclibc-%{libname}
%{uclibc_root}%{_libdir}/libmpfr.so.%{major}*
%endif

%files -n %{devname}
%doc installed-docs/*
%{_includedir}/mpfr.h
%{_includedir}/mpf2mpfr.h
%{_infodir}/mpfr.info*
%{_libdir}/libmpfr.so
%if %{with uclibc}
%{uclibc_root}%{_libdir}/libmpfr.so
%endif

%files -n %{statname}
%{_libdir}/libmpfr.a
%if %{with uclibc}
%{uclibc_root}%{_libdir}/libmpfr.a
%endif
