#!/bin/sh
set -eu

cd openpipe

pluginList=$(find plugins/ -name "*.py" | grep -v "__init__" | sort)

for pluginFile in $pluginList
do
	testFile=$(echo "tests/$pluginFile" | sed "s/\.py/.yaml/g")
	if [ ! -r $testFile ]; then
		#mkdir -p $(dirname $testFile)
		echo openpipe/$testFile is missing !!!
		exit 1
	fi
done
