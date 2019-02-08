#!/bin/sh
set -eu

pluginList=$(find openpipe/plugins/ -name "*.py" | grep -v "__init__" | sort)
for pluginFile in $pluginList
do
	mdFile=$(echo $pluginFile | sed "s/\.py/.md/g")
	if [ ! -r $mdFile ]; then
		mkdir -p $(dirname $mdFile)
		echo $mdFile is missing !!!
		exit 1
	fi
done
