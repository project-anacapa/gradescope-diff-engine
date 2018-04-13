#!/usr/bin/env sh

echo "foo"       # 10,You should echo foo to stdout

>&2 echo "error" # , , 10, You should echo bar to stderr


