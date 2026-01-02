%bcond clang 1

# BUILD WARNING:
#  Remove qt-devel and qt3-devel and any kde*-devel on your system !
#  Having KDE libraries may cause FTBFS here !

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define pkg_rel 4

%define tde_pkg libkipi

%define tde_prefix /opt/trinity

%define libkipi %{_lib}kipi

%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	0.1.5
Release:	%{?tde_version}_%{?!preversion:%{pkg_rel}}%{?preversion:0_%{preversion}}%{?dist}
Summary:	Library for apps that want to use kipi-plugins (runtime version) [Trinity]
Group:		System/Libraries
URL:		http://www.trinitydesktop.org/

License:	GPLv2+


Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/libraries/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildSystem:    cmake
BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:    -DCMAKE_SKIP_RPATH=OFF
BuildOption:    -DCMAKE_SKIP_INSTALL_RPATH=OFF
BuildOption:    -DCMAKE_BUILD_WITH_INSTALL_RPATH=ON
BuildOption:    -DCMAKE_INSTALL_PREFIX="%{tde_prefix}"
BuildOption:    -DINCLUDE_INSTALL_DIR="%{tde_prefix}/include/tde"
BuildOption:    -DLIB_INSTALL_DIR="%{tde_prefix}/%{_lib}"
BuildOption:    -DDATA_INSTALL_DIR="%{tde_prefix}/share/apps"
BuildOption:    -DSHARE_INSTALL_PREFIX="%{tde_prefix}/share"
BuildOption:    -DSERVICETYPES_INSTALL_DIR="%{tde_prefix}/share/servicetypes"
BuildOption:    -DICON_INSTALL_DIR="%{tde_prefix}/share/icons"
BuildOption:    -DWITH_ALL_OPTIONS=ON -DBUILD_ALL=ON -DBUILD_DOC=ON
BuildOption:    -DBUILD_TRANSLATIONS=ON
BuildOption:    -DWITH_GCC_VISIBILITY=%{!?with_clang:ON}%{?with_clang:OFF}

BuildRequires: trinity-tdelibs-devel >= %{tde_version}

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

# CMAKE
BuildRequires:	trinity-tde-cmake >= %{tde_version}

%description
Libkipi is a library
- that contains common routines and widget used by kipi-plugins
- to ease implementation of the kipi-plugins interface in an application
  that wants to use kipi-plugins
    
Homepage: http://www.kipi-plugins.org/

##########

%package -n trinity-%{libkipi}0
Summary:	library for apps that want to use kipi-plugins (runtime version) [Trinity]
Group:		System/Libraries

Obsoletes:	trinity-%{tde_pkg} < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	trinity-%{tde_pkg} = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n trinity-%{libkipi}0
Libkipi is a library
  o that contains common routines and widget used by kipi-plugins
  o to ease implementation of the kipi-plugins interface in an application
    that wants to use kipi-plugins
    
Homepage: http://www.kipi-plugins.org/

%files -n trinity-%{libkipi}0 -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%{tde_prefix}/%{_lib}/libkipi.so.0
%{tde_prefix}/%{_lib}/libkipi.so.0.1.1
%{tde_prefix}/share/apps/kipi/
%{tde_prefix}/share/icons/hicolor/*/apps/kipi.png
%{tde_prefix}/share/servicetypes/kipiplugin.desktop

##########

%package -n trinity-%{libkipi}-devel
Group:		Development/Libraries/Other
Summary:	library for apps that want to use kipi-plugins (development version) [Trinity]
Requires:	%{name} = %{?epoch:%{epoch}:}%{version}-%{release}

Obsoletes:	trinity-%{tde_pkg}-devel < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	trinity-%{tde_pkg}-devel = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n trinity-%{libkipi}-devel
Libkipi is a library
  o that contains common routines and widget used by kipi-plugins
  o to ease implementation of the kipi-plugins interface in an application
    that wants to use kipi-plugins
    
This package contains development files and documentation for libkipi library.
Homepage: http://www.kipi-plugins.org/

%files -n trinity-%{libkipi}-devel
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

