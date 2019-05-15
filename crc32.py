#!/usr/bin/env python
## crc32.py by Naomi Peori <naomi@peori.ca>

import os
import sys
import binascii
import zipfile

if len(sys.argv) < 2:
  print "Usage:", sys.argv[0], "<file> [offset]"
  sys.exit()

if len(sys.argv) > 2:
  offset = int(sys.argv[2])
else:
  offset = 0

if os.path.isfile(sys.argv[1]):
  if sys.argv[1].endswith(".zip"):
    with zipfile.ZipFile(sys.argv[1]) as file:
      for info in file.infolist():
        if offset > 0:
          with file.open(info.filename) as inputFile:
            data = inputFile.read(offset)
            crc = (binascii.crc32(inputFile.read()) & 0xFFFFFFFF)
            inputFile.close()
        else:
          crc = (info.CRC & 0xFFFFFFFF)
  else:
    with open(sys.argv[1],'rb') as file:
      if offset > 0:
        file.read(offset)
      crc = (binascii.crc32(file.read()) & 0xFFFFFFFF)
      file.close()

print "%08X" % crc
