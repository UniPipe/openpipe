#!/bin/sh
set -eu

rm -f archives/*
array=(gzip:.gz bzip2:.bz2 xz:.xz)

for item in ${array[*]}; do
    cmd=$(echo $item|cut -d":" -f1)
    ext=$(echo $item|cut -d":" -f2)
    for file in test.*; do
        $cmd -c $file > archives/$file$ext
    done
    tar -cf - test.* | $cmd -c > archives/test.tar$ext
done