Name:           ladybug-cli
Version:        0.15.3
Release:        1%{?dist}
Summary:        Embedded graph database command-line client

License:        MIT
URL:            https://ladybugdb.com/
Source0:        https://github.com/LadybugDB/ladybug/archive/refs/tags/v%{version}.tar.gz#/ladybug-%{version}.tar.gz
Patch0:         ladybug-%{version}-fix-fixed-width-integers.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++

# upstream builds the default CLI/library RPM targets against
# bundled copies from third_party/ and does not currently expose switches to use
# system copies for these dependencies. This list includes deps used by the
# default CLI/library build and by optional extensions shipped by upstream, but
# omits benchmark, test, and language-binding-only bundled deps.
Provides:       bundled(alp)
Provides:       bundled(antlr4_cypher) = 4.13.1
Provides:       bundled(antlr4_runtime) = 4.13.1
Provides:       bundled(brotli) = 1.1.0
Provides:       bundled(cppjieba) = 5.6.0
Provides:       bundled(fast_float)
Provides:       bundled(fastpfor) = 0.1.8
Provides:       bundled(glob)
Provides:       bundled(httplib) = 0.14.2
Provides:       bundled(lz4) = 1.10.0
Provides:       bundled(mbedtls) = 3.1.0
Provides:       bundled(miniz) = 10.0.3
Provides:       bundled(parquet) = 0.11.0
Provides:       bundled(pcg)
Provides:       bundled(pyparse)
Provides:       bundled(re2)
Provides:       bundled(roaring_bitmap) = 4.5.1
Provides:       bundled(simsimd) = 6.2.1
Provides:       bundled(snappy) = 1.2.1
Provides:       bundled(taywee_args) = 6.4.2
Provides:       bundled(thrift)
Provides:       bundled(utf8proc) = 2.4.0
Provides:       bundled(yyjson) = 0.10.0
Provides:       bundled(zstd) = 1.5.7

%description
Ladybug is an embedded graph database optimized for query speed and
scalability.

This package provides the lbug interactive shell command-line tool.

%package -n liblbug-devel
Summary:        Shared runtime library for Ladybug

%description -n liblbug-devel
Shared runtime library for Ladybug.

%package -n liblbug-static
Summary:        Development files for Ladybug
Requires:       liblbug%{?_isa} = %{version}-%{release}

%description -n liblbug-static
Header files and static library for building applications against Ladybug.

%prep
%autosetup -p1 -n ladybug-%{version}

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
  -DCMAKE_CXX_FLAGS="-DHAVE_INTTYPES_H=1" \
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

# Remove cppjieba headers and dictionary data — not part of the public API.
rm -rf %{buildroot}%{_includedir}/cppjieba
rm -rf %{buildroot}%{_datadir}/cppjieba

# Strip executable bits from installed debug sources that have no shebang
# (third-party C/C++ source files installed under /usr/src/debug).
# The directory may not exist when debuginfo generation is disabled.
if [ -d "%{buildroot}/usr/src/debug" ]; then
  find %{buildroot}/usr/src/debug -type f \( -name "*.cpp" -o -name "*.h" -o -name "*.c" \) \
    -perm /0111 -exec chmod a-x {} +
fi

%check
%{buildroot}%{_bindir}/lbug --version >/dev/null || :

%files
%license LICENSE
%doc README.md
%{_bindir}/lbug

%files -n liblbug-devel
%{_libdir}/liblbug.so
%{_libdir}/liblbug.so.0
%{_libdir}/liblbug.so.0.15.3

%files -n liblbug-static
%{_includedir}/lbug.h
%{_libdir}/liblbug.a

%changelog
* Mon Apr 27 2026 Ally Heev <allyheev@gmail.com> - 0.15.3-2
- Move shared runtime library to liblbug-devel subpackage
- Move headers and static library liblbug-static subpackage
- Mention third_party libs in the spec

* Fri Apr 03 2026 Arun <arun@ladybugdb.com> - 0.15.3-1
- Update to upstream version 0.15.3

* Mon Mar 09 2026 Arun <arun@ladybugdb.com> - 0.15.1-1
- Initial RPM packaging
- Split into CLI, runtime library, and development packages
