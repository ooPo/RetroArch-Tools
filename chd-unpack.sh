#!/bin/bash

## chd-unpack.sh - by Naomi Peori <naomi@peori.ca>
## Unpacks any CHD files in the current directory into their own directories.

IFS="
"

FILES=$(ls *.chd)

for FILE in $FILES; do

  CHD=${FILE%.chd}

  if [ ! -d "${CHD}" ]; then
    mkdir -p "${CHD}"
  fi

  pushd "${CHD}"
    # chdman extractcd -i "../${FILE}" -o "${CHD}.cue" -ob "${CHD}.bin"
    chdman extractcd -i "../${FILE}" -o "${CHD}.cue"
    popd

done

# chdman extractcd -i FILE.chd -o FILE.cue -ob FILE.bin
