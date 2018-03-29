#!/usr/bin/env python

import json
import pprint

def loadResultsJsonIfExists():    
    try:
        results = json.load(open('results.json'))
    except:
        results = { "tests" : [] }
    return results    

if __name__ == "__main__":

    results = loadResultsJsonIfExists()

    pprint.pprint(results)
    
    with open('results.json', 'w') as outfile:
        json.dump(results, outfile)


    
