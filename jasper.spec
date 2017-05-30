%define	major	4
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname %{name} -d

%bcond_without bootstrap

Summary:	JPEG-2000 utilities
Name:		jasper
Version:	2.0.12
Release:	1
License:	BSD-like
Group:		Graphics
Url:		http://www.ece.uvic.ca/~mdadams/jasper/
Source0:	http://www.ece.uvic.ca/~frodo/jasper/software/jasper-%{version}.tar.gz
Patch0:		http://pkgs.fedoraproject.org/cgit/rpms/jasper.git/plain/jasper-1.900.1-CVE-2008-3520.patch

BuildRequires:	jpeg-devel
%if ! %{with bootstrap}
BuildRequires:	pkgconfig(glut)
BuildRequires:	pkgconfig(xmu)
%endif
BuildRequires:	cmake
BuildRequires:	ninja

%description
JasPer is a software-based implementation of the codec specified in the
emerging JPEG-2000 Part-1 standard (i.e., ISO/IEC 15444-1).  This package
contains tools for working with JPEG-2000 images.

%package -n	%{libname}
Summary:	Libraries for JasPer
Group:		System/Libraries

%description -n	%{libname}
This package contains a library for working with JPEG-2000 images.

%package -n	%{devname}
Summary:	Development tools for programs which will use the libjasper library
Group:		Development/C
Requires:	%{libname} >= %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
This package contains the development files for %{name}.

%prep
%setup -q
%apply_patches
mv doc/README doc/README.pdf

find -type d |xargs chmod 755
find -type f |xargs chmod 644

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
