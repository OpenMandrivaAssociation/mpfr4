%define major 4
%define libname	%mklibname %{name} %{major}
%define devname	%mklibname %{name} -d
%define statname %mklibname %{name} -d -s
%bcond_with crosscompile
%bcond_with devel

# (tpg) optimize it a bit
%global optflags %optflags -O3

Summary:	Old version of the MPFR library
Name:		mpfr4
Version:	3.1.6
Release:	5
License:	LGPLv3+
Group:		System/Libraries
Url:		http://www.mpfr.org/
Source0:	http://www.mpfr.org/mpfr-current/mpfr-%{version}.tar.xz
# (tpg) upstream patches
Patch0:		http://www.mpfr.org/mpfr-current/patch01
BuildRequires:	gmp-devel

%description
The MPFR library is a C library for multiple-precision
floating-point computations with correct rounding. 

This is an old version provided for compatibility with
legacy applications only. Use the mpfr package instead.

%package -n %{libname}
Summary:	Multiple-precision floating-point computations with correct rounding
Group:		System/Libraries

%description -n %{libname}
The MPFR library is a C library for multiple-precision
floating-point computations with correct rounding. 

%if %{with devel}
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
%endif

%prep
%setup -qn mpfr-%{version}
%autopatch -p1

%build
%ifarch %{arm}
# For some reason, mpfr forces gcc
# but gcc generates __modsi3 calls when it should
# be generating __aeabi_modsi3 instead
export CC=clang
export CXX=clang++
%endif

%configure \
	--enable-shared \
%if %{with devel}
	--enable-static \
%endif
%if %{with crosscompile}
	--with-gmp-lib=%{_prefix}/%{_target_platform}/sys-root%{_libdir} \
%endif
	--enable-thread-safe

if "$?" != "0"; then
	echo "configure failed, here's config.log:"
	cat config.log
	exit 1
fi

%make

%install
%makeinstall_std

%if %{with devel}
rm -rf installed-docs
mv %{buildroot}%{_docdir}/%{name} installed-docs
%endif

%if ! %{with devel}
rm -rf %{buildroot}%{_includedir} \
	%{buildroot}%{_infodir} \
	%{buildroot}%{_libdir}/*.so \
	%{buildroot}%{_docdir}
%endif

%ifnarch aarch64
%check
make check
%endif

%files -n %{libname}
%{_libdir}/libmpfr.so.%{major}*

%if %{with devel}
%files -n %{devname}
%{_includedir}/mpfr.h
%{_includedir}/mpf2mpfr.h
%{_infodir}/mpfr.info*
%{_libdir}/libmpfr.so

%files -n %{statname}
%{_libdir}/libmpfr.a
%endif
