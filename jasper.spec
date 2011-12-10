%define major 1
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

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
Source0: 	http://www.ece.uvic.ca/~mdadams/jasper/software/jasper-%{version}.zip
# P0 comes from jasper_1.900.1-3ubuntu0.7.10.1.diff
Patch0:		jasper-1.900.1-security_fixes.diff
BuildRequires:	jpeg-devel
%if !%bootstrap
BuildRequires:	mesaglut-devel
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

%package -n	%{develname}
Summary:	Development tools for programs which will use the libjasper library
Group:		Development/C
Requires:	%{libname} >= %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Conflicts:	lib64jasper1.701_1-devel
Obsoletes:	%{mklibname %{name} 1 -d} < 1.900.1-5
Provides:	%{mklibname %{name} 1 -d} = %{version}-%{release}

%description -n	%{develname}
The %{libname}-devel package includes the header files necessary for 
developing programs which will manipulate JPEG-2000 files using
the libjasper library.

If you are going to develop programs which will manipulate JPEG-2000 images,
you should install %{libname}-devel.  You'll also need to have the
%{libname} package installed.

%prep
%setup -q
%patch0 -p1

%{__mv} doc/README doc/README.pdf

%build
%configure2_5x \
    --enable-shared \
    --disable-static
%make

%install
%{__rm} -rf %{buildroot}
%makeinstall_std

%multiarch_includes %{buildroot}%{_includedir}/jasper/jas_config.h

# cleanup
rm -f %{buildroot}%{_libdir}/*.la

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
