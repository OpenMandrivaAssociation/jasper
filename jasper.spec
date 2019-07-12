%define major 4
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

%bcond_with bootstrap

%global optflags %{optflags} -O3

Summary:	JPEG-2000 utilities
Name:		jasper
Version:	2.0.16
Release:	1
License:	BSD-like
Group:		Graphics
Url:		http://www.ece.uvic.ca/~mdadams/jasper/
Source0:	https://github.com/mdadams/jasper/releases/jasper-version-%{version}.tar.gz
Patch0:		jasper-1.900.1-fix-filename-buffer-overflow.patch
BuildRequires:	pkgconfig(libjpeg)
%if %{without bootstrap}
BuildRequires:	pkgconfig(glut)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(xmu)
%endif
BuildRequires:	cmake
BuildRequires:	ninja

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

%prep
%autosetup -n %{name}-version-%{version} -p1
mv doc/README doc/README.pdf

find -type d |xargs chmod 755
find -type f |xargs chmod 644
sed -r 's|(CMAKE_SKIP_BUILD_RPATH) FALSE|\1 TRUE|g' -i CMakeLists.txt

%cmake -G Ninja

%build
%ninja -C build

%install
%ninja_install -C build

%files
%doc README LICENSE
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
%doc doc/README.pdf doc/jasper.pdf doc/jpeg2000.pdf
%doc %{_docdir}/JasPer
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_libdir}/libjasper.so
%{_libdir}/pkgconfig/jasper.pc
