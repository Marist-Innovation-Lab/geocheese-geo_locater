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

    isp_data = urllib2.urlopen('https://www.whoismyisp.org/ip/' + my_ip).read()
    clean_isp_data = BeautifulSoup(isp_data).text
    # print(clean_isp_data)

    isp_name = re.findall('Who\sis\smy\sISP\?(.*)The\sInternet\s', clean_isp_data)
    isp_host = re.findall('this\sIP\sis\'(.*)\'\.Other', clean_isp_data)
    isp_ip = re.findall('IP\saddress\sis(\d+.\d+.\d+.\d+).\sThis', clean_isp_data)

    isp_info2 = {
        'name': to_string(isp_name[0]),
        'host': to_string(isp_host[0]),
        'ip': to_string(isp_ip[0])
    }

    return isp_info2

#query_("114.149.196.91")