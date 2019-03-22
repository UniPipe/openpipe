#!/bin/sh
set -eu

test_files=$(ls -1 test.*)
compressors="gzip bzip2 xz"
for compressor in $compressors; do
    for file in $test_files; do
        output_file=$(echo archives/$file.$compressor | sed -e "s/bzip2/bz/" -e "s/gzip/gz/g")
        $compressor -c $file > $output_file
    done
    output_file=$(echo archives/test.tar.$compressor | sed -e "s/bzip2/bz/" -e "s/gzip/gz/g")
    tar -cvf - test.* | $compressor -c > $output_file
done


