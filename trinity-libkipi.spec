%bcond clang 1

# TDE variables
%define tde_pkg libkipi

%define tde_prefix /opt/trinity

%define libname %mklibname kipi
%define devname %mklibname kipi -d

%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%undefine _debugsource_template

%define tarball_name %{tde_pkg}-trinity


Name:		trinity-%{tde_pkg}
Version:	14.1.6
Release:	1
Summary:	Library for apps that want to use kipi-plugins (runtime version) [Trinity]
Group:		System/Libraries
URL:		http://www.trinitydesktop.org/

License:	GPLv2+


Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{version}/main/libraries/%{tarball_name}-%{version}.tar.xz

BuildSystem:    cmake

BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:    -DCMAKE_INSTALL_PREFIX=%{tde_prefix}
BuildOption:    -DINCLUDE_INSTALL_DIR=%{tde_prefix}/include/tde
BuildOption:    -DSHARE_INSTALL_PREFIX=%{tde_prefix}/share
BuildOption:    -DSERVICETYPES_INSTALL_DIR=%{tde_prefix}/share/servicetypes
BuildOption:    -DICON_INSTALL_DIR=%{tde_prefix}/share/icons
BuildOption:    -DWITH_ALL_OPTIONS=ON -DBUILD_ALL=ON -DBUILD_DOC=ON
BuildOption:    -DBUILD_TRANSLATIONS=ON
BuildOption:    -DWITH_GCC_VISIBILITY=%{!?with_clang:ON}%{?with_clang:OFF}

BuildRequires: trinity-tdelibs-devel >= %{version}
BuildRequires: pkgconfig(tqt)
BuildRequires:	trinity-tde-cmake >= %{version}

BuildRequires: desktop-file-utils
BuildRequires: pkgconfig
BuildRequires: gettext

%{!?with_clang:BuildRequires: gcc-c++}

# LCMS support
BuildRequires:  pkgconfig(lcms)

# JPEG support
BuildRequires:  pkgconfig(libjpeg)

# ACL support
BuildRequires:  pkgconfig(libacl)

# IDN support
BuildRequires:	pkgconfig(libidn)

# OPENSSL support
BuildRequires:  pkgconfig(openssl)

BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(sm)


%description
Libkipi is a library
- that contains common routines and widget used by kipi-plugins
- to ease implementation of the kipi-plugins interface in an application
  that wants to use kipi-plugins
    
Homepage: http://www.kipi-plugins.org/

##########

%package -n trinity-%{libname}0
Summary:	library for apps that want to use kipi-plugins (runtime version) [Trinity]
Group:		System/Libraries

%description -n trinity-%{libname}0
Libkipi is a library
  o that contains common routines and widget used by kipi-plugins
  o to ease implementation of the kipi-plugins interface in an application
    that wants to use kipi-plugins
    
Homepage: http://www.kipi-plugins.org/

%files -n trinity-%{libname}0 -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%{tde_prefix}/%{_lib}/libkipi.so.0
%{tde_prefix}/%{_lib}/libkipi.so.0.1.1
%{tde_prefix}/share/apps/kipi/
%{tde_prefix}/share/icons/hicolor/*/apps/kipi.png
%{tde_prefix}/share/servicetypes/kipiplugin.desktop

##########

%package -n trinity-%{devname}
Group:		Development/Libraries/Other
Summary:	library for apps that want to use kipi-plugins (development version) [Trinity]
Requires:	trinity-%{libname}0 = %{EVRD}

%description -n trinity-%{devname}
Libkipi is a library
  o that contains common routines and widget used by kipi-plugins
  o to ease implementation of the kipi-plugins interface in an application
    that wants to use kipi-plugins
    
This package contains development files and documentation for libkipi library.
Homepage: http://www.kipi-plugins.org/

%files -n trinity-%{devname}
%defattr(-,root,root,-)
%{tde_prefix}/%{_lib}/libkipi.so
%{tde_prefix}/%{_lib}/libkipi.la
%{tde_prefix}/include/tde/libkipi/
%{tde_prefix}/%{_lib}/pkgconfig/libkipi.pc


%conf -p 
unset QTDIR QTINC QTLIB
export PATH="%{tde_prefix}/bin:${PATH}"


%install -a
%find_lang %{tde_pkg}

