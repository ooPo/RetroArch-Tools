#!/bin/sh
## compress.sh by Naomi Peori <naomi@peori.ca>
## Create single zip files for a directory of files.

IFS="
"

if [ ! $# -eq 1 ]; then
  echo "Usage: ${0} <directory>";
  exit
fi

if [ -d "${1}" ]; then
  for FILE in $(find "${1}" -type f ! -name "*.zip" | sort); do
    if [ -f "${FILE}" ]; then
      ZIPFILE="${FILE%.*}.zip"
      if [ ! -f "${ZIPFILE}" ]; then
        zip -9 "${ZIPFILE}" "${FILE}"
      fi
    fi
  done
fi
