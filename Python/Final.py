# reads the name, say F, of a text file, and creates a text file 
# F.json containing one JSON object with three fields:
# {"file_name": "F", "title": "1st line of F", "content": "rest of F lines"}
# any double quote, \n, \r in F is replaced with a space " "
#

import sys
import json

fname = raw_input()
try:
    inf = open(fname, "r")
except IOError:
    print "\nError opening file!"
    sys.exit()

Contents = inf.readlines();
    
Headers = ["Headline", "Reporters/ Reporting Agency", "Content"]

Content_String = ''

for i in range(2, len(Contents)):
    Content_String += Contents[i]
            
Final = []
Final.append(Contents[0])
Final.append(Contents[1])
Final.append(Content_String)

json_dict = dict(zip(Headers, Final))
# print(json_dict)
json_dict=json.dumps(json_dict);
sys.stdout.write(json_dict)

inf.close()
