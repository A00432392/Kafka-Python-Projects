from bs4 import BeautifulSoup
import urllib
from urllib.request import urlopen
import json
import sys 
import re
import datetime
from datetime import date, time, datetime
#from datetime import datetime, date, time
#import mapping as city
import pickle
from dateutil.rrule import rrule, DAILY



BASE_URL="https://booking.kayak.com/flights/"

class Booking(object):
    
    def __init__(self):
        self.url_browse = ""
        self.flights_data = ""
        self.stoppage = ""
        self.arrival_time = ""
        self.trip_json = []
        
        
        
    def browse(self, url="", roundtrip=False):
        print(url)
        try:
            self.url_browse = urllib.request(url)
            
        #except urllib.HTTPError: 
        except:
            print('There was an ERROR')
        fil = open("out.txt","w")
        fil.write(str(self.url_browse))
        fil.close()
        
        
        
    
    def journey_oneway(self, origin, destination, depart_date, adult=1, children=0, infant=0):
        adult = str(adult) if adult >= 1 else "1"
        children = str(children) if children >= 1 else str(children)
        infant = str(infant) if infant >= 1 else str(infant)
        new_url = BASE_URL + origin +"-"+ destination+"/"+depart_date+"/"+adult+"adults/"
        return self.browse(new_url)


    

if __name__== "__main__":
    print
    print("="*30) 
    origin = "YHZ"
    destination = "YTO"
    
    #Range of dates in which we want the data
    a = date(2019, 3, 20)   
    b = date(2019, 3, 24)
    
    
    for dt in rrule(DAILY, dtstart=a, until=b):
        print(dt.strftime("%d-%m-%Y"))
        dept_date = str(dt.strftime("%Y-%m-%d"))
        bro = Booking()
        
        #f1=open('buff.csv', 'a') 
        j_o = bro.journey_oneway(origin,destination,dept_date)
    
  