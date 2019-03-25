#!/bin/sh
set -eu

pluginList=$(find openpipe/plugins/ -name "*.py" | sort)

for pluginFile in $pluginList
do
	testFile=$(echo "$pluginFile" | sed "s/_.py/_test.yaml/g")
	if [ ! -r $testFile ]; then
		echo $testFile is missing !!!
		exit 1
	fi
done