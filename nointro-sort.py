#!/usr/bin/env python

##
## nointro-sort.py by Naomi Peori <naomi@peori.ca>
## Sort roms using NoIntro-compatible datfiles.
##

import os
import sys
import binascii
import zipfile
import xml.etree.ElementTree as ET
import shutil
import multiprocessing

##
## Configuration
##

datfolder = "00_DATFILES"
offsets = { 'a78':128, 'lnx':64, 'nes': 16 }

##
## Check the arguments.
##

if len(sys.argv) < 2:
  print "Usage:", sys.argv[0], "<source>"
  sys.exit()

source = sys.argv[1]

if not os.path.isdir(source):
  print "ERROR: Source directory doesn't exist:", source
  sys.exit()

##
## Load the datfiles.
##

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

            size     = int(rom.get('size')) if rom.get('size') else 0
            crc      = int(rom.get('crc'),16) if rom.get('crc') else 0
            filename = datfile[:-4] + "/" + gamename + ".zip"

            if not size in roms:
              roms[size] = {}

            if not crc in roms[size]:
              roms[size][crc] = []

            roms[size][crc].append({'filename': filename, 'romname': romname})

##
## Functions
##

def scanDirectory(directory):
  if os.path.isdir(directory):
    for dirname, subdirectories, filenames in os.walk(directory):
      [pool.apply_async(scanFile, args=(dirname + "/" + filename,)) for filename in filenames]

def scanFile(filename):
  if filename.endswith(".zip"):
    print filename
    with zipfile.ZipFile(filename, mode="r", allowZip64=True) as file:
      for info in file.infolist():

        data      = file.read(info.filename)
        extension = info.filename[-3:]
        offset    = offsets[extension] if extension in offsets else 0
        crc       = info.CRC if offset == 0 else binascii.crc32(data[offset:]) & 0xFFFFFFFF
        size      = info.file_size - offset

        matchFile(size, crc, data)

def matchFile(size, crc, data):
  if size in roms:
    if crc in roms[size]:
      for rom in roms[size][crc]:
        writeFile(rom['filename'],rom['romname'], data)

def writeFile(filename, romname, data):
  if not os.path.isfile(filename):
    directory = os.path.dirname(filename)
    if not os.path.isdir(directory):
      os.makedirs(os.path.dirname(filename))
  with zipfile.ZipFile(filename, mode="a", compression=zipfile.ZIP_DEFLATED, allowZip64=True) as file:
    if not romname in file.namelist():
      print "  " + filename + " " + romname
      file.writestr(romname, data);

##
## Main Program
##

pool = multiprocessing.Pool(4)
scanDirectory(source)
pool.close()
pool.join()
