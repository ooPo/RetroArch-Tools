#!/bin/bash
## retroarch-scan.sh by Naomi Peori <naomi@peori.ca>
## Scan a folder of roms to generate a RetroArch compatible playlist.

IFS="
"

if [ ! $# -eq 2 ]; then
  echo "Usage: ${0} <directory> <name>"
  exit
fi

if [ -d "${1}" ]; then

  ## Open the playlist file.
  exec 3>"${2}.lpl"

  ## Output the playlist header.
  echo '{'                                      >&3
  echo '  "version": "1.0",'                    >&3
  echo '  "items": ['                           >&3

  ## For each zip file...
  for FILE in $(find "${1}" -type f | sort); do
    if [ -f "${FILE}" ]; then
      echo "${FILE}"

      ## Optain some metadata about the file.
      FILENAME=$(basename "${FILE}")
      CRC32=$(./crc32.py "${FILE}")

      ## Output the playlist entry.
      echo '    {'                              >&3
      echo '      "path": "'${FILE}'",'         >&3
      echo '      "label": "'${FILENAME%.*}'",' >&3
      echo '      "core_path": "DETECT",'       >&3
      echo '      "core_name": "DETECT",'       >&3
      echo '      "crc32": "'${CRC32}'|crc",'   >&3
      echo '      "db_name": "'${2}'.lpl"'      >&3
      echo '    },'                             >&3

    fi
  done

  ## Output the playlist footer.
  echo '  ]'                                    >&3
  echo '}'                                      >&3

  ## Close the playlist file.
  exec 3>&-

fi
