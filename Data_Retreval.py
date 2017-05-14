"""
API methods for getitng, extracting GTFS data and exporting results.

by Arnold Valdez
"""

import json
import urllib
import urllib2
import point
import zipfile
import csv
import os


 

def GetLocations(key):

    """
    Gets locations with GTFS data
    Input
       
       key : your API Key
    Output
       dictionary with code(key) and geography(value)
    """

    data = {}
    data['key'] = key
    url_values = urllib.urlencode(data)


    base = "https://api.transitfeeds.com/v1/getLocations"
    full_url = base + '?' + url_values
    js = urllib2.urlopen(full_url)
    data = json.load(js)
   
    d= data['results']['locations']
    return d






def ShowStates(locaData):

    """
    Displays states with GTFS data
           
       locaData : location dictionary from GetLocations()
    Output
       dictionary with state code(key) and geography(value)
    """
    
    for k in locaData:
        if (k["pid"] == 31):
            print "{: <4} {}".format(k["id"], k["t"])



def ShowCity(cityPID, localData):

    """
    Displays cities with GTFS data

       cityPID: state code
       locaData : location dictionary from GetLocations()
       
    Output
       dictionary with city code(key) and geography(value)
    """
    
    for k in localData:
        if (k["pid"] == cityPID):
            print "{: <4} {}".format(k["id"], k["t"])

def ShowAgencyFeeds(key,locID):
    """
    Displays agency with GTFS feeds

       locID: city code
       key : API key
       
    Output
       dictionary with feed code(key) and feed name(value)
    """
    data = {}
    data['key'] = key
    data['location'] = locID
    data['page'] = 1
    data['limit'] = 50
    data['type'] = 'gtfs'    
    url_values = urllib.urlencode(data)


    base = "https://api.transitfeeds.com/v1/getFeeds"
    full_url = base + '?' + url_values
    js = urllib2.urlopen(full_url)
    result = json.load(js)
   
    d = result['results']['feeds']
    i = 0
    for k in d:
        i = i+1
        print "{} {}".format(i, k["t"])
    return result

def GetGTFS(key,d, num):

    """
    Downloads GTFS data

       key : API key
       d : output from ShowAgencyFeeds(key,locID)
       num : feed code
    Output
       dictionary with city code(key) and geography(value)
    """
    
    i = int(num) -1
    feedID = d['results']['feeds'][0]['id']
    
    data = {}
    data['key'] = key
    data['feed'] = feedID
    url_values = urllib.urlencode(data)


    base = "https://api.transitfeeds.com/v1/getLatestFeedVersion"
    full_url = base + '?' + url_values
    urllib.urlretrieve(full_url, "GTFS.zip")
    


def ExtractStops():
    """
    Extracts the stops.txt from GTFS data

       
    Output
       dict_list : dictionary with stopID, Lat, Lon
       max(seqX),max(seqY),min(seqX),min(seqY) :
           Cordinates indicating geograpic extent of stops
    """
    
    zipOb = zipfile.ZipFile("GTFS.zip")
    zipOb.extract("stops.txt","resource/")
    zipOb.close()
   

    reader = csv.DictReader(open("resource/stops.txt", 'rb'))
    dict_list = []
    for line in reader:
        dict_list.append(line)

    seqX = [x['stop_lon'] for x in dict_list]
    
    

    seqY = [y['stop_lat'] for y in dict_list]
    min(seqY)
    max(seqY)

   
    os.remove("GTFS.zip")
    
           
    return dict_list,max(seqX),max(seqY),min(seqX),min(seqY)
    
def Dict2CSV(filepath,my_dict):

    """
    Saves dictionary as CSV file

    filepath : file path for saved file
    my_dict : dictionary to b converted
       
    Output
       CSV file
    """
    
    
    failed = True
    while failed:
        try:
            myfile = open(filepath,'wb')
            with myfile:
                w = csv.writer(myfile)
                w.writerow(["Stop_ID","GEOID"])
                w.writerows(my_dict.items())
                failed = False
        
        except IOError:
            print "WARNING!!! The JointResult.csv file might be still open please close it."
            raw_input("Press enter when file is closed")

    
       
        
    
            

