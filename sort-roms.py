#!/usr/bin/env python
## sort-roms.py by Naomi Peori <naomi@peori.ca>
## Scan and sort roms using No-Intro compatible datfiles.

import os
import sys
import binascii
import zipfile
import xml.etree.ElementTree as ET
import shutil

##
## Check the arguments.
##

if len(sys.argv) != 5:
  print "Usage:", sys.argv[0], "<source> <destination> <datfile> <offset>"
  sys.exit()

source      = sys.argv[1]
destination = sys.argv[2]
datfile     = sys.argv[3]
offset      = int(sys.argv[4])

if not os.path.isdir(source):
  print "ERROR: Source directory doesn't exist.", source
  sys.exit()

if not os.path.isdir(destination):
  print "ERROR: Destination directory doesn't exist.", destination
  sys.exit()

if not os.path.isfile(datfile):
  print "ERROR: Data file does not exist.", datfile
  sys.exit()

if offset < 0:
  print "ERROR: Negative offsets are unsupported.", offset
  sys.exit()

if offset > 0:
  print "WARNING: Non-zero offset will skip zip files.", offset

##
## Load the datfile.
##

tree = ET.parse(datfile)
root = tree.getroot()

##
## File Functions
##

def crcFromFile(filepath):
  if os.path.isfile(filepath):
    if filepath.endswith(".zip"):
      with zipfile.ZipFile(filepath) as file:
        for info in file.infolist():
          return "%08X" % info.CRC
    else:
      with open(filepath,'rb') as file:
        if offset > 0:
          data = file.read(offset)
        data = file.read()
        file.close()
        return "%08X" % (binascii.crc32(data) & 0xFFFFFFFF)

def sizeFromFile(filepath):
  if os.path.isfile(filepath):
    if filepath.endswith(".zip"):
      with zipfile.ZipFile(filepath) as file:
        for info in file.infolist():
          return info.file_size
    else:
      return os.path.getsize(filepath)

##
## Match Functions
##

def matchFile(filepath):
  if os.path.isfile(filepath):
    crc = crcFromFile(filepath)
    size = sizeFromFile(filepath) - offset
    for game in root.findall('game'):
      for rom in game.findall('rom'):
        if rom.get('crc') == crc and int(rom.get('size')) == size:
          return rom.get('name')

##
## Scan Functions
##

def scanDirectory(directory):
  if os.path.isdir(directory):
    for dirname, subdirectories, filenames in os.walk(directory):
      for subdirectory in subdirectories:
        scanDirectory(directory + "/" + subdirectory)
      for filename in filenames:
        scanFile(directory + "/" + filename)

def scanFile(filepath):
  if not (filepath.endswith(".zip") and offset > 0):
    match = matchFile(filepath)
    if match:
      filename, fileextension = os.path.splitext(filepath)
      matchname, matchextension = os.path.splitext(match)
      matchpath = destination + "/" + matchname + fileextension
      if not os.path.isfile(matchpath):
        print "COPYING:", matchpath
        shutil.copyfile(filepath, matchpath)

##
## Main Program
##

scanDirectory(source)
