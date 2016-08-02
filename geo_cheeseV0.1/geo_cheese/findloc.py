import xml
import backup_query as backup
import reverse_latlng_google as reverse_g
import random_ip
import geoip2.database
import geocoder
import re
import json
import urllib2
import sys
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

# Main function to retrieve GeoISP data about target IP address
def find_loc(mmdb_file, my_ip):

    # Declare GeoLocation Variables
    country = None
    subdivision = None
    city = None
    zip = None
    lat = None
    long = None

    # Declare ISP Variables
    isp_asn = None
    isp_name = None
    isp_host = None
    isp_ip = None

    print("Target IP: " + my_ip)
    try:
        print("Retrieving basic geolocation data from GeoLite2-City.mmdb...")
        # Gets user's public IP address to be used by location services
        # my_ip = urlopen('http://ip.42.pl/raw').read()

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

        print("Basic geolocation data retrieved from GeoLite2-City.mmdb...\n")
    except:
        print("Failed to retrieve data from GeoLite2-City.mmdb...")
        print("IP Address is invalid " + str(my_ip) + "\n")

    # In case array is empty do backup lookup via lat long
    if not subdivision or not city or not zip:
        try:
            print("Some geolocation data is still missing, running geocoder...")
            g = geocoder.google([lat, long], method='reverse')

            if not subdivision:
                subdivision = g.state_long
            if not city:
                city = g.city
            if not zip:
                zip = g.postal

            print("Successfully retrieved missing geolocation data from geocoder...\n")
        except:
            error = sys.exc_info()[0]
            print("Error: " + str(error))
            print("Geocoder failed to properly retrieve data...\n")

    # In case array is still empty use online Google Maps API to retrieve all avaliable information
    if not subdivision or not city or not zip:
        try:
            print("Some geolocation data is still missing, querying Online Google Maps API...")
            back_geo = reverse_g.backup_latlng(lat, long)

            if not city:
                city = back_geo['city']
            if not subdivision:
                subdivision = back_geo['sublocality']
            if not zip:
                zip = back_geo['postal']

            print("Successfully retrieved missing geolocation data from Online Google Maps API...\n")
        except:
            error = sys.exc_info()[0]
            print("Error: " + str(error))
            print("Failure to open Google Maps API or connection rejected...\n")

    # Get's ISP Information
    try:
        print("Retrieving ISP Data...")
        isp_data2 = urllib2.Request('http://whatismyipaddress.com/ip/' + my_ip, headers={'User-Agent': 'Mozilla/5.0'})
        clean_isp_data2 = urllib2.urlopen(isp_data2).read()
        clean_isp_data2 = BeautifulSoup(clean_isp_data2).text
        #print(clean_isp_data2)

        isp_name = re.findall('ISP:(.*)Organization:', clean_isp_data2)
        isp_host = re.findall('Hostname:(.*)ASN:', clean_isp_data2)
        isp_asn = re.findall('ASN:(\d+)ISP:', clean_isp_data2)
        isp_ip = re.findall('FALSEIP:(\d+.\d+.\d+.\d+)Decimal', clean_isp_data2)

        if isp_name:
            print("isp_name acquired from WhatIsMyIPAddress...")
        if isp_host:
            print("isp_host acquired from WhatIsMyIPAddress...")
        if isp_asn:
            print("isp_asn acquired from WhatIsMyIPAddress...")
        if isp_ip:
            print("isp_ip acquired from WhatIsMyIPAddress...")

        print("Successfully retrieved ISP data from WhatIsMyIPAddress...\n")
    except:
        error = sys.exc_info()[0]
        print("Error: " + str(error))
        print("Failure to open WhatIsMyIPAddress or connection rejected...\n")

    # Backup Query in case data is still missing
    if not isp_ip or not isp_host or not isp_name or not isp_asn:
        try:
            print("Some ISP data is missing, running backup query...")
            isp_info2 = backup.query_(my_ip)
            isp_local_data = backup.get_asn(my_ip)

            if not isp_ip and isp_info2['ip'] != None:
                isp_ip = []
                isp_ip.append(isp_info2['ip'])
                if isp_ip and isp_ip != []:
                    print("isp_ip acquired from WhoIsMyISP...")
            if not isp_host and isp_info2['host'] != None:
                isp_host = []
                isp_host.append(isp_info2['host'])
                if isp_host and isp_host != []:
                    print("isp_host acquired from WhoIsMyISP...")
            if not isp_name and isp_info2['name'] != None:
                isp_name = []
                isp_name.append(isp_info2['name'])
                if isp_name and isp_name != []:
                    print("isp_name acquired from WhoIsMyISP...")

            print("Querying local database for ISP ASN and Name...")
            try:
                if not isp_asn and isp_local_data['isp_asn'] != None:
                    print("isp_asn acquired from local database...")
                    isp_asn = []
                    isp_asn.append(isp_local_data['isp_asn'])
                if not isp_name and isp_local_data['isp_name'] != None:
                    print("isp_name acquired from local database...")
                    isp_name = []
                    isp_name.append(isp_local_data['isp_name'])
            except:
                print("Local database failed to return values...")

            print("Backup query successfully retrieved missing ISP data...\n")
        except:
            error = sys.exc_info()[0]
            print("Error: " + str(error))
            print("Backup query failed to retrieve ISP data...\n")

    if not isp_name or not isp_host or not isp_asn or not isp_ip:
        try:
            print("Some ISP data is missing, retrieving information from ipinfo.io...")
            isp_data3 = urllib2.urlopen('http://ipinfo.io/' + str(my_ip) + '/json').read()
            isp_data3_json = json.loads(isp_data3)

            if not isp_host:
                isp_host = []
                if isp_data3_json['hostname'] != "No Hostname":
                    isp_host.append(isp_data3_json['hostname'])
                if isp_host and isp_host != []:
                    print("isp_host acquired from ipinfo.io...")
            if not isp_asn:
                isp_asn = re.findall('AS(\d+)\s', isp_data3_json['org'])
                if isp_asn and isp_asn != []:
                    print("isp_asn acquired from ipinfo.io...")
            if not isp_name:
                isp_name = re.findall('AS\d+\s(.*)', isp_data3_json['org'])
                if isp_name and isp_name != []:
                    print("isp_name acquired from ipinfo.io...")
            if not isp_ip:
                isp_ip = []
                isp_ip.append(isp_data3_json['ip'])
                if isp_ip and isp_ip != []:
                    print("isp_ip acquired from ipinfo.io...")

            print("Successfully retrieved ISP information from ipinfo.io...\n")
        except:
            error = sys.exc_info()[0]
            print("Error: " + str(error))
            print("Failure to open ipinfo.io or connection rejected...\n")

    if not isp_name or not isp_asn or not isp_ip:
        try:
            print("Some ISP data is missing, retrieving information from ip-api.com...")
            isp_data2 = urllib2.urlopen('http://ip-api.com/json/' + my_ip).read()
            isp_json = json.loads(isp_data2)
            #print(isp_json)

            if not isp_name:
                isp_name = []
                isp_name.append(isp_json['isp'])
                print("isp_name acquired from ip-api.com...")
            if not isp_asn:
                isp_asn = re.findall('AS(\d+)\s', isp_json['as'])
                if isp_asn[0] != "0000":
                    print("isp_asn acquired from ip-api.com...")
            if not isp_ip:
                isp_ip = []
                isp_ip.append(isp_json['query'])
                print("isp_ip acquired from ip-api.com...")

            print("Successfully retrieved ISP information from ip-api.com...\n")
        except:
            error = sys.exc_info()[0]
            print("Error: " + str(error))
            print("Failure to open ip-api.com or connection rejected...\n")

    # Assigns default values in case data is found to be missing
    if not country or country == None or country == "None":
        country = 'Unknown'

    if not subdivision or subdivision == None or subdivision == "None":
        subdivision = 'Unknown'

    if not city or city == "None":
        city = 'Unknown'

    if not zip or zip == "None":
        zip = '0000'

    if not lat or lat == "None":
        lat = '0.000'

    if not long or long == "None":
        long = '0.000'

    if not isp_name or isp_name[0]  == "None":
        isp_name = ['Unknown']

    if not isp_host or isp_host[0] == "None":
        isp_host = ['Unknown']

    if not isp_asn or isp_asn[0] == "None":
        isp_asn = ['0000']

    if not isp_ip or isp_ip[0] == "None":
        isp_ip = ['0.0.0.0']

    location_info = {
        'country': to_string(country),
        'subdivision': to_string(subdivision),
        'city': to_string(city),
        'postal': to_string(zip),
        'lat': str(lat),
        'long': str(long),
        'name': to_string(isp_name[0]),
        'ASN': str(isp_asn[0]),
        'host': to_string(isp_host[0]),
        'ip': to_string(isp_ip[0])
    }

    if location_info:
        if 'Unknown' in location_info.values() or '0.0.0.0' in location_info.values() or '0000' in location_info.values() or 'None' in location_info.values():
            print("Data may not be avaliable or Error may have occured")
            print("Incomplete GeoISP Data acquired - " + my_ip)
            print(location_info)
            print(" ")
        else:
            print("Successfully obtained GeoISP Data - " + my_ip)
            print(location_info)
            print(" ")

    else:
        location_info = {
            'country': 'Unknown',
            'subdivision': 'Unknown',
            'city': 'Unknown',
            'postal': '0000',
            'lat': '0.000',
            'long': '0.000',
            'name': 'Unknown',
            'ASN': '0000',
            'host': 'Unknown',
            'ip': '0.0.0.0'
        }

        error = sys.exc_info()[0]
        print("Error: " + str(error))
        print("Failed to obtain GeoISP Data\n")

    return location_info

#for x in xrange(10):
#    print(x + 1)
#    find_loc("local_dbs/GeoLite2-City.mmdb", random_ip.rand_ip())
#find_loc("local_dbs/GeoLite2-City.mmdb", '243.63.89.86') # Invalid IP for Testing
#find_loc("local_dbs/GeoLite2-City.mmdb", "176.245.154.188")
#find_loc("local_dbs/GeoLite2-City.mmdb", random_ip.rand_ip())
#get_asn("166.193.75.232")