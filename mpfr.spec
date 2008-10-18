%define lib_major               1
%define lib_name                %mklibname %{name} %{lib_major}
%define lib_name_devel          %mklibname %{name} -d
%define lib_name_static_devel   %mklibname %{name} -d -s

Name:           mpfr
Version:        2.3.2
Release:        %mkrel 1
Epoch:          0
Summary:        Multiple-precision floating-point computations with correct rounding
License:        LGPL 
Group:          System/Libraries
URL:            http://www.mpfr.org/
Source0:        http://www.mpfr.org/mpfr-current/mpfr-%{version}.tar.lzma
BuildRequires:  libgmp-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
The MPFR library is a C library for multiple-precision
floating-point computations with correct rounding. 

%package -n %{lib_name}
Summary:        Multiple-precision floating-point computations with correct rounding
Group:          System/Libraries

%description -n %{lib_name}
The MPFR library is a C library for multiple-precision
floating-point computations with correct rounding. 

%package -n %{lib_name_devel}
Summary:        Development headers and libraries for MPFR
Group:          Development/C
Requires(post): info-install
Requires(preun): info-install
Requires:       %{lib_name} = %{epoch}:%{version}-%{release}
Provides:       lib%{name}-devel = %{epoch}:%{version}-%{release}
Provides:       %{name}-devel = %{epoch}:%{version}-%{release}
Obsoletes:	%mklibname -d %name 1

%description -n %{lib_name_devel}
The development headers and libraries for the MPFR library.

%package -n %{lib_name_static_devel}
Summary:        Static libraries for MPFR
Group:          Development/C
Requires:       %{lib_name_devel} = %{epoch}:%{version}-%{release}
Provides:       lib%{name}-static-devel = %{epoch}:%{version}-%{release}
Provides:       %{name}-static-devel = %{epoch}:%{version}-%{release}
Obsoletes:	%mklibname -d -s %name 1

%description -n %{lib_name_static_devel}
Static libraries for the MPFR library.

%prep
%setup -q

%build
%{configure2_5x} --enable-shared
%{make}

%install
%{__rm} -rf %{buildroot}
%{makeinstall_std}

%check
%{make} check

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
%defattr(0644,root,root,0755)
%doc AUTHORS BUGS COPYING COPYING.LIB FAQ.html INSTALL NEWS README TODO VERSION
%defattr(-,root,root,0755)
%{_libdir}/libmpfr.so.%{lib_major}*

%files -n %{lib_name_devel}
%defattr(-,root,root,0755)
%{_includedir}/mpfr.h
%{_includedir}/mpf2mpfr.h
%{_infodir}/mpfr.info*
%{_libdir}/libmpfr.la 
%{_libdir}/libmpfr.so

%files -n %{lib_name_static_devel}
%defattr(-,root,root,0755)
%{_libdir}/libmpfr.a
