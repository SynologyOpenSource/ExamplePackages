#!/bin/sh
# Copyright (c) 2000-2021 Synology Inc. All rights reserved.

. /pkgscripts-ng/include/pkg_util.sh
package="nmap"
version="7.91-1001"
os_min_ver="7.0-40850"
displayname="nmap"
arch="$(pkg_get_platform) "
maintainer="Synology Inc."
description="This package will install nmap in your DSM system."
[ "$(caller)" != "0 NULL" ] && return 0
pkg_dump_info