#!/bin/sh
set -eu
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
rm -f tmp/file.state
cp samples/test.txt tmp/
python -m openpipe.cli  run $DIR/test_file_delta_state.yaml > tmp/zero
[[ "$(wc -c tmp/zero| cut -d" " -f1)" == "0" ]] || exit 1   # Exit if is not zero
echo OK
echo Line 3 > tmp/test.txt
python -m openpipe.cli  run $DIR/test_file_delta_state.yaml > tmp/zero
echo OK
