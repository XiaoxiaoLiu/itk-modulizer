#!/usr/bin/python
#==========================================================================
#
#   Copyright Insight Software Consortium
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#          http://www.apache.org/licenses/LICENSE-2.0.txt
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
#
#==========================================================================*/
# This script is used to generate two XML files that organize the hierarchy
# of groups, modules and classes.
#
# To run it, type ./modulefinder.py   ITK_SOURCE_TREE
#
# from the directory where the Manifest.txt file is.
# an output file called itkModules.xml will be generated.
#

import glob
import sys
import os.path
import re

if len(sys.argv) != 3:
    print("USAGE:  {0} [monolithic ITK PATH] [modular ITK PATH]".format(sys.argv[0]))
    sys.exit(-1)


HeadOfITKTree = sys.argv[1];
if (HeadOfITKTree[-1] == '/'):
    HeadOfITKTree = HeadOfITKTree[0:-1]

HeadOfModularITKTree = sys.argv[2];
if (HeadOfModularITKTree[-1] ==  '/'):
    HeadOfModularITKTree = HeadOfModularITKTree[0:-1]

testFiles = glob.glob(HeadOfITKTree+'/Testing/Code/*/*.cxx')

modulesTable =  open('./visualization/itkModules.xml','w')
missingEntries =  open('./missingIncludes.log','w')

manifestfile = open("./Manifest.txt",'r')
manifestlines = manifestfile.readlines()

classmoduletable = {'classname':'modulename'}
modulegrouptable = {'modulename':'groupname'}
groupnames = []

for line in manifestlines:
  words = line.split()
  inputfile = words[0]
  group = words[1]
  module = words[2]
  destinationSubdir = words[3]
  if destinationSubdir == 'Source':
    basepath, basefilename = os.path.split(inputfile)
    basename, extension = os.path.splitext(basefilename)
    classmoduletable[basename] = module
    modulegroup = modulegrouptable.get(module,'not-found')

    if modulegroup == 'not-found':
      modulegrouptable[module] = group

    try:
        groupindex = groupnames.index(group)
    except ValueError:
        groupindex = -1

    if groupindex == -1:
      groupnames.append(group)

for groupname in groupnames:
  print groupname
  modulesTable.write('<node id="'+groupname+'>\n')
  modulesTable.write('</node>\n')

modulesTable.close()
missingEntries.close()

