%define lib_major       1
%define lib_name        %mklibname %{name} %{lib_major}

Summary:        Multiple-precision floating-point computations with correct rounding
Name:           mpfr
Version:        2.2.1
Release:        %mkrel 4
Epoch:          0
License:        LGPL 
Group:          System/Libraries
URL:            http://www.mpfr.org/
Source0:        http://www.mpfr.org/mpfr-current/mpfr-2.2.1.tar.bz2
BuildRequires:  libgmp-devel
BuildRoot:      %{_tmppath}/%{name}-%{epoch}:%{version}-%{release}-root

%description
The MPFR library is a C library for multiple-precision
floating-point computations with correct rounding. 

%package -n %{lib_name}
Summary:        Multiple-precision floating-point computations with correct rounding
Group:          System/Libraries

%description -n %{lib_name}
The MPFR library is a C library for multiple-precision
floating-point computations with correct rounding. 

%package -n %{lib_name}-devel
Summary:        Development headers and libraries for MPFR
Group:          Development/C
Requires(post): info-install
Requires(preun): info-install
Requires:       %{lib_name} = %{epoch}:%{version}-%{release}
Provides:       lib%{name}-devel = %{epoch}:%{version}-%{release}
Provides:       %{_lib}%{name}-devel = %{epoch}:%{version}-%{release}
Provides:       %{name}-devel = %{epoch}:%{version}-%{release}

%description -n %{lib_name}-devel
The development headers and libraries for the MPFR library.

%prep
%setup -q

%build
%{configure2_5x} --enable-shared
%{make}

%install
%{__rm} -rf %{buildroot}
%{makeinstall}

%check
%{make} check

%post -n %{lib_name} -p /sbin/ldconfig

%postun -n %{lib_name} -p /sbin/ldconfig

%post -n %{lib_name}-devel
%_install_info %{name}.info

%preun -n %{lib_name}-devel
%_remove_install_info %{name}.info

%clean
%{__rm} -rf %{buildroot}

%files -n %{lib_name}
%defattr(0644,root,root,0755)
%doc AUTHORS BUGS COPYING COPYING.LIB ChangeLog FAQ.html INSTALL NEWS README TODO VERSION
%defattr(-,root,root,0755)
%{_libdir}/libmpfr.so.*

%files -n %{lib_name}-devel
%defattr(-,root,root,0755)
%{_includedir}/mpfr.h
%{_includedir}/mpf2mpfr.h
%{_infodir}/mpfr.info*
%{_libdir}/libmpfr.a
%{_libdir}/libmpfr.la 
%{_libdir}/libmpfr.so
