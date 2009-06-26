%define major 1
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d
%define staticname %mklibname %{name} -d -s

Summary:	JPEG-2000 utilities
Name:		jasper
Version:	1.900.1
Release:	%mkrel 6
License:	BSD-like
Group:		Graphics
URL:		http://www.ece.uvic.ca/~mdadams/jasper/
Source0: 	http://www.ece.uvic.ca/~mdadams/jasper/software/jasper-%version.zip
# P0 comes from jasper_1.900.1-3ubuntu0.7.10.1.diff
Patch0:		jasper-1.900.1-security_fixes.diff
BuildRequires:	libjpeg-devel
BuildRequires:	libmesaglut-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
%patch0 -p1

%{__mv} doc/README doc/README.pdf

%build
%configure2_5x --enable-shared

%make

%install
%{__rm} -rf %{buildroot}

%makeinstall_std
%multiarch_includes %{buildroot}%{_includedir}/jasper/jas_config.h

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README LICENSE NEWS
%{_bindir}/imgcmp
%{_bindir}/imginfo
%{_bindir}/jasper
%{_bindir}/jiv
%{_bindir}/tmrdemo
%{_mandir}/man1/imgcmp.1*
%{_mandir}/man1/imginfo.1*
%{_mandir}/man1/jasper.1*
%{_mandir}/man1/jiv.1*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%doc doc/README.pdf doc/jasper.pdf doc/jpeg2000.pdf 
%multiarch %dir %{multiarch_includedir}/%{name}
%multiarch %{multiarch_includedir}/%{name}/*.h
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_libdir}/*.la
%{_libdir}/*.so

%files -n %{staticname}
%defattr(-,root,root)
%{_libdir}/*.a
