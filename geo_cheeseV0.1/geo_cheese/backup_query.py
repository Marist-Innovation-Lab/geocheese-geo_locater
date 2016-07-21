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

def query_(my_ip):
    #my_ip = urllib2.urlopen('http://ip.42.pl/raw').read()

    isp_data2 = urllib2.Request('http://whatismyipaddress.com/ip/' + my_ip, headers={'User-Agent': 'Mozilla/5.0'})
    clean_isp_data2 = urllib2.urlopen(isp_data2).read()
    clean_isp_data2 = BeautifulSoup(clean_isp_data2).text

    isp_name = re.findall('ISP:(.*)Organization:', clean_isp_data2)
    isp_host = re.findall('Hostname:(.*)ASN:', clean_isp_data2)
    isp_ip = re.findall('FALSEIP:(\d+.\d+.\d+.\d+)Decimal', clean_isp_data2)

    isp_info2 = {
        'name': to_string(isp_name[0]),
        'host': to_string(isp_host[0]),
        'ip': to_string(isp_ip[0])
    }

    if isp_info2:
        print("Backup Query Successfully retrieved GeoLocation Data")
        print(isp_info2)

    return isp_info2
