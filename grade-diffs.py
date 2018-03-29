#!/usr/bin/env python

from __future__ import print_function

import json
import pprint
import argparse
import textwrap
import os
import sys

def loadResultsJsonIfExists():    
    try:
        results = json.load(open('results.json'))
    except:
        results = { "tests" : [] }
    return results    

def haltWithError(message):
    print (message)
    sys.exit(1)

if __name__ == "__main__":


    parser = argparse.ArgumentParser(description='Generate Gradescope compatible results.json for diff-based testing',
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('script', 
        help= textwrap.dedent('''\
        name of script file, e.g. diffs.sh

        The directory diffs.sh-reference should already exist, having been
        populated with the command generate-reference-output.py diffs.sh

        blank lines and lines with \# in first column will be ignored
        other lines will have comments with four comma separated fields, e.g.

          echo foo \# 10, You should echo foo to stdout
          >&2 echo "error" # , , 10, You should echo bar to stderr
        
       '''))

    args = parser.parse_args()    

    reference_dir = args.script + "-reference"
    
    if (not os.path.isdir(reference_dir)):
        haltWithError("ERROR: the directory " + reference_dir + " does not exist")

    
    results = loadResultsJsonIfExists()

    with open('results.json', 'w') as outfile:
        json.dump(results, outfile)


    
