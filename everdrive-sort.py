#!/usr/bin/env python

##
## everdrive-sort.py by Naomi Peori <naomi@peori.ca>
## Sort roms using EverDrive compatible datfiles.
##

import os
import sys
import zipfile
import multiprocessing

##
## Check the arguments.
##

if len(sys.argv) < 2:
  print "\nUsage:", sys.argv[0], "<source>"
  sys.exit()

source = sys.argv[1]

if not os.path.isdir(source):
  print "ERROR: Source directory doesn't exist:", source
  sys.exit()

##
## Load the datfiles.
##

datfolder = "00_DATFILES"
roms = {}

datfiles = os.listdir(datfolder)
for dirname, subdirectories, filenames in os.walk(datfolder):
  for filename in filenames:
    with open(dirname + "/" + filename, "r") as file:
      for line in file.read().splitlines():
        temp1, name, temp3, temp4, crc32 = line.split("\t");
        crc32 = int(crc32, 16)
        if not crc32 in roms:
          roms[crc32] = []
        roms[crc32].append(name)

##
## Functions
##

def scanDirectory(directory):
  if os.path.isdir(directory):
    for dirname, subdirectories, filenames in os.walk(directory):
      [pool.apply_async(scanFile, args=(dirname + "/" + filename,)) for filename in filenames]
      for subdirectory in subdirectories:
        scanDirectory(dirname + "/" + subdirectory)

def scanFile(filename):
  if filename.endswith(".zip"):
    print filename
    with zipfile.ZipFile(filename, mode="r", allowZip64=True) as file:
      for info in file.infolist():
        matchFile(info.CRC, file.read(info.filename))

def matchFile(crc, data):
  if crc in roms:
    for filename in roms[crc]:
      writeFile(filename, data)

def writeFile(filename, data):
  if not os.path.isfile(filename):
    directory = os.path.dirname(filename)
    if not os.path.isdir(directory):
      os.makedirs(os.path.dirname(filename))
    with open(filename, "w") as file:
      print "  " + filename
      file.write(data)

##
## Main Program
##

pool = multiprocessing.Pool()
scanDirectory(source)
pool.close()
pool.join()
