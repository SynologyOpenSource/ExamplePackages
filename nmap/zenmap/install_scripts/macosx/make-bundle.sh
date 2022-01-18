#!/bin/sh -e
set -x

test "x$UNDER_JHBUILD" = "x" && exit 1

# make-bundle.sh
APP_NAME=Zenmap
ZENMAP_DIST_DIR=$PWD/dist
ZENMAP_BUILD_DIR=$PWD/build

export ZENMAP_DIST_DIR
export ZENMAP_BUILD_DIR

BASE=$ZENMAP_DIST_DIR/$APP_NAME.app/Contents
SCRIPT_DIR=`dirname "$0"`

CC=${CC:-clang}
CFLAGS=${CFLAGS:--Wall -arch i386}

echo "Running $0."

echo "Removing old build."
rm -rf "$ZENMAP_DIST_DIR" "$ZENMAP_BUILD_DIR"

echo "Building bundle"
gtk-mac-bundler "$SCRIPT_DIR/zenmap.bundle"

echo "Stripping unoptimized Python libraries"
#Remove some stuff that is unneeded. This cuts 40M off the installed size.
rm -rf $BASE/Resources/lib/python2.7/test/
rm -rf $BASE/Resources/lib/python2.7/config/
rm -rf $BASE/Resources/lib/python2.7/idlelib/
rm -rf $BASE/Resources/lib/python2.7/lib-tk/
rm -rf $BASE/Resources/lib/python2.7/lib2to3/
rm -f  $BASE/Resources/lib/python2.7/site-packages/*.a
find "$BASE/Resources/lib/python2.7" -type f -name '*.py' | while read py; do
# If the .pyc exists, delete the .py
  test -f "${py}c" && rm -v "$py"
done
find "$BASE/Resources/lib/python2.7" -type f -name '*.pyo' | while read py; do
  # If the .pyc exists, delete the .pyo
  test -f "${py/%o/c}" && rm -v "$py"
done

echo "Building using distutils"
python setup.py build --executable "/usr/bin/env python"
python setup.py install vanilla --prefix "$BASE/Resources"

echo "Renaming main Zenmap executable."
mv $BASE/MacOS/$APP_NAME $BASE/MacOS/zenmap.bin
# This is a dummy script, so we'll clean it up:
rm $BASE/MacOS/$APP_NAME-bin

echo "Compiling and installing authorization wrapper."
echo $CC $CPPFLAGS $CFLAGS $LDFLAGS -v "$SCRIPT_DIR/zenmap_auth.m" -lobjc -framework Foundation -o "$BASE/MacOS/$APP_NAME"
$CC $CPPFLAGS $CFLAGS $LDFLAGS -v "$SCRIPT_DIR/zenmap_auth.m" -lobjc -framework Foundation -o "$BASE/MacOS/$APP_NAME"

echo "Filling out Info.plist"
python - "$SCRIPT_DIR/Info.plist" >"$BASE/Info.plist" <<'EOF'
import sys
from string import Template
from zenmapCore.Version import *
from zenmapCore.Name import *
with open(sys.argv[1],"r") as f:
  sys.stdout.write(Template(f.read()).substitute(
    VERSION=VERSION,
    APP_WEB_SITE=APP_WEB_SITE,
    APP_COPYRIGHT=APP_COPYRIGHT
    ))
EOF
