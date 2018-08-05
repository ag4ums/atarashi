#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Copyright 2018 Aman Jain (amanjain5221@gmail.com)

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
import argparse
import json
from multiprocessing import Pool as ThreadPool
import os
from pathlib import Path

from tqdm import tqdm

from atarashi.libs.license_clustering import cluster_licenses
from atarashi.license.licenseLoader import LicenseLoader

__author__ = "Aman Jain"
__email__ = "amanjain5221@gmail.com"

globalLicenseList = ""


def find_ngrams(input_list, n):
  return zip(*[input_list[i:] for i in range(n)])


def load_database(licenseList, verbose = 0):
  if isinstance(licenseList, str):
    licenses = LicenseLoader.fetch_licenses(licenseList)
    if 'processed_text' not in licenses.columns:
      raise ValueError('The license list does not contain processed_text column.')
  else:
    licenses = licenseList

  uniqueNGrams = []

  cluster_arr = cluster_licenses(licenses, verbose)
  for cluster in cluster_arr:
    license_text = licenses[licenses['shortname'] == cluster[0]].iloc[0]['processed_text']
    ngrams = []
    ngramrange = [2, 5, 6, 7, 8]
    for x in ngramrange:
      ngrams += list(find_ngrams(license_text.split(), x))
    obj = {
      'shortname': cluster,  # add all shortnames
      'ngrams': ngrams
    }
    uniqueNGrams.append(obj)
  return uniqueNGrams, cluster_arr, licenses


def unique_ngrams(uniqueNGram):
  matches = []

  filtered = [x for x in globalLicenseList if x[0] not in uniqueNGram['shortname']]
  for ngram in uniqueNGram['ngrams']:
    find = ' '.join(ngram)
    ismatch = True
    # check with all license text except for licenses in cluster
    for lic in filtered:
      if find in lic[1]:
        ismatch = False
        break

    if ismatch:
      matches.append(find)
  # print("Matches", matches)
  return matches


def createNgrams(licenseList, ngramJsonLoc, threads = os.cpu_count(),
                 verbose = 0):
  uniqueNGrams, cluster_arr, licenses = load_database(licenseList, verbose)
  no_keyword_matched = []
  matched_output = []
  ngram_keywords = []

  cpuCount = os.cpu_count()
  threads = cpuCount * 2 if threads > cpuCount * 2 else threads
  pool = ThreadPool(threads)
  zip_ngrams = zip(list(range(len(cluster_arr))), uniqueNGrams)

  globalLicenseList = licenseList
  for idx, row in enumerate(tqdm(pool.imap_unordered(unique_ngrams, uniqueNGrams),
                                 desc = "Licenses processed", total = len(cluster_arr),
                                 unit = "license")):

    matched_output.append([str(uniqueNGrams[idx]['shortname']), len(row)])
    if len(row) == 0:
      no_keyword_matched.append(uniqueNGrams[idx]['shortname'])

    ngram_keywords.append({
      'shortname': uniqueNGrams[idx]['shortname'],
      'ngrams': row
    })

  ngramJsonLoc = os.path.abspath(ngramJsonLoc)
  folder = os.path.dirname(ngramJsonLoc)

  Path(folder).mkdir(exist_ok = True)
  with open(ngramJsonLoc, 'w') as myfile:
    myfile.write(json.dumps(ngram_keywords))
  return ngramJsonLoc, matched_output, no_keyword_matched


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("processedLicenseList", help = "Specify the processed license list file")
  parser.add_argument("ngramJson", help = "Specify the location to store "
                      "NGRAM JSON")
  parser.add_argument("-t", "--threads", required = False, default = os.cpu_count(),
                      type = int,
                      help = "No of threads to use for download. Default: CPU count")
  parser.add_argument("-v", "--verbose", help = "increase output verbosity",
                      action = "count", default = 0)
  args = parser.parse_args()

  licenseList = args.processedLicenseList
  threads = args.threads
  ngramJsonLoc = args.ngramJson
  verbose = args.verbose

  createNgrams(licenseList, ngramJsonLoc, threads, verbose = verbose)
  if verbose > 0:
    print(matched_output)
    print("licenses with no unique keywords")
    print(no_keyword_matched)

'''
Steps:
1. Get all licenses (processed)
2. Make ngrams of it and store somewhere
3. Now check all the ngrams of each license
4. store the unique ngrams in a file (maybe csv or any file)

'''