#!/bin/bash

PKG_UTILS="/pkgscripts/include/pkg_util.sh"

. $PKG_UTILS
. ./uifile_setting.sh

pkg_dump_wizard_content()
{
    local out=$1
    cat > "$out" <<EOF
[{
	"custom_render_fn": $(cat $REMOVE_ENTRY_JS | jq -R),
	"custom_render_name": "remove_setting"
}, {
	"custom_render_fn": $(cat $REMOVE_NOTICE_ENTRY_JS | jq -R),
	"custom_render_name": "remove_notice"
}]
EOF
}

pkg_dump_uninst_wizard()
{
	if [ ! -d "$PKG_WIZARD_DIR" ]; then
		mkdir $PKG_WIZARD_DIR
	fi

	pkg_dump_wizard_content $PKG_WIZARD_DIR/uninstall_uifile
}

PKG_WIZARD_DIR="."
pkg_dump_uninst_wizard
