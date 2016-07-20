import re
import xml
import urllib2
from unidecode import unidecode
from BeautifulSoup import BeautifulSoup

# For filtering string of unicode, and prepare for printing
def to_string(word):
    if isinstance(word, unicode) and word:
        return str(unidecode(word))
    else:
        return str(word)

def query():
    my_ip = urllib2.urlopen('http://ip.42.pl/raw').read()

    isp_data2 = urllib2.Request('http://whatismyipaddress.com/ip/' + my_ip, headers={'User-Agent': 'Mozilla/5.0'})
    clean_isp_data2 = urllib2.urlopen(isp_data2).read()
    clean_isp_data2 = BeautifulSoup(clean_isp_data2).text

    isp_name = re.findall('ISP:(.*)Organization:', clean_isp_data2)
    isp_host = re.findall('Hostname:(.*)ASN:', clean_isp_data2)
    isp_ip = re.findall('FALSEIP:(\d+.\d+.\d+.\d+)Decimal', clean_isp_data2)

    isp_country = re.findall('Country:(.*)State/Region:', clean_isp_data2)
    isp_subdiv = re.findall('State/Region:(.*)City:', clean_isp_data2)
    isp_city = re.findall('City:(.*)Latitude:', clean_isp_data2)

    isp_lat = re.findall('Latitude:(\-?\d+\.\d+).*\(', clean_isp_data2)
    isp_long = re.findall('Longitude:(\-?\d+\.\d+).*\(', clean_isp_data2)

    print("ISP Name: " + to_string(isp_name[0]))
    print("ISP Host: " + to_string(isp_host[0]))
    print("ISP IP: " + to_string(isp_ip[0]))

    print("Country: " + to_string(isp_country[0]))
    print("Subdivision: " + to_string(isp_subdiv[0]))
    print("City: " + to_string(isp_city[0]))

    print("Lat: " + to_string(isp_lat[0]) + ", " + "Long: " + to_string(isp_long[0]))

query()