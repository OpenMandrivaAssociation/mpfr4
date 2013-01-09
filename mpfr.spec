%define lib_major		4
%define lib_name		%mklibname %{name} %{lib_major}
%define lib_name_devel		%mklibname %{name} -d
%define lib_name_static_devel	%mklibname %{name} -d -s

Summary:	Multiple-precision floating-point computations with correct rounding
Name:		mpfr
Version:	3.1.1
Release:	1
Epoch:		0
License:	LGPLv3+
Group:		System/Libraries
URL:		http://www.mpfr.org/
Source0:	http://www.mpfr.org/mpfr-current/mpfr-%{version}.tar.xz
BuildRequires:	gmp-devel

%description
The MPFR library is a C library for multiple-precision
floating-point computations with correct rounding. 

%package -n %{lib_name}
Summary:	Multiple-precision floating-point computations with correct rounding
Group:		System/Libraries

%description -n %{lib_name}
The MPFR library is a C library for multiple-precision
floating-point computations with correct rounding. 

%package -n %{lib_name_devel}
Summary:	Development headers and libraries for MPFR
Group:		Development/C
Requires:	%{lib_name} = %{EVRD}
Provides:	lib%{name}-devel = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Obsoletes:	%mklibname -d %{name} 1

%description -n %{lib_name_devel}
The development headers and libraries for the MPFR library.

%package -n %{lib_name_static_devel}
Summary:	Static libraries for MPFR
Group:		Development/C
Requires:	%{lib_name_devel} = %{EVRD}
Provides:	lib%{name}-static-devel = %{EVRD}
Provides:	%{name}-static-devel = %{EVRD}
Obsoletes:	%mklibname -d -s %{name} 1

%description -n %{lib_name_static_devel}
Static libraries for the MPFR library.

%prep
%setup -q

%build
%configure2_5x \
	--enable-shared \
	--enable-thread-safe

%make

%install
%__rm -rf %{buildroot}
%makeinstall_std

rm -rf installed-docs
mv %{buildroot}%{_docdir}/%{name} installed-docs

%check
make check

%files -n %{lib_name}
%{_libdir}/libmpfr.so.%{lib_major}*

%files -n %{lib_name_devel}
%doc installed-docs/*
%{_includedir}/mpfr.h
%{_includedir}/mpf2mpfr.h
%{_infodir}/mpfr.info*
%{_libdir}/libmpfr.so

%files -n %{lib_name_static_devel}
%{_libdir}/libmpfr.a
