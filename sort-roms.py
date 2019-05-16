#!/usr/bin/env python

##
## sort-roms.py by Naomi Peori <naomi@peori.ca>
## Sort roms using MAME & NoIntro compatible datfiles.
##

import os
import sys
import binascii
import zipfile
import xml.etree.ElementTree as ET
import shutil

##
## Check the arguments.
##

if len(sys.argv) < 4:
  print "Usage:", sys.argv[0], "<source> <destination> <datfile> <offset>"
  sys.exit()

source      = sys.argv[1]
destination = sys.argv[2]
datfile     = sys.argv[3]

offset = 0
if len(sys.argv) > 4:
  offset = int(sys.argv[4])

if not os.path.isdir(source):
  print "ERROR: Source directory doesn't exist:", source
  sys.exit()

if not os.path.isdir(destination):
  print "WARNING: Destination directory doesn't exist:", destination
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

##
## Parse the datfile into a faster searchable structure.
##

print "Parsing the datfile:"

roms = {}

for game in root.findall('game') + root.findall('machine'):
  gameName = game.get('name')
  for rom in game.findall('rom'):
    if not rom.get('merge') and not rom.get('status') == "nodump":
      romName = rom.get('name')
      size = 0
      if rom.get('size'):
        size = int(rom.get('size'))
      crc = 0
      if rom.get('crc'):
        crc = int(rom.get('crc'),16)
      if not size in roms.keys():
        roms[size] = {}
      if not crc in roms[size].keys():
        roms[size][crc] = {}
      if not roms[size][crc]:
        roms[size][crc] = []
      roms[size][crc].append({'gameName': gameName, 'romName': romName})

print "Done!"

##
## Helper Functions
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
## Functions
##

def scanDirectory(directory):
  if os.path.isdir(directory):
    for dirname, subdirectories, filenames in os.walk(directory):
      for subdirectory in subdirectories:
        scanDirectory(dirname + "/" + subdirectory)
      for filename in filenames:
        scanFile(dirname + "/" + filename)

def scanFile(filepath):
  if filepath.endswith(".zip"):
    print filepath
    with zipfile.ZipFile(filepath, mode="r", allowZip64=True) as file:
      for info in file.infolist():
        matchFile(file, info.filename, getCrc(file, info.filename, info.CRC), info.file_size - offset)
      file.close()

def matchFile(file, name, crc, size):
  if size in roms.keys():
    rom = roms[size]
    if crc in rom.keys():
      matches = rom[crc]
      for match in matches:
        gameName = match['gameName']
        romName  = match['romName']
        with zipfile.ZipFile(destination + "/" + gameName + ".zip", mode="a", compression=zipfile.ZIP_DEFLATED, allowZip64=True) as outputFile:
          if not romName in outputFile.namelist():
            print "  " + name + " ==> " + gameName + "/" + romName
            outputFile.writestr(romName, file.read(name));
          outputFile.close()

##
## Main Program
##

scanDirectory(source)
