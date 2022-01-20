#!/bin/bash

source /pkgscripts-ng/include/pkg_util.sh

package="MyApplication"
version="1.0-0001"
os_min_ver="7.0-40000"
install_dep_packages="WebStation>=3.0.0-0323:PHP7.4>=7.4.18-0114:Apache2.4>=2.4.46-0122"
maintainer="MyCompany"
maintainer_url="http://app.mycompany.com"
distributor="MyCompany"
distributor_url="http://app.mycompany.com"
silent_upgrade="no"
arch="noarch"
dsmappname="com.mycompany.app"
displayname="Web example package"
displayname_enu="Web example package"
displayname_cht="Web 範例套件"
description="This my sample package"
description_enu="This my sample package"
description_cht="這是我的範例套件"

[ "$(caller)" != "0 NULL" ] && return 0

pkg_dump_info
