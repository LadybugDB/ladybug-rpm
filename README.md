# Ladybug RPM packaging

This directory contains an RPM spec that mirrors the Debian split:
- `ladybug-cli`: CLI binary (`lbug`)
- `liblbug-devel`: shared runtime library
- `liblbug-static`: headers and static library

## Build locally

1. Copy `ladybug-cli.spec` to your RPM `SPECS` directory.
2. Download sources: `spectool -g -R ladybug-cli.spec`
3. Build: `rpmbuild -ba ladybug-cli.spec`

Note: You may also use [Mock](https://rpm-packaging-guide.github.io/#mock) to build in a clean chroot environment.

## Notes

- The spec explicitly disables optional language bindings and tests.
- Upstream currently installs `liblbug.*` under `/usr/lib`; the `%install`
  section relocates files to `%{_libdir}` when required by distro policy.
