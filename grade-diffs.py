#!/usr/bin/env python

from __future__ import print_function

import json
import pprint
import argparse
import textwrap
import os
import sys
import re
from jsonschema import validate

testSchema = {
     "type" : "object",
     "properties" : {
         "stdout" : {"type" : "number"},
         "stderr" : {"type" : "number"},
         "name" :   {"type" : "string"},
         "visibility" : {
             "type" : "string",
             "enum": ["hidden",
                      "after_due_date",
                      "after_published",
                      "visible"]
         }
     }
 }

def lineToTestAnnotation(line,linenumber):
    """
    returns a dictionary indicating whether this line is a test annotation or not

    { isTest: bool, True if this is a test annotation with valid json
      test: dict, the json string converted to a dictionary
      isError: bool, True if this appears to be a test annotation attempt with an error in it
      jsonString: str, the json string extracted (or what we got as the json string)
      line: str, the entire line contents,
      linenumber: int, the line number in the file
      error: str, the best error message we can give
    }
   """

   # TODO... finish this function
    



def loadResultsJsonIfExists():    
    try:
        results = json.load(open('results.json'))
    except:
        results = { "tests" : [] }
    return results    

def haltWithError(message):
    print (message)
    sys.exit(1)

def processLine(args,line, linenumber):
    if (args.verbose > 0):
        print("linenumber: ",linenumber," line: ",line.strip())
   
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

    parser.add_argument('--verbose', '-v', action='count')
    
    args = parser.parse_args()    

    reference_dir = args.script + "-reference"

    if (not os.path.isfile(args.script)):
        haltWithError("ERROR: the script " + args.script + " does not exist")

    if (not os.path.isdir(reference_dir)):
        haltWithError("ERROR: the directory " + reference_dir + " does not exist")

        
    with open(args.script) as infile:
        linenumber = 0
        for line in infile:
            linenumber += 1
            processLine(args,line,linenumber)
        
    results = loadResultsJsonIfExists()

    with open('results.json', 'w') as outfile:
        json.dump(results, outfile)


    
