# reads the name, say F, of a text file, and creates a text file 
# F.json containing one JSON object with three fields:
# {"file_name": "F", "title": "1st line of F", "content": "rest of F lines"}
# any double quote, \n, \r in F is replaced with a space " "
#
import json
import sys

# fname = raw_input()
try:
    fo = open("C:\\Users\\Meghashyam\\Desktop\\100607aaa.txt", "r")
except IOError:
    # print "\nError opening file!"
    sys.exit()

# sys.stdout.write('{"file_name": "' + fname + '", "headline": "')
first = True
second = True
linecount = 0

Contents = fo.readlines();
    
Headers = ["Headline", "Reporters/ Reporting Agency", "Content"]

Content_String = ''

for i in range(2, len(Contents)):
    Content_String += Contents[i]
            
Final = []
Final.append(Contents[0])
Final.append(Contents[1])
Final.append(Content_String)

#print(Content_String)

json_dict = dict(zip(Headers, Final))
print(json_dict["Content"])
json_dict=json.dumps(json_dict)


#print(json_dict)
fo.close()
