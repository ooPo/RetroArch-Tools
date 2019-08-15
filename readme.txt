##
## RetroArch-Tools
## by Naomi Peori <naomi@peori.ca>
##

I installed Lakka and it was great but a little rough at times. I made
these tools to help manage roms and playlists. They run fine on-device
or on any reasonably unix-like platform. Enjoy!

nointro-audit.sh <source>
  - Uses No-Intro/MAME compatible datfiles.
  - Scans the source directory and compare its contents to the datfile.

nointro-sort.py <source>
  - Uses No-Intro/MAME compatible datfiles.
  - Recursively scans the source directory and copies on match.

everdrive-sort.py <source>
  - Uses EverDrive/SmokeMonsterPacks compatible datfiles.
  - Recursively scans the source directory and copies on match.

retroarch-scan.sh <directory> <name>
  - Scans the directory and generates a RetroArch compatible playlist.

chd-unpack.sh
  - Unpacks any CHD files in the current directory into their own directories.

compress.sh <source>
  - Scans the source directory and creates a zip file for each file.
  - Compression is skipped if the zip file already exists.

crc32.py <filename>
  - Calculates the CRC32 value for the file.
  - Uses the internal value instead for zip files.
