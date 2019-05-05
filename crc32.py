#!/usr/bin/env python
## crc32.py by Naomi Peori <naomi@peori.ca>

import os
import sys
import binascii
import zipfile

if len(sys.argv) != 2:
  print "Usage:", sys.argv[0], "<file>"
  sys.exit()

if os.path.isfile(sys.argv[1]):
  if sys.argv[1].endswith(".zip"):
    with zipfile.ZipFile(sys.argv[1]) as file:
      for info in file.infolist():
        crc = (info.CRC & 0xFFFFFFFF)
  else:
    with open(sys.argv[1],'rb') as file:
      crc = (binascii.crc32(file.read()) & 0xFFFFFFFF)
      file.close()

print "%08X" % crc
