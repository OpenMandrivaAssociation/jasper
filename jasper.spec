%define major 1
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d
%define staticname %mklibname %{name} -d -s

%define bootstrap 0
%{?_without_bootstrap: %global bootstrap 0}
%{?_with_bootstrap: %global bootstrap 1}

Summary:	JPEG-2000 utilities
Name:		jasper
Version:	1.900.1
Release:	15
License:	BSD-like
Group:		Graphics
URL:		http://www.ece.uvic.ca/~mdadams/jasper/
Source0: 	http://www.ece.uvic.ca/~mdadams/jasper/software/jasper-%version.zip
Patch1: jasper-1.701.0-GL.patch
# autoconf/automake bits of patch1
Patch2: jasper-1.701.0-GL-ac.patch
# CVE-2007-2721 (bug #240397)
# borrowed from http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=413041;msg=88
Patch3: patch-libjasper-stepsizes-overflow.diff
# borrowed from http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=469786 
Patch4: jpc_dec.c.patch
# OpenBSD hardening patches addressing couple of possible integer overflows
# during the memory allocations
# https://bugzilla.redhat.com/show_bug.cgi?id=CVE-2008-3520
Patch5: jasper-1.900.1-CVE-2008-3520.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=CVE-2008-3522
Patch6: jasper-1.900.1-CVE-2008-3522.patch
# add pkg-config support
Patch7: jasper-pkgconfig.patch

Patch8: jasper-1.900.1-CVE-2011-4516-CVE-2011-4517-CERT-VU-887409.patch

# Issues found by static analysis of code
Patch10: jasper-1.900.1-Coverity-BAD_SIZEOF.patch
Patch11: jasper-1.900.1-Coverity-CHECKED_RETURN.patch
Patch12: jasper-1.900.1-Coverity-FORWARD_NULL.patch
Patch13: jasper-1.900.1-Coverity-NULL_RETURNS.patch
Patch14: jasper-1.900.1-Coverity-RESOURCE_LEAK.patch
Patch15: jasper-1.900.1-Coverity-UNREACHABLE.patch
Patch16: jasper-1.900.1-Coverity-UNUSED_VALUE.patch
BuildRequires:	jpeg-devel
BuildRequires:	autoconf automake libtool
%if !%bootstrap
BuildRequires:	pkgconfig(glut)
%endif

%description
JasPer is a software-based implementation of the codec specified in the
emerging JPEG-2000 Part-1 standard (i.e., ISO/IEC 15444-1).  This package
contains tools for working with JPEG-2000 images.

%package -n %{libname}
Summary:	Libraries for JasPer
Group:		System/Libraries
Provides:	lib%{name} = %{version}-%{release}

%description -n %{libname}
JasPer is a software-based implementation of the codec specified in the
emerging JPEG-2000 Part-1 standard (i.e., ISO/IEC 15444-1).  This package
contains libraries for working with JPEG-2000 images.

%package -n %{develname}
Summary:	Development tools for programs which will use the libjasper library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Conflicts:	lib64jasper1.701_1-devel
Obsoletes:	%{mklibname %{name} 1 -d} < 1.900.1-5
Provides:	%{mklibname %{name} 1 -d}

%description -n %{develname}
The %{libname}-devel package includes the header files necessary for 
developing programs which will manipulate JPEG-2000 files using
the libjasper library.

If you are going to develop programs which will manipulate JPEG-2000 images,
you should install %{libname}-devel.  You'll also need to have the
%{libname} package installed.

%package -n %{staticname}
Summary:	Static libraries for programs which will use the libjasper library
Group:		Development/C
Requires:	%{develname} = %{version}-%{release}
Provides:	lib%{name}-static-devel = %{version}-%{release}
Provides:	%{name}-static-devel = %{version}-%{release}
Provides:	%{libname}-static-devel = %{version}-%{release}
Conflicts:	lib64jasper1.701_1-static-devel
Obsoletes:	%{mklibname %{name} 1 -d -s} < 1.900.1-5
Provides:	%{mklibname %{name} 1 -d -s}

%description -n %{staticname}
The %{libname}-static-devel package includes the static 
libraries necessary for developing programs which will manipulate JPEG-2000 
files using the libjasper library.

%prep
%setup -q
%patch1 -p1 -b .GL
%patch2 -p1 -b .GL-ac
%patch3 -p1 -b .CVE-2007-2721
%patch4 -p1 -b .jpc_dec_assertion
%patch5 -p1 -b .CVE-2008-3520
%patch6 -p1 -b .CVE-2008-3522
%patch7 -p1 -b .pkgconfig
%patch8 -p1 -b .CVE-2011-4516-4517

%patch10 -p1 -b .BAD_SIZEOF
%patch11 -p1 -b .CHECKED_RETURN
%patch12 -p1 -b .FORWARD_NULL
%patch13 -p1 -b .NULL_RETURNS
%patch14 -p1 -b .RESOURCE_LEAK
%patch15 -p1 -b .UNREACHABLE
%patch16 -p1 -b .UNUSED_VALUE

%__mv doc/README doc/README.pdf

%build
autoreconf -fi

%configure2_5x --enable-shared

%make

%install
%makeinstall_std

%multiarch_includes %{buildroot}%{_includedir}/jasper/jas_config.h

%files
%doc README LICENSE NEWS
%{_bindir}/imgcmp
%{_bindir}/imginfo
%{_bindir}/jasper
%if !%bootstrap
%{_bindir}/jiv
%endif
%{_bindir}/tmrdemo
%{_mandir}/man1/imgcmp.1*
%{_mandir}/man1/imginfo.1*
%{_mandir}/man1/jasper.1*
%{_mandir}/man1/jiv.1*

%files -n %{libname}
%{_libdir}/lib*.so.%{major}*

%files -n %{develname}
%doc doc/README.pdf doc/jasper.pdf doc/jpeg2000.pdf 
%dir %{_includedir}/%{name}
%dir %{multiarch_includedir}/%{name}
%{multiarch_includedir}/%{name}/*.h
%{_includedir}/%{name}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/jasper.pc

%files -n %{staticname}
%{_libdir}/*.a

