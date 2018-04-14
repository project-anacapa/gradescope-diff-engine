#!/usr/bin/env sh

# @test{"stdout":20,"name":"You should echo foo on stdout"}
python3 hello.py 

# @test{"stderr":10", "name":"check stderr"}
python3 hello.py

# @test{"filename":"myfile.out", "points":10, "name":"Check contents of myfile.out"}
python3 hello.py






