#!/usr/bin/env python

##
## audit-roms.py by Naomi Peori <naomi@peori.ca>
## Audit roms using MAME & NoIntro compatible datfiles.
##

import os
import sys
import binascii
import zipfile
import xml.etree.ElementTree as ET

##
## Check the arguments.
##

if len(sys.argv) < 3:
  print "Usage:", sys.argv[0], "<source> <datfile> [offset]"
  sys.exit()

source  = sys.argv[1]
datfile = sys.argv[2]

if len(sys.argv) > 3:
  offset  = int(sys.argv[3])
else:
  offset = 0

if not os.path.isdir(source):
  print "ERROR: Source directory doesn't exist:", source
  sys.exit()

if not os.path.isfile(datfile):
  print "ERROR: Data file does not exist:", datfile
  sys.exit()

if offset < 0:
  print "ERROR: Negative offsets are unsupported.", offset
  sys.exit()

##
## Load the datfile.
##

print "Loading the datfile: "
tree = ET.parse(datfile)
root = tree.getroot()
print "Done!"
print " "

##
## CRC Functions
##

def getCrc(file, name, crc):
  if offset == 0:
    return crc
  else:
    with file.open(name) as inputFile:
      data = inputFile.read(offset)
      data = inputFile.read()
      inputFile.close()
      return binascii.crc32(data) & 0xFFFFFFFF

##
## Find and Match Functions
##

def findRom(roms, name):
  for rom in roms:
    if name == rom.get('name'):
      return True
  return False

def matchRom(roms, name, size, crc):
  for rom in roms:
    romSize = 0
    if rom.get('size'):
      romSize = int(rom.get('size'))
    romCrc = 0
    if rom.get('crc'):
      romCrc  = int(rom.get('crc'),16)
    if name == rom.get('name') and size == romSize and crc == romCrc:
      return True
  return False

##
## Reset the counters.
##

games_total   = 0
games_missing = 0
games_extra   = 0

roms_total    = 0
roms_corrupt  = 0
roms_missing  = 0
roms_extra    = 0

##
## Audit the games.
##

games = root.findall('game') + root.findall('machine')
games_total = len(games)

for game in games:

  gameName = game.get('name') + ".zip"
  gameFile = source + "/" + gameName

  if not os.path.isfile(gameFile):
    print "MISSING GAME: " + gameName
    games_missing += 1

  else:
    with zipfile.ZipFile(gameFile, mode="r", allowZip64=True) as file:

      roms = game.findall('rom')
      for rom in roms[:]:
        if rom.get('merge') or rom.get('status') == "nodump":
          roms.remove(rom)

      roms_total += len(roms)

      romNames = []
      for rom in roms:
        romNames.append(rom.get('name'))

      for info in file.infolist():

        name = info.filename;
        size = info.file_size - offset;
        crc  = getCrc(file, name, info.CRC);

        if not name in romNames:
          print "EXTRA ROM:" + gameName + "/" + name
          roms_extra += 1

        elif not matchRom(roms, name, size, crc):
          print "CORRUPT ROM:" + gameName + "/" + name
          roms_corrupt += 1

      for romName in romNames:
        if not romName in file.namelist():
          print "MISSING ROM:" + gameName + "/" + romName
          roms_missing += 1

      file.close()

##
## Audit the files.
##

gameNames = []
for game in games:
  gameNames.append(game.get('name') + ".zip")

for dirname, subdirectories, filenames in os.walk(source):
  for filename in filenames:
    if filename.endswith(".zip"):
      if not filename in gameNames:
        print "EXTRA GAME:" + filename
        games_extra += 1

##
## Output the stats.
##

print " "
print "Stats:"
print "  Missing Games: %d/%d (%.02f%%)" % (games_missing, games_total, 100 * float(games_missing) / float(games_total))
print "  Extra Games:   %d" % games_extra
print "  Missing Roms:  %d/%d (%.02f%%)" % (roms_missing, roms_total, 100 * float(roms_missing) / float(roms_total))
print "  Corrupt Roms:  %d" % roms_corrupt
print "  Extra Roms:    %d" % roms_extra
