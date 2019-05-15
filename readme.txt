##
## RetroArch-Tools
## by Naomi Peori <naomi@peori.ca>
##

I installed Lakka and it was great but a little rough at times. I made
these tools to help manage roms and playlists. They run fine on-device
or on any reasonably unix-like platform. Enjoy!

audit-roms.sh <source> <datfile> [offset]
  - Uses MAME and No-Intro compatible datfiles.
  - Scans the source directory and compare its contents to the datfile.
  - Outputs stats and a list of missing games and roms.

compress.sh <source>
  - Scans the source directory and creates a zip file for each file.
  - Compression is skipped if the zip file already exists.

crc32.py <filename>
  - Calculates the CRC32 value for the file.
  - Uses the internal value instead for zip files.
  - Useful for scripts that need a quick CRC32 value.

sort-roms.py <source> <destination> <datfile> [offset]
  - Uses MAME and No-Intro compatible datfiles.
  - Recursively scans the source directory and copies on match.
  - Offset, in bytes, to skip headers.

scan-roms.sh <directory> <name>
  - Scans the directory and generates a RetroArch compatible playlist.
  - Lakka missed some of my sets so I made this to do it manually.
