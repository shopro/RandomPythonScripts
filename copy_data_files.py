#!/usr/bin/env python

import shutil
import os
import sys
import argparse
import re
import time

parser = argparse.ArgumentParser(description=
     'Copy NSpike .dat files into individual directories');
parser.add_argument('-s', '--sourcedir',
    help='Source directory containing .dat files');
parser.add_argument('-d', '--destdir', 
    help='Destination directory for .dat file directories');
parser.add_argument('--add-dates', help='Append file date to directory name',
    action='store_true');

args = parser.parse_args();

if args.sourcedir :
  SourceDirectory = args.sourcedir;
else :
  SourceDirectory = os.getcwd();

if args.destdir :
  DestinationDirectory = args.destdir;
else :
  DestinationDirectory = os.getcwd();

SourceDirectory = os.path.realpath(SourceDirectory);
DestinationDirectory = os.path.realpath(DestinationDirectory);

print "Source files directory is: ", SourceDirectory
print "Destination files directory is: ", DestinationDirectory

DatFiles = os.listdir(SourceDirectory);

for f in DatFiles:
  FullFileName = os.path.realpath(os.path.join(SourceDirectory,f))
  filedata = os.path.splitext(os.path.basename(FullFileName))
  if filedata[-1] != ".dat" :
    continue;
  # Get file creation time
  FileDate = time.strftime("%m%d%Y_%H%M", 
      time.gmtime(os.path.getctime(FullFileName)));
  #print "File ", FullFileName, "Just file ", os.path.basename(FullFileName), " Date:", FileDate

  fileregex = re.search(
      'Rat(?P<name>\w*)_Day(?P<day>\w*)_Run(?P<run>\w*)\.*(?P<extra>.*)\.(?P<machine>\w*)\.dat$', 
      os.path.basename(FullFileName))

  if fileregex is None:
    print "File error: ", FullFileName
    continue;

  if args.add_dates :
    AnimalDirName = 'Rat%s_Day%003d_Run%s_%s' % \
                  (fileregex.group('name'), int(fileregex.group('day')),
                     fileregex.group('run'), FileDate)
  else:
    AnimalDirName = 'Rat%s_Day%003d_Run%s' % \
                  (fileregex.group('name'), int(fileregex.group('day')),
                      fileregex.group('run'))
  
  if os.path.exists(os.path.join(DestinationDirectory,AnimalDirName)) :
    AnimalDirName = AnimalDirName + '.2'

  os.makedirs(os.path.join(DestinationDirectory,AnimalDirName))

  print AnimalDirName

  shutil.copy2(FullFileName, os.path.join(DestinationDirectory, AnimalDirName, AnimalDirName +
    '.dat'));

