%define major 4
%define libname	%mklibname %{name} %{major}
%define devname	%mklibname %{name} -d
%define statname %mklibname %{name} -d -s
# -Oz causes the testsuite to crash
%global optflags -Os -g
%bcond_with	crosscompile
%bcond_with	uclibc

Summary:	Multiple-precision floating-point computations with correct rounding
Name:		mpfr
Version:	3.1.3
Release:	5
License:	LGPLv3+
Group:		System/Libraries
Url:		http://www.mpfr.org/
Source0:	http://www.mpfr.org/mpfr-current/mpfr-%{version}.tar.xz
Source1:	%{name}.rpmlintrc
# Version from 2016-02-23
Patch0:		http://www.mpfr.org/mpfr-current/allpatches
BuildRequires:	gmp-devel
%if %{with uclibc}
# for bootstrapping...
BuildRequires:	uclibc-gmp-devel
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

%if %{with uclibc}
%package -n uclibc-%{libname}
Summary:	Multiple-precision floating-point computations with correct rounding (uClibc)
Group:		System/Libraries

%description -n uclibc-%{libname}
The MPFR library is a C library for multiple-precision
floating-point computations with correct rounding. 

%package -n uclibc-%{devname}
Summary:	Development headers and libraries for MPFR
Group:		Development/C
Requires:	uclibc-%{libname} = %{EVRD}
Requires:	%{devname} = %{EVRD}
Provides:	uclibc-%{name}-devel = %{EVRD}
Conflicts:	%{devname} < 3.1.3-2

%description -n uclibc-%{devname}
The development headers and libraries for the MPFR library.
%endif

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
%apply_patches

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

%files -n uclibc-%{devname}
%{uclibc_root}%{_libdir}/libmpfr.so
%{uclibc_root}%{_libdir}/libmpfr.a
%endif

%files -n %{devname}
%doc installed-docs/*
%{_includedir}/mpfr.h
%{_includedir}/mpf2mpfr.h
%{_infodir}/mpfr.info*
%{_libdir}/libmpfr.so

%files -n %{statname}
%{_libdir}/libmpfr.a
