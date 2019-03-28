#!/usr/bin/python
import uuid
import sys
import fileinput
from time import time, sleep
from random import randint
import datetime
from datetime import date, time, datetime
import datetime
import json
import requests
from lxml import html
from collections import OrderedDict
import argparse
import pickle
from dateutil.rrule import rrule, DAILY


def parse(source, destination, date, delta):
        try:
            url = "https://www.expedia.com/Flights-Search?trip=oneway&leg1=from:{0},to:{1},departure:{2}TANYT&passengers=adults:1,children:0,seniors:0,infantinlap:Y&options=cabinclass%3Aeconomy&mode=search&origref=www.expedia.com".format(source, destination, date)
            #print(url)
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
            response = requests.get(url, headers=headers, verify=False)
            
           
            
            parser = html.fromstring(response.text)
            json_data_xpath = parser.xpath("//script[@id='cachedResultsJson']//text()")
            
            raw_json = json.loads(json_data_xpath[0] if json_data_xpath else '')
            
            
            flight_data = json.loads(raw_json["content"])

            flight_info = OrderedDict() 
            lists = []

            for i in flight_data['legs'].keys():
                total_distance = flight_data['legs'][i].get("formattedDistance", '')
                exact_price = flight_data['legs'][i].get('price', {}).get('totalPriceAsDecimal', '')

                departure_location_airport = flight_data['legs'][i].get('departureLocation', {}).get('airportLongName', '')
                departure_location_city = flight_data['legs'][i].get('departureLocation', {}).get('airportCity', '')
                departure_location_airport_code = flight_data['legs'][i].get('departureLocation', {}).get('airportCode', '')
                
                arrival_location_airport = flight_data['legs'][i].get('arrivalLocation', {}).get('airportLongName', '')
                arrival_location_airport_code = flight_data['legs'][i].get('arrivalLocation', {}).get('airportCode', '')
                arrival_location_city = flight_data['legs'][i].get('arrivalLocation', {}).get('airportCity', '')
                airline_name = flight_data['legs'][i].get('carrierSummary', {}).get('airlineName', '')
                
                no_of_stops = flight_data['legs'][i].get("stops", "")
                flight_duration = flight_data['legs'][i].get('duration', {})
                flight_hour = flight_duration.get('hours', '')
                flight_minutes = flight_duration.get('minutes', '')
                flight_days = flight_duration.get('numOfDays', '')

                if no_of_stops == 0:
                    stop = "Nonstop"
                else:
                    stop = str(no_of_stops) + ' Stop'

                total_flight_duration = "{0} days {1} hours {2} minutes".format(flight_days, flight_hour, flight_minutes)
                departure = departure_location_city
                arrival = arrival_location_city
                carrier = flight_data['legs'][i].get('timeline', [])[0].get('carrier', {})
                plane = carrier.get('plane', '')
                plane_code = carrier.get('planeCode', '')
                formatted_price = "{0:.2f}".format(exact_price)

                if not airline_name:
                    airline_name = carrier.get('operatedBy', '')
                today = datetime.datetime.today().strftime("%m/%d/%Y %H:%M")
                
                timings = []
                #print("Size of list before for loop"+str(len(timings)))
                for timeline in  flight_data['legs'][i].get('timeline', {}):
                    if 'departureAirport' in timeline.keys():
                        departure_airport = timeline['departureAirport'].get('longName', '')
                        
                        departure_time = timeline['departureTime'].get('time', '')
                        
                        departure_time = datetime.datetime.strptime(departure_time, "%I:%M%p")
                        departure_time= str(departure_time.strftime("%H:%M"))
                        
                        arrival_airport = timeline.get('arrivalAirport', {}).get('longName', '')
                        arrival_time = timeline.get('arrivalTime', {}).get('time', '')
                        
                        flight_timing = {
                                            'departure_airport':departure_airport,
                                            'departure_date':date,
                                            'departure_time':departure_time,
                                            'arrival_airport':arrival_airport,
                                            'arrival_time':arrival_time
                        }
                        timings.append(flight_timing)
                    
                
                dep_time = str(timings[0]['departure_date'])+" "+str(timings[0]['departure_time'])
                hours_to_departure = calculate_hours(today, dep_time)
                    
                flight_info = {'stops':stop,
                    'ticket_price':formatted_price,
                    'days_to_departure': delta,
                    'hours_to_departure':str(hours_to_departure),
                    'date_of_extraction' : str(today),
                    'departure':departure,
                    'arrival':arrival,
                    'flight_duration':total_flight_duration,
                    'airline':airline_name,
                    'plane':plane,
                    'timings':timings,
                    'plane_code':plane_code,
                    'id': str(uuid.uuid4())
                }
                lists.append(flight_info)
            sortedlist = sorted(lists, key=lambda k: k['ticket_price'], reverse=False)
            return sortedlist
        
        except Exception as e:
            print(repr(e))
            
def calculate_hours(extraction_time, departure_time):
    
    
    #set the date and time format
    date_format = "%m/%d/%Y %H:%M"
    
    #set the format
    extraction_time  = datetime.datetime.strptime(extraction_time, date_format)
    dep_time  = datetime.datetime.strptime(departure_time, date_format)
                
    diff= dep_time-extraction_time
               
    #print days
    days = diff.days
 
    #print overall hours
    days_to_hours = days * 24
    diff_btw_two_times = (diff.seconds) / 3600
    overall_hours = days_to_hours + diff_btw_two_times
    hours_to_departure = round(overall_hours,2)
    
    return hours_to_departure;

def replace(file):
    searchExp = "]["
    replaceExp = "   ,"
    for line in fileinput.input(file, inplace=True):
        if searchExp in line:
            line = line.replace(searchExp, replaceExp)
        sys.stdout.write(line)
        
def beautify(file):
    with open(file) as f:
        json_string = f.read()
    try:
        parsed_json = json.loads(json_string)
        formatted_json = json.dumps(parsed_json, indent = 4,sort_keys=True)
        with open("%s" % (file) , "w") as f:
            f.write(formatted_json)
    except Exception as e:
        print(repr(e))

if __name__ == "__main__":
    
    source = "yhz"
    dest_list = ['yto', 'yul', 'yyt', 'yow', 'yyc', 'yhm', 'lhr', 'yqy']
    #dest_list = ['yto']
    today = datetime.datetime.today().strftime("%m_%d")
    day = datetime.datetime.today()
    # Range of dates in which we want the data
    a = date(2019, 3, 29)   
    b = date(2019, 6, 30)
    
    for destination in dest_list:
        sleep(randint(0,5))
        for dt in rrule(DAILY, dtstart=a, until=b):
            delta=dt-day
            delta=delta.days
            sleep(randint(0,3))
            dept_date = str(dt.strftime("%m/%d/%Y"))
            print ("Fetching flight details for route "+source +" - "+destination+ " of "+ dept_date )
            scraped_data = parse(source, destination, dept_date,delta)
            
            print ("Writing " + source + "-" + destination +" for date "+dept_date+ " data to output file")
            if scraped_data is not None:
                with open('Results\\%s-%s-flight-results.json' % (source, str(today)), 'a+') as fp:
                    json.dump(scraped_data, fp, indent=4)     
    file="Results\\"+str(source)+"-"+str(today)+"-flight-results.json"  
    replace(file)
    beautify(file)
    print("bye")
