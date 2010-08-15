%define lib_major		4
%define lib_name		%mklibname %{name} %{lib_major}
%define lib_name_devel		%mklibname %{name} -d
%define lib_name_static_devel	%mklibname %{name} -d -s

Summary:	Multiple-precision floating-point computations with correct rounding
Name:		mpfr
Version:	3.0.0
Release:	%mkrel 3
Epoch:		0
License:	LGPLv3+
Group:		System/Libraries
URL:		http://www.mpfr.org/
Source0:	http://www.mpfr.org/mpfr-current/mpfr-%{version}.tar.xz
Patch0:		mpfr-3.0.0-official-patch-1.patch
BuildRequires:	libgmp-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
Requires(post):	info-install
Requires(preun):	info-install
Requires:	%{lib_name} = %{epoch}:%{version}-%{release}
Provides:	lib%{name}-devel = %{epoch}:%{version}-%{release}
Provides:	%{name}-devel = %{epoch}:%{version}-%{release}
Obsoletes:	%mklibname -d %name 1

%description -n %{lib_name_devel}
The development headers and libraries for the MPFR library.

%package -n %{lib_name_static_devel}
Summary:	Static libraries for MPFR
Group:		Development/C
Requires:	%{lib_name_devel} = %{epoch}:%{version}-%{release}
Provides:	lib%{name}-static-devel = %{epoch}:%{version}-%{release}
Provides:	%{name}-static-devel = %{epoch}:%{version}-%{release}
Obsoletes:	%mklibname -d -s %name 1

%description -n %{lib_name_static_devel}
Static libraries for the MPFR library.

%prep
%setup -q
%patch0 -p1

%build
%configure2_5x \
	--enable-shared \
	--enable-thread-safe

%make

%install
%{__rm} -rf %{buildroot}
%makeinstall_std

rm -rf installed-docs
mv %{buildroot}%{_docdir}/%{name} installed-docs

%check
make check

%if %mdkversion < 200900
%post -n %{lib_name} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{lib_name} -p /sbin/ldconfig
%endif

%post -n %{lib_name_devel}
%_install_info %{name}.info

%preun -n %{lib_name_devel}
%_remove_install_info %{name}.info

%clean
%{__rm} -rf %{buildroot}

%files -n %{lib_name}
%defattr(-,root,root)
%{_libdir}/libmpfr.so.%{lib_major}*

%files -n %{lib_name_devel}
%defattr(-,root,root)
%doc installed-docs/*
%{_includedir}/mpfr.h
%{_includedir}/mpf2mpfr.h
%{_infodir}/mpfr.info*
%{_libdir}/libmpfr.la 
%{_libdir}/libmpfr.so

%files -n %{lib_name_static_devel}
%defattr(-,root,root)
%{_libdir}/libmpfr.a
