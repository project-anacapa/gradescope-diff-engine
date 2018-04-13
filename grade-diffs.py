#!/usr/bin/env python3

from __future__ import print_function

import json
import pprint
import argparse
import textwrap
import os
import sys
import re
from jsonschema import validate
from jsonschema import ValidationError
from pprint import pprint

testSchema ={
  "type": "object",
  "properties": {
    "stdout": {
      "type": "number"
    },
    "stderr": {
      "type": "number"
    },
    "name": {
      "type": "string"
    },
    "visibility": {
      "type": "string",
      "enum": [
        "hidden",
        "after_due_date",
        "after_published",
        "visible"
      ]
    }
  },
  "additionalProperties": False
}


def lineToTestAnnotation(args,line,linenumber):
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

   retVal = { "line" : line, "linenumber" : linenumber }

   test_regular_expression="^#[ ]*@test(.*)$" # test it at https://pythex.org/
   
   matches = re.match(test_regular_expression, line.strip())
   if not matches:
       retVal["isTest"]=False
       retVal["isError"]=False       
       return retVal

   retVal["jsonString"]=matches.group(1)

    
   try:
       retVal["test"]=json.loads(retVal["jsonString"])
       v=validate(retVal["test"], testSchema)
       retVal["isTest"]=True
       retVal["isError"]=False
   except ValidationError:
       retVal["isTest"]=False       
       retVal["isError"]=True
       retVal["error"]="ERROR MESSAGE SHOULD GO HERE"
         
   return retVal
    



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
    if (args.verbose > 1):
        print("linenumber: ",linenumber," line: ",line.strip())
    testAnnotation = lineToTestAnnotation(args,line,linenumber)
    return testAnnotation
 
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

    parser.add_argument('--verbose', '-v', action='count', default=0)
    parser.add_argument('--reference', '-r',action='store_true')
    
    args = parser.parse_args()    

    if (not os.path.isfile(args.script)):
        haltWithError("ERROR: the script " + args.script + " does not exist")


    testAnnotations=[]
    with open(args.script) as infile:
        linenumber = 0
        prevLineWasTestAnnotation = False
        for line in infile:
            linenumber += 1
            if prevLineWasTestAnnotation:
               ta["shell_command"]=line
               testAnnotations.append(ta)
               prevLineWasTestAnnotation = False
            else:
              ta = processLine(args,line,linenumber)
              if ta["isTest"]:
                 prevLineWasTestAnnotation = True

    if args.verbose > 2:
       pprint(testAnnotations)

    reference_dir = args.script + "-reference"        

       
    if args.reference:
       print("Creating directory ",reference_dir,"...")
       try:
          os.mkdir(reference_dir)
       except FileExistsError:
          haltWithError("Error: " + reference_dir + " already exists.  Please delete it before proceeding")
          
       pass # Do what is needed for calculating reference output here
    
    else:

       if (not os.path.isdir(reference_dir)):
          haltWithError("ERROR: the directory " + reference_dir + " does not exist")

       # Do what is needed to run each command and calculate the grades
       # Then add each of those to the JSON file.
       
       results = loadResultsJsonIfExists()

       # THIS IS THE PLACE IN THE CODE WHERE YOU ADD TESTS into the results["tests"] array.
        
       with open('results.json', 'w') as outfile:
           json.dump(results, outfile)


    
