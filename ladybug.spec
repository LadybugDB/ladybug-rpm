Name:           ladybug-cli
Version:        0.15.1
Release:        1%{?dist}
Summary:        Embedded graph database command-line client

License:        MIT
URL:            https://ladybugdb.com/
Source0:        https://github.com/LadybugDB/ladybug/archive/refs/tags/v%{version}.tar.gz#/ladybug-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++

%description
Ladybug is an embedded graph database optimized for query speed and
scalability.

This package provides the lbug interactive shell command-line tool.

%package -n liblbug
Summary:        Shared runtime library for Ladybug

%description -n liblbug
Shared runtime library for Ladybug.

%package -n liblbug-devel
Summary:        Development files for Ladybug
Requires:       liblbug%{?_isa} = %{version}-%{release}

%description -n liblbug-devel
Header files and static library for building applications against Ladybug.

%prep
%autosetup -n ladybug-%{version}

%build
%cmake \
  -DBUILD_LBUG=ON \
  -DBUILD_SHELL=ON \
  -DBUILD_TESTS=OFF \
  -DBUILD_EXTENSION_TESTS=OFF \
  -DBUILD_SINGLE_FILE_HEADER=OFF \
  -DBUILD_BENCHMARK=OFF \
  -DBUILD_WAL_DUMP=OFF \
  -DBUILD_JAVA=OFF \
  -DBUILD_NODEJS=OFF \
  -DBUILD_PYTHON=OFF \
  -DCMAKE_INSTALL_LIBDIR=%{_libdir}
%cmake_build

%install
%cmake_install

# Upstream installs libraries to %{_prefix}/lib by default. Move to %{_libdir}
# for RPM policy compliance when needed.
if [ -e "%{buildroot}%{_prefix}/lib/liblbug.so" ] || [ -e "%{buildroot}%{_prefix}/lib/liblbug.a" ]; then
  mkdir -p "%{buildroot}%{_libdir}"
  [ -e "%{buildroot}%{_prefix}/lib/liblbug.so" ] && mv "%{buildroot}%{_prefix}/lib/liblbug.so" "%{buildroot}%{_libdir}/"
  [ -e "%{buildroot}%{_prefix}/lib/liblbug.a" ] && mv "%{buildroot}%{_prefix}/lib/liblbug.a" "%{buildroot}%{_libdir}/"
fi

%check
%{buildroot}%{_bindir}/lbug --version >/dev/null || :

%files
%license LICENSE
%doc README.md
%{_bindir}/lbug

%files -n liblbug
%{_libdir}/liblbug.so

%files -n liblbug-devel
%{_includedir}/lbug.h
%{_libdir}/liblbug.a

%changelog
* Mon Mar 09 2026 Arun <arun@ladybugdb.com> - 0.15.1-1
- Initial RPM packaging
- Split into CLI, runtime library, and development packages
