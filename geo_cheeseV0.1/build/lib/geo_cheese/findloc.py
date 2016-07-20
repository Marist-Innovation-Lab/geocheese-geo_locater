import xml

import geoip2.database
import geocoder
import re
import json
from urllib2 import urlopen
from unidecode import unidecode
from BeautifulSoup import BeautifulSoup


# For filtering string of unicode, and prepare for printing
def to_string(word):
    if isinstance(word, unicode) and word:
        return str(unidecode(word))
    else:
        return str(word)


# For removing HTML Tags for web scrape
def remove_tags(text):
    return ''.join(xml.etree.ElementTree.fromstring(text).itertext())


def find_loc(mmdb_file, my_ip):
    # Gets user's public IP address to be used by location services
    #my_ip = urlopen('http://ip.42.pl/raw').read()

    # Creates a reader to parse through the database to get information on the IP provided
    reader = geoip2.database.Reader(mmdb_file)
    # Assigns the list of results to a variable to be printed out later.
    response = reader.city(my_ip)

    # Individually assigns list elements to different variables for formatting
    country = response.country.name
    subdivision = response.subdivisions.most_specific.name
    city = response.city.name
    zip = response.postal.code
    lat = response.location.latitude
    long = response.location.longitude

    # Close Database Connection
    reader.close()

    # In case array is empty do backup lookup via lat long
    g = geocoder.google([lat, long], method='reverse')

    if not subdivision:
        subdivision = g.state_long
    if not city:
        city = g.city
    if not zip:
        zip = g.postal

    # Get's ISP Information
    isp_data = urlopen('https://www.whoismyisp.org/ip/' + my_ip).read()
    clean_isp_data = BeautifulSoup(isp_data).text
    #print(clean_isp_data)

    isp_name = re.findall('Who\sis\smy\sISP\?(.*)The\sInternet\s', clean_isp_data)
    isp_host = re.findall('this\sIP\sis\'(.*)\'\.Other', clean_isp_data)
    isp_ip = re.findall('IP\saddress\sis(\d+.\d+.\d+.\d+).\sThis', clean_isp_data)

    if not isp_name or not isp_host or not isp_ip:
        isp_data2 = urlopen('http://ip-api.com/json/' + my_ip).read()
        isp_json = json.loads(isp_data2)

        if not isp_name:
            isp_name = []
            isp_name.append(isp_json['isp'])
        if not isp_host:
            isp_host = []
            isp_host.append("Unknown")
        if not isp_ip:
            isp_ip = []
            isp_ip.append(isp_json['query'])

    # Formats data into a more readable format
    #location = "Country: " + to_string(country) + "\nSubdivision: " + to_string(subdivision) + "\nCity: " + to_string(city) + "\nPostal Code: " + to_string(zip)
    #latlong = "Lat: " + str(lat) + ", Long: " + str(long)
    #isp_info = "ISP Name: " + to_string(isp_name[0]) + "\nISP Host: " + to_string(isp_host[0]) + "\nISP IP: " + to_string(isp_ip[0])

    #print(isp_info)
    #print(location)
    #print(latlong)
    if not country:
        country = 'Unknown'
    
    if not subdivision:
        subdivision = 'Unknown'
    
    if not city:
        city = 'Unknown'
    
    if not zip:
        zip = '0000'
    
    if not lat:
        lat = '0.000'
    
    if not long:
        long = '0.000'
        
    if not isp_name:
        isp_name = ['Unknown']
    
    if not isp_host:
        isp_host = ['Unknown']
        
    if not isp_ip:
        isp_ip = ['0.0.0.0']
    
    location_info = {
        'country': to_string(country),
        'subdivision': to_string(subdivision),
        'city': to_string(city),
        'postal': to_string(zip),
        'lat': str(lat),
        'long': str(long),
        'name': to_string(isp_name[0]),
        'host': to_string(isp_host[0]),
        'ip': to_string(isp_ip[0])
    }
    
    return location_info

#find_loc(raw_input("Target IP: "))

