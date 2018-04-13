#!/usr/bin/env sh

# @test{"stdout":20,"name":"You should echo foo on stdout"}
echo "foo"

# @test{"stderr":10, "name":"Run prog1"}
>&2 echo "bar" # , , 10, You should echo bar to stderr





