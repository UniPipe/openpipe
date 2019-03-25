#!/bin/sh
set -eu

cd openpipe

pluginList=$(find plugins/ -name "*.py" | grep -v "__init__" | sort)

for pluginFile in $pluginList
do
	testFile=$(echo "$pluginFile" | sed "s/(_)+.py/_test.yaml/g")
	if [ ! -r $testFile ]; then
		echo openpipe/$testFile is missing !!!
		exit 1
	fi
done