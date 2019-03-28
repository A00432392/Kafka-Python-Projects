import fileinput
import json
import sys 
import re
import datetime
import pickle
from dateutil.rrule import rrule, DAILY


def replace(file):
    searchExp="]["
    replaceExp="   ,"
    for line in fileinput.input(file, inplace=True):
        if searchExp in line:
            line = line.replace(searchExp,replaceExp)
        sys.stdout.write(line)
        
        
def beautify(file):
    with open(file) as f:
        json_string = f.read()
    try:
        parsed_json = json.loads(json_string)
        formatted_json = json.dumps(parsed_json, indent = 4,sort_keys=True)
        with open("flight_details.json", "w") as f:
            f.write(formatted_json)
    except Exception as e:
        print(repr(e))
    
        



if __name__ == "__main__":
    fil = "yhz-03_21-flight.json"
    replace(fil)
    beautify(fil)
    print("end")