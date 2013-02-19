%define	major	1
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname %{name} -d

%bcond_without	bootstrap

Summary:	JPEG-2000 utilities
Name:		jasper
Version:	1.900.1
Release:	16
License:	BSD-like
Group:		Graphics
Url:		http://www.ece.uvic.ca/~frodo/jasper/
Source0:	http://www.ece.uvic.ca/~frodo/jasper/software/jasper-%{version}.zip
Patch1:		jasper-1.701.0-GL.patch
# autoconf/automake bits of patch1
Patch2:		jasper-1.701.0-GL-ac.patch
# CVE-2007-2721 (bug #240397)
# borrowed from http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=413041;msg=88
Patch3:		patch-libjasper-stepsizes-overflow.diff
# borrowed from http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=469786 
Patch4:		jpc_dec.c.patch
# OpenBSD hardening patches addressing couple of possible integer overflows
# during the memory allocations
# https://bugzilla.redhat.com/show_bug.cgi?id=CVE-2008-3520
Patch5:		jasper-1.900.1-CVE-2008-3520.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=CVE-2008-3522
Patch6:		jasper-1.900.1-CVE-2008-3522.patch
# add pkg-config support
Patch7:		jasper-pkgconfig.patch

Patch8:		jasper-1.900.1-CVE-2011-4516-CVE-2011-4517-CERT-VU-887409.patch

# Issues found by static analysis of code
Patch10:	jasper-1.900.1-Coverity-BAD_SIZEOF.patch
Patch11:	jasper-1.900.1-Coverity-CHECKED_RETURN.patch
Patch12:	jasper-1.900.1-Coverity-FORWARD_NULL.patch
Patch13:	jasper-1.900.1-Coverity-NULL_RETURNS.patch
Patch14:	jasper-1.900.1-Coverity-RESOURCE_LEAK.patch
Patch15:	jasper-1.900.1-Coverity-UNREACHABLE.patch
Patch16:	jasper-1.900.1-Coverity-UNUSED_VALUE.patch

BuildRequires:	jpeg-devel
%if !%{with bootstrap}
BuildRequires:	pkgconfig(glut)
%endif

%description
JasPer is a software-based implementation of the codec specified in the
emerging JPEG-2000 Part-1 standard (i.e., ISO/IEC 15444-1).  This package
contains tools for working with JPEG-2000 images.

%package -n	%{libname}
Summary:	Libraries for JasPer
Group:		System/Libraries

%description -n	%{libname}
JasPer is a software-based implementation of the codec specified in the
emerging JPEG-2000 Part-1 standard (i.e., ISO/IEC 15444-1).  This package
contains libraries for working with JPEG-2000 images.

%package -n	%{devname}
Summary:	Development tools for programs which will use the libjasper library
Group:		Development/C
Requires:	%{libname} >= %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Conflicts:	lib64jasper1.701_1-devel
Obsoletes:	%{mklibname %{name} 1 -d} < 1.900.1-5

%description -n	%{devname}
The %{libname}-devel package includes the header files necessary for 
developing programs which will manipulate JPEG-2000 files using
the libjasper library.

If you are going to develop programs which will manipulate JPEG-2000 images,
you should install %{libname}-devel.  You'll also need to have the
%{libname} package installed.

%prep
%setup -q
%apply_patches

mv doc/README doc/README.pdf

find -type d |xargs chmod 755

autoreconf -fi

%build
%configure2_5x \
	--enable-shared \
	--disable-static
%make

%install
%makeinstall_std

%multiarch_includes %{buildroot}%{_includedir}/jasper/jas_config.h

%files
%doc README LICENSE NEWS
%{_bindir}/imgcmp
%{_bindir}/imginfo
%{_bindir}/jasper
%if !%{with bootstrap}
%{_bindir}/jiv
%endif
%{_bindir}/tmrdemo
%{_mandir}/man1/imgcmp.1*
%{_mandir}/man1/imginfo.1*
%{_mandir}/man1/jasper.1*
%{_mandir}/man1/jiv.1*

%files -n %{libname}
%{_libdir}/libjasper.so.%{major}*

%files -n %{devname}
%doc doc/README.pdf doc/jasper.pdf doc/jpeg2000.pdf
%dir %{_includedir}/%{name}
%dir %{multiarch_includedir}/%{name}
%{multiarch_includedir}/%{name}/*.h
%{_includedir}/%{name}/*
%{_libdir}/libjasper.so
%{_libdir}/pkgconfig/jasper.pc
