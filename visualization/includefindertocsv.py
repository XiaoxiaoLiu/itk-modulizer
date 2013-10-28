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
# This script is used to find all the #include relationships between ITK files.
# It looks in the Manifest.txt file and for each file it generates the list of
# files that are included from there.

#
# To run it, type ./includefinder.py   ITK_SOURCE_TREE
#
# from the directory where the Manifest.txt file is.
# an output file called itkIncludes.xml will be generated.
#

import glob
import sys
import os.path
import re


includesTable =  open('./itkIncludes.csv','w')
missingEntries =  open('./missingIncludes.log','w')
print('created ./itkIncludes.cvs and ./missingIncludes.log')

manifestfile = open("Manifest.txt",'r')
manifestlines = manifestfile.readlines()

moduletable = {'classname':'modulename'}

for line in manifestlines:
  if (line[0]!='#'):
    words = line.split()
    inputfile = words[0]
    group = words[1]
    module = words[2]
    destinationSubdir = words[3]
    if destinationSubdir == 'src' or destinationSubdir =='include':
      basepath, basefilename = os.path.split(inputfile)
      basename, extension = os.path.splitext(basefilename)
      moduletable[basename] = module

for line in manifestlines:
  if (line[0]!='#'):
    words = line.split()
    inputfile = words[0]
    group = words[1]
    module = words[2]
    destinationSubdir = words[3]
    if destinationSubdir == 'src' or destinationSubdir == 'include':
      basepath, basefilename = os.path.split(inputfile)
      basename, extension = os.path.splitext(basefilename)
  #    includesTable.write('<class id="'+basename+'" module="'+module+'">\n')
      basemodule = moduletable.get(basename,'not-found')
      fullinputfile = inputfile
      for codeline in open(fullinputfile,'r'):
        if codeline.find("#include") != -1:
          searchresult = re.search('itk.*\.h',codeline)
          if searchresult:
            includedclass = searchresult.group()
            if not re.search('\+',includedclass):
              if not re.search('itksys',includedclass):
                if not re.search(basename,includedclass):
                  includebasename, includeextension = os.path.splitext(includedclass)
                  includemodule = moduletable.get(includebasename,'not-found')

                  if includemodule == 'not-found':
                    missingEntries.write(includedclass+' included from '+inputfile+'\n')
                  else:
                    if includemodule != 'itk-common':
                      if basemodule != includemodule:
                        includesTable.write(basename+","+includebasename+'\n')

  #                includesTable.write('\t<class id="'+includebasename+'" module="'+includemodule+'">\n')
  #                includesTable.write('\t</class>\n')
  #    includesTable.write('</class>\n')

includesTable.close()
missingEntries.close()
