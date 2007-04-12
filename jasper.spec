%define	name		jasper	
%define	version		1.701.0 
%define	release		%mkrel 6

%define api_version	1.701
%define lib_major	1
%define lib_name	%mklibname %{name} %{api_version} %{lib_major}
%define lib_name_api	%mklibname %{name} %{api_version}
%define lib_name_major	%mklibname %{name} %{lib_major}

Summary:	JPEG-2000 utilities 
Name:		%name
Version:	%version
Release:	%release
License:	BSD-like
Group:		Graphics	
URL:		http://www.ece.uvic.ca/~mdadams/jasper/
Source0:	%name-%version.tar.bz2
BuildRoot:	%_tmppath/%name--buildroot
BuildRequires:	libjpeg-devel
BuildRequires:	libmesaglut-devel

%description
JasPer is a software-based implementation of the codec specified in the
emerging JPEG-2000 Part-1 standard (i.e., ISO/IEC 15444-1).  This package
contains tools for working with JPEG-2000 images.

%package -n %{lib_name}
Summary:	Libraries for JasPer.
Group:		System/Libraries
Provides:	lib%{name} = %{version}-%{release}
Provides:	%{lib_name_api} = %{version}-%{release}
Provides:	%{lib_name_major} = %{version}-%{release}

%description -n %{lib_name}
JasPer is a software-based implementation of the codec specified in the
emerging JPEG-2000 Part-1 standard (i.e., ISO/IEC 15444-1).  This package
contains libraries for working with JPEG-2000 images.

%package -n %{lib_name}-devel
Summary:	Development tools for programs which will use the libjasper library
Group:		Development/C
Requires:	%{lib_name} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	%{lib_name_api}-devel = %{version}-%{release}
Provides:	%{lib_name_major}-devel = %{version}-%{release}

%description -n %{lib_name}-devel
The %{lib_name}-devel package includes the header files necessary for 
developing programs which will manipulate JPEG-2000 files using
the libjasper library.

If you are going to develop programs which will manipulate JPEG-2000 images,
you should install %{lib_name}-devel.  You'll also need to have the
%{lib_name} package installed.

%package -n %{lib_name}-static-devel
Summary:	Static libraries for programs which will use the libjasper library
Group:		Development/C
Requires:	%{lib_name}-devel = %{version}-%{release}
Provides:	lib%{name}-static-devel = %{version}-%{release}
Provides:	%{name}-static-devel = %{version}-%{release}
Provides:	%{lib_name_api}-static-devel = %{version}-%{release}
Provides:	%{lib_name_major}-static-devel = %{version}-%{release}

%description -n %{lib_name}-static-devel
The %{lib_name}-static-devel package includes the static 
libraries necessary for developing programs which will manipulate JPEG-2000 
files using the libjasper library.


%prep

%setup -q

%{__mv} doc/README doc/README.pdf

# Don't want an RPATH for /usr/X11R6/lib
%{__perl} -pi -e 's#(sys_lib_dlsearch_path_spec=".*?)"#$1 /usr/X11R6/lib"#' configure 


%build

%configure --enable-shared

%make

%install
%{__rm} -rf %{buildroot}

%makeinstall
%multiarch_includes $RPM_BUILD_ROOT%{_includedir}/jasper/jas_config.h

%post -n %{lib_name} -p /sbin/ldconfig

%postun -n %{lib_name} -p /sbin/ldconfig

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README LICENSE
%{_bindir}/imginfo
%{_bindir}/imgcmp
%{_bindir}/jasper
%{_bindir}/jiv

%files -n %{lib_name}
%defattr(-,root,root)
%{_libdir}/lib*.so.*

%files -n %{lib_name}-devel
%defattr(-,root,root)
%doc doc/README.pdf doc/jasper.pdf doc/jpeg2000.pdf 
%multiarch %dir %{multiarch_includedir}/%{name}
%multiarch %{multiarch_includedir}/%{name}/*.h
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_libdir}/*.la
%{_libdir}/*.so

%files -n %{lib_name}-static-devel
%defattr(-,root,root)
%{_libdir}/*.a


