##
## RetroArch-Tools
## by Naomi Peori <naomi@peori.ca>
##

I installed Lakka and it was great but a little rough at times. I made
these tools to help manage roms and playlists. They run fine on-device
or on any reasonably unix-like platform. Enjoy!

compress.sh <directory>
  - Iterates through all files in the specified directory creating zip
    files for each if one does not already exist.

crc32.py <filename>
  - Calculates the CRC32 value for the file.
  - Uses the internal value instead for zip files.
  - Useful for scripts that need a quick CRC32 value.

scan-roms.sh <directory> <name>
  - Scans the directory and generates a RetroArch compatible playlist.
  - Lakka missed some of my sets so I made this to do it manually.

sort-roms.py <source> <destination> <datfile> <offset>
  - Uses No-Intro compaible datfiles.
  - Recursively scans the source directory and copies on match.
  - Offset, in bytes, to skip headers. Does not work on zipped files.
