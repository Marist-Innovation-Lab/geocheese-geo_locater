import re
import xml
import urllib3
import json
from unidecode import unidecode
from BeautifulSoup import BeautifulSoup
from pprint import pprint

# For filtering string of unicode, and prepare for printing
def to_string(word):
    if isinstance(word, unicode) and word:
        return str(unidecode(word))
    else:
        return str(word)

def query_(my_ip):
    try:
        http = urllib3.PoolManager()
        url = 'https://www.whoismyisp.org/ip/' + my_ip
        response = http.request('GET', url)
        isp_data = response.data
        clean_isp_data = BeautifulSoup(isp_data).text
        # print(clean_isp_data)

        isp_name = re.findall('Who\sis\smy\sISP\?(.*)The\sInternet\s', clean_isp_data)
        isp_host = re.findall('this\sIP\sis\'(.*)\'\.Other', clean_isp_data)
        isp_ip = re.findall('IP\saddress\sis(\d+.\d+.\d+.\d+)\.\s', clean_isp_data)

        if not isp_name:
            isp_name = None
        if not isp_host:
            isp_host = None
        if not isp_ip:
            isp_ip = None

        isp_info2 = {
            'name': isp_name[0],
            'host': isp_host[0],
            'ip': isp_ip[0]
        }

    except:
        isp_info2 = {
            'name': None,
            'host': None,
            'ip': None
        }

        print("Backup query failed or Connection Rejected...")

    return isp_info2

def get_asn(my_ip):
    try:
        # Initialize module and load IP to ASN database
        # the sample database can be downloaded or built - see below
        with open('local_dbs/ipasn.json') as asn_db:
            ip_asn = json.load(asn_db)
        with open('local_dbs/asnames.json') as asn_host:
            asn_name = json.load(asn_host)
        isp_asn = ip_asn[str(my_ip)]
        isp_name = asn_name[str(isp_asn)]

        if not isp_asn:
            isp_asn = None
        if not isp_name:
            isp_name = None

        isp_info = {
            'isp_asn': isp_asn,
            'isp_name': isp_name
        }

    except:
        print("IP Address is not in local ASN Database...")
        isp_info = {
            'isp_asn': None,
            'isp_name': None
        }

    return isp_info

#print(query_("166.193.75.232"))
#print(get_asn("159.66.242.0"))