%define major 7
%define libname %mklibname %{name}
%define devname %mklibname %{name} -d

%bcond_with bootstrap

%global optflags %{optflags} -O3

Summary:	JPEG-2000 utilities
Name:		jasper
Version:	4.2.8
Release:	1
License:	BSD-like
Group:		Graphics
Url:		https://www.ece.uvic.ca/~mdadams/jasper/
Source0:	https://github.com/jasper-software/jasper/releases/download/version-%{version}/jasper-%{version}.tar.gz
BuildRequires:	pkgconfig(libjpeg)
%if %{without bootstrap}
BuildRequires:	pkgconfig(glut)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(xmu)
%endif

BuildSystem:    cmake

BuildOption:    -DJAS_ENABLE_LATEX:BOOL=OFF
BuildOption: 	 -DJAS_ENABLE_CXX:BOOL=ON
# not really, but it errors if not enabled
BuildOption:    -DALLOW_IN_SOURCE_BUILD:BOOL=ON

%description
JasPer is a software-based implementation of the codec specified in the
emerging JPEG-2000 Part-1 standard (i.e., ISO/IEC 15444-1).  This package
contains tools for working with JPEG-2000 images.

%package -n %{libname}
Summary:	Libraries for JasPer
Group:		System/Libraries

%description -n %{libname}
This package contains a library for working with JPEG-2000 images.

%package -n %{devname}
Summary:	Development tools for programs which will use the libjasper library
Group:		Development/C
Requires:	%{libname} >= %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package contains the development files for %{name}.


%files
%{_bindir}/imgcmp
%{_bindir}/imginfo
%{_bindir}/jasper
%{_mandir}/man1/imgcmp.1*
%{_mandir}/man1/imginfo.1*
%{_mandir}/man1/jasper.1*
%if ! %{with bootstrap}
%{_bindir}/jiv
%{_mandir}/man1/jiv.1*
%endif

%files -n %{libname}
%{_libdir}/libjasper.so.%{major}*

%files -n %{devname}
%doc doc/jpeg2000.pdf
%doc %{_docdir}/JasPer
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_libdir}/libjasper.so
%{_libdir}/pkgconfig/jasper.pc
