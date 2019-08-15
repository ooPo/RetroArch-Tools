#!/usr/bin/env python

##
## nointro-audit.py by Naomi Peori <naomi@peori.ca>
## Audit roms using NoIntro-compatible datfiles.
##

import os
import sys
import binascii
import zipfile
import xml.etree.ElementTree as ET
import shutil

##
## Configuration
##

datfolder = "00_DATFILES"
offsets = { 'a78':128, 'lnx':64, 'nes': 16 }

##
## Load the datfiles.
##

folders = []
roms = {}

for dirname, subdirectories, filenames in os.walk(datfolder):
  for datfile in filenames:
    if datfile.endswith(".dat"):
      print datfile
      tree = ET.parse(datfolder + "/" + datfile)
      root = tree.getroot()
      for game in root.findall('game') + root.findall('machine'):
        gamename = game.get('name')
        for rom in game.findall('rom'):
          if not rom.get('merge') and not rom.get('status') == "nodump":
            romname = rom.get('name')

            folder   = datfile[:-4]
            filename = folder + "/" + gamename + ".zip"
            size     = int(rom.get('size')) if rom.get('size') else 0
            crc      = int(rom.get('crc'),16) if rom.get('crc') else 0

            if folder not in folders:
              folders.append(folder)

            if not filename in roms:
              roms[filename] = {}

            roms[filename][romname] = {'size': size, 'crc': crc}

##
## Check for unwanted files.
##

def scanExtras(directory):
  for dirname, subdirectories, filenames in os.walk(directory):
    for subdirectory in subdirectories:
      scanDirectory(dirname + "/" + subdirectory)
    for filename in filenames:
      file = dirname + "/" + filename
      if not file in roms:
        print "EXTRA FILE: " + file

for folder in folders:
  scanExtras(folder)

##
## Check existing files.
##

for filename in roms:
  if not os.path.isfile(filename):
    print "MISSING FILE: " + filename
  else:
    if filename.endswith(".zip"):
      with zipfile.ZipFile(filename, mode="r", allowZip64=True) as file:
        for rom in roms[filename]:
          if rom not in file.namelist():
            print "MISSING ROM: " + filename + "/" + rom
        for info in file.infolist():
          romname = filename + "/" + info.filename
          if info.filename not in roms[filename]:
            print "EXTRA ROM: " + romname
          else:
            rom = roms[filename][info.filename]

            extension = info.filename[-3:]
            offset    = offsets[extension] if extension in offsets else 0
            data      = file.read(info.filename) if offset != 0 else 0
            crc       = info.CRC if offset == 0 else binascii.crc32(data[offset:]) & 0xFFFFFFFF

            if rom['size'] != info.file_size - offset:
              print "CORRUPT SIZE: " + romname
            if rom['crc'] != crc:
              print "CORRUPT CRC: " + romname

