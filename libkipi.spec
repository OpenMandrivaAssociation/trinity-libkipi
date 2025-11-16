#
# Please submit bugfixes or comments via http://www.trinitydesktop.org/
#

# BUILD WARNING:
#  Remove qt-devel and qt3-devel and any kde*-devel on your system !
#  Having KDE libraries may cause FTBFS here !

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define tde_pkg libkipi
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%if 0%{?mdkversion} || 0%{?mgaversion} || 0%{?pclinuxos}
%define libkipi %{_lib}kipi
%else
%define libkipi libkipi
%endif

%if 0%{?mdkversion}
%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1
%endif

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity
%global toolchain %(readlink /usr/bin/cc)


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	0.1.5
Release:	%{?tde_version}_%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}
Summary:	Library for apps that want to use kipi-plugins (runtime version) [Trinity]
Group:		System/Libraries
URL:		http://www.trinitydesktop.org/

%if 0%{?suse_version}
License:	GPL-2.0+
%else
License:	GPLv2+
%endif

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:			%{tde_prefix}

Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/libraries/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildRequires: cmake make
BuildRequires: trinity-tdelibs-devel >= %{tde_version}

BuildRequires: desktop-file-utils
BuildRequires: pkgconfig
BuildRequires: gettext
%if "%{?toolchain}" != "clang"
BuildRequires: gcc-c++
%endif

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
%{tde_libdir}/libkipi.so.0
%{tde_libdir}/libkipi.so.0.1.1
%{tde_datadir}/apps/kipi/
%{tde_datadir}/icons/hicolor/*/apps/kipi.png
%{tde_datadir}/servicetypes/kipiplugin.desktop

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
%{tde_libdir}/libkipi.so
%{tde_libdir}/libkipi.la
%{tde_tdeincludedir}/libkipi/
%{tde_libdir}/pkgconfig/libkipi.pc

##########

%if 0%{?suse_version} && 0%{?opensuse_bs} == 0
%debug_package
%endif

##########

%prep
%autosetup -n %{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"

if ! rpm -E %%cmake|grep -e 'cd build\|cd ${CMAKE_BUILD_DIR:-build}'; then
  %__mkdir_p build
  cd build
fi

%cmake \
  -DCMAKE_BUILD_TYPE="RelWithDebInfo" \
  -DCMAKE_C_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_CXX_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_SKIP_RPATH=OFF \
  -DCMAKE_SKIP_INSTALL_RPATH=OFF \
  -DCMAKE_VERBOSE_MAKEFILE=ON \
  -DWITH_GCC_VISIBILITY=OFF \
  \
  -DCMAKE_INSTALL_PREFIX="%{tde_prefix}" \
  -DINCLUDE_INSTALL_DIR="%{tde_tdeincludedir}" \
  -DLIB_INSTALL_DIR="%{tde_libdir}" \
  -DDATA_INSTALL_DIR="%{tde_datadir}/apps" \
  -DSHARE_INSTALL_PREFIX="%{tde_datadir}" \
  -DSERVICETYPES_INSTALL_DIR="%{tde_datadir}/servicetypes" \
  -DICON_INSTALL_DIR="%{tde_datadir}/icons" \
  \
  -DWITH_ALL_OPTIONS=ON \
  -DWITH_GCC_VISIBILITY=ON \
  \
  -DBUILD_ALL=ON \
  -DBUILD_DOC=ON \
  -DBUILD_TRANSLATIONS=ON \
  \
  ..


%install
export PATH="%{tde_bindir}:${PATH}"
%__make install DESTDIR=%{buildroot} -C build

%find_lang %{tde_pkg}

