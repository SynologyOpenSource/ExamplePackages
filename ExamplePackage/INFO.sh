#!/bin/bash
# Copyright (c) 2000-2020 Synology Inc. All rights reserved.

source /pkgscripts/include/pkg_util.sh

package="ExamplePackage"
version="1.0.0-0001"
displayname="Example Package"
os_min_ver="7.0-40000"
maintainer="Synology Inc."
arch="$(pkg_get_platform)"
description="this is an example package"
dsmuidir="ui"
[ "$(caller)" != "0 NULL" ] && return 0
pkg_dump_info
