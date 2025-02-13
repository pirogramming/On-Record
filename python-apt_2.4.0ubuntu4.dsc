-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA512

Format: 3.0 (native)
Source: python-apt
Binary: python-apt-doc, python-apt-dev, python-apt-common, python3-apt, python3-apt-dbg
Architecture: any all
Version: 2.4.0ubuntu4
Maintainer: Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com>
Uploaders: Michael Vogt <mvo@debian.org>, Julian Andres Klode <jak@debian.org>
Standards-Version: 4.5.0
Vcs-Browser: https://salsa.debian.org/apt-team/python-apt
Vcs-Git: https://salsa.debian.org/apt-team/python-apt.git
Testsuite: autopkgtest
Testsuite-Triggers: apt-utils, binutils, dirmngr, distro-info-data, fakeroot, gnupg, intltool, pycodestyle, pyflakes3, python3-all
Build-Depends: apt (>= 1.0.9.4), apt-utils <!nocheck>, debhelper-compat (= 12), dh-python, distro-info-data <!nocheck>, fakeroot, libapt-pkg-dev (>= 1.9.11~), python3-all (>= 3.3), python3-all-dev (>= 3.3), python3-all-dbg (>= 3.3), python3-distutils, python3-distutils-extra (>= 2.0), python3-setuptools, python3-sphinx (>= 0.5), gnupg <!nocheck>, dirmngr <!nocheck> | gnupg (<< 2) <!nocheck>, pycodestyle <!nocheck>, pyflakes3 <!nocheck>
Package-List:
 python-apt-common deb python optional arch=all
 python-apt-dev deb python optional arch=all
 python-apt-doc deb doc optional arch=all
 python3-apt deb python optional arch=any
 python3-apt-dbg deb debug optional arch=any
Checksums-Sha1:
 2be72e4d3b7b50759846f86933c00de6ebcf00b3 346012 python-apt_2.4.0ubuntu4.tar.xz
Checksums-Sha256:
 4ab9c915d1295afbf2ca197993454d3659bb8dee4e9cd39ceba9efe5970873cc 346012 python-apt_2.4.0ubuntu4.tar.xz
Files:
 4fff31608611d381b617a4d61536bae7 346012 python-apt_2.4.0ubuntu4.tar.xz
Original-Maintainer: APT Development Team <deity@lists.debian.org>

-----BEGIN PGP SIGNATURE-----

iQFGBAEBCgAwFiEEVhrVhe7XZpIbqN2W1lhhiD4BTbkFAmbV8lMSHHBhcmlkZUB1
YnVudHUuY29tAAoJENZYYYg+AU25vXMH/0NbIN8mc3VWDT6EDrMexZy6umm7j33o
8AvVb6QYFY1MezxJmhS19+YT0i20rVRYTq2LDMirWeCEtC9sGqZ8UarrITBFU55W
j1Q292jCCCRHQnkTla3bulT2TQByZRDsvXWbAAKDsLSzJY0usNIyXJfYDG7YoKDq
rR4wrk10iep/GnG6yxBwPVJe1zv7GKg5k5sopgWORULOXO/5YUXznoxhZE6JaSBC
8hw1fHUnUYF2W9e6Uy5+rownAF7RDAD054vCNymZiwstrSUgxweuam85ImUp8kCU
QXh/EsXMph4kh+8Go7R7gExnGgZsOv6rq504LEtPgyl04StGnorfsEc=
=ge9h
-----END PGP SIGNATURE-----
