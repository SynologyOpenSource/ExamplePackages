#!/bin/bash

PKG_UTILS="/source/synopkgutils/pkg_util.sh"

. $PKG_UTILS
. ./uifile_setting.sh

pkg_dump_wizard_content()
{
    local out=$1
    cat > "$out" <<EOF
[{
	"custom_render_fn": $(cat $INSTALL_ENTRY_JS | jq -R),
	"custom_render_name": "install_setting"
}]
EOF
}

pkg_dump_inst_wizard()
{
	if [ ! -d "$PKG_WIZARD_DIR" ]; then
		mkdir $PKG_WIZARD_DIR
	fi

	pkg_dump_wizard_content $PKG_WIZARD_DIR/install_uifile
}

PKG_WIZARD_DIR="."
pkg_dump_inst_wizard
