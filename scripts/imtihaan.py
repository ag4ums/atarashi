#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
version 2 as published by the Free Software Foundation.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

__author__ = "Aman Jain"

import os
import sys
import argparse

from CosineSimNgram import NgramSim
from dameruLevenDist import classifyLicenseDameruLevenDist
from tfidf import tfidfcosinesim, tfidfsumscore

args = None

if __name__ == "__main__":
  """
  Iterate on all files in directory 
  expected output is the name 
  """
  parser = argparse.ArgumentParser()
  parser.add_argument("LicenseList", help="Specify the processed license list file which contains licenses")
  parser.add_argument("AgentName", choices=['DLD', 'tfidfcosinesim', 'tfidfsumscore', 'Ngram'],
                      help="Name of the agent that needs to be run")
  parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
  args = parser.parse_args()
  agent_name = args.AgentName
  processedLicense = args.LicenseList

  pathname = os.path.dirname(sys.argv[0])
  pathto = os.path.abspath(pathname) + '/../tests/SPDXTestfiles'
  for subdir, dirs, files in os.walk(pathto):
    for file in files:
      filepath = subdir + os.sep + file
      actual_license = filepath.split('/')[-1].split('.c')[0]
      if agent_name == "DLD":
        result = str(classifyLicenseDameruLevenDist(filepath, processedLicense))
      elif agent_name == "tfidfcosinesim":
        result = str(tfidfcosinesim(filepath, processedLicense))
      elif agent_name == "tfidfsumscore":
        result = str(tfidfsumscore(filepath, processedLicense))
      elif agent_name == "Ngram":
        result = str(NgramSim(filepath, processedLicense, "BigramCosineSim"))
      print(actual_license + " " + result)