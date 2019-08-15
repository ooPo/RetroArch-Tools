#!/usr/bin/env python

##
## sort-everdrive.py by Naomi Peori <naomi@peori.ca>
## Sort roms using EverDrive compatible datfiles.
##

import os
import sys
import zipfile

##
## Check the arguments.
##

if len(sys.argv) < 4:
  print "Usage:", sys.argv[0], "<source> <destination> <datfile>"
  sys.exit()

source      = sys.argv[1]
destination = sys.argv[2]
datfile     = sys.argv[3]

if not os.path.isdir(source):
  print "ERROR: Source directory doesn't exist:", source
  sys.exit()

if not os.path.isdir(destination):
  print "WARNING: Destination directory doesn't exist:", destination
  sys.exit()

if not os.path.isfile(datfile):
  print "ERROR: Data file does not exist:", datfile
  sys.exit()

##
## Load the datfile.
##

roms = {}

with open(datfile, "r") as file:
  lines = file.read().splitlines()
  file.close()
  for line in lines:
    temp1, name, temp3, temp4, crc32 = line.split("\t");
    crc32 = int(crc32, 16)
    roms[crc32] = name

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

def scanFile(filename):
  if filename.endswith(".zip"):
    print filename
    with zipfile.ZipFile(filename, mode="r", allowZip64=True) as file:
      for info in file.infolist():
        matchFile(file, info.filename, info.CRC)
      file.close()

def matchFile(file, name, crc):
  if crc in roms.keys():
    filename = destination + "/" + roms[crc]
    writeFile(filename, file.read(name))

def writeFile(filename, data):
  if not os.path.isfile(filename):
    directory = os.path.dirname(filename)
    if not os.path.isdir(directory):
      os.makedirs(os.path.dirname(filename))
    with open(filename, "w") as file:
      print "  " + filename
      file.write(data)
      file.close()

##
## Main Program
##

scanDirectory(source)
