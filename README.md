# Ladybug RPM packaging

This directory contains an RPM spec that mirrors the Debian split:
- `ladybug-cli`: CLI binary (`lbug`)
- `liblbug-devel`: shared runtime library
- `liblbug-static`: headers and static library

## Build locally

1. Download source tarball:
   - `https://github.com/LadybugDB/ladybug/archive/refs/tags/v0.15.3.tar.gz`
2. Place tarball in your RPM `SOURCES` directory with name:
   - `ladybug-cli-0.15.3.tar.gz`
3. Copy `ladybug.spec` to your RPM `SPECS` directory.
4. Build:
   - `rpmbuild -ba ladybug.spec`

## Notes

- The spec explicitly disables optional language bindings and tests.
- Upstream currently installs `liblbug.*` under `/usr/lib`; the `%install`
  section relocates files to `%{_libdir}` when required by distro policy.
