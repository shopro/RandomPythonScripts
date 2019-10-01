#!/usr/bin/env python

import shutil
import os
import sys
import argparse
import re
import time
import filecmp

parser = argparse.ArgumentParser(description=
     'Copy NSpike .dat files into individual directories');
parser.add_argument('-s', '--source-dir',
    help='Source directory containing .dat files');
parser.add_argument('-d', '--dest-dir', 
    help='Destination directory for .dat file directories');
parser.add_argument('--add-dates', help='Append file date to directory name',
    action='store_true');
parser.add_argument('--reverse-order', help='Reverse default order from Day/Run to Run/Day',
    action='store_true');

args = parser.parse_args();

if args.source_dir :
  SourceDirectory = args.source_dir;
else :
  SourceDirectory = os.getcwd();

if args.dest_dir :
  DestinationDirectory = args.dest_dir;
else :
  DestinationDirectory = os.getcwd();

SourceDirectory = os.path.realpath(SourceDirectory);
DestinationDirectory = os.path.realpath(DestinationDirectory);

print("Source files directory is: ", SourceDirectory)
print("Destination files directory is: ", DestinationDirectory)

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

  if args.reverse_order is not True :
    fileregex = re.search(
        'Rat(?P<name>\w*)_Day(?P<day>\w*)_Run(?P<run>\w*)\.*(?P<extra>.*)\.(?P<machine>\w*)\.dat$', 
        os.path.basename(FullFileName))
  else :
    fileregex = re.search(
        'Rat(?P<name>\w*)_Run(?P<run>\w*)_Day(?P<day>\w*)\.*(?P<extra>.*)\.(?P<machine>\w*)\.dat$', 
        os.path.basename(FullFileName))

  if fileregex is None:
    print("File error: ", FullFileName)
    continue;

  RatName = fileregex.group('name')
  try:
    ExperimentDay = '%003d' % int(fileregex.group('day'))
  except ValueError:
    ExperimentDay = fileregex.group('day')
  ExperimentRun = fileregex.group('run');

  if args.add_dates :
    AnimalDirName = 'Rat%s_Day%s_Run%s_%s' % \
                  (RatName, ExperimentDay, ExperimentRun, FileDate)
  else:
    AnimalDirName = 'Rat%s_Day%s_Run%s' % \
                  (RatName, ExperimentDay, ExperimentRun)
  

  destfile = os.path.join(DestinationDirectory, AnimalDirName, AnimalDirName + '.dat')
  if os.path.exists(destfile) :
    # compare destination file and source and create a new dir if different
    if filecmp.cmp(FullFileName,destfile) is not True :
      print("Creating a new directory for", AnimalDirName)
      AnimalDirName = AnimalDirName + '.2'
      DestinationFileName = os.path.join(DestinationDirectory, AnimalDirName, AnimalDirName + '.dat')
    else :
      print("Ignoring existing", AnimalDirName)
      continue;

  DestinationFileName = os.path.join(DestinationDirectory, AnimalDirName, AnimalDirName + '.dat')
  os.makedirs(os.path.join(DestinationDirectory,AnimalDirName))

  print(AnimalDirName)

  shutil.copy2(FullFileName, DestinationFileName);

