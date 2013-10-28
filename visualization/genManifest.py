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

# This mini script finds the .h and .txx files and put them into include directory

import sys
import os

ITKModulePath = "/home/xiaoxiao/work/src/ITK/Modules"

# [ITK file name] [Group name ] [Module name] [Subdir in the module]
with open('./Manifest.txt','w') as Manifest:
    for root, subFolders, files in os.walk(ITKModulePath):
        for name in files:
           ext = name.split('.')[-1]
           if ( ext == "hxx" or ext =="h" or ext == "cxx"):
             filename = os.path.join(root, name)
             parts = filename.split('/')
             group  =   parts[-4]
             module =   parts[-3]
             subdir =   parts[-2]
             if(not 'ThirdParty' in parts):
               if (not subdir == "test"):
                 line =filename+' '+group+' '+module+' '+subdir+'\n'
                 Manifest.write(line);

Manifest.close()

