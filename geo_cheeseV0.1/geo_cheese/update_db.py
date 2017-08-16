import gzip
import glob
import os.path
import urllib3
import sys
import shutil
import re

hash_dir = "./local_dbs/dbs_hash/"
dir = "./local_dbs/"

# Main function to call all others
def main():
    try:
        if get_geo_hash():
            get_geo_file()
            extract_geo_file()
            print("Successfully acquired latest version of GeoLite2-City.mmdb...\n")
        else:
            print("GeoLite2-City.mmdb is up-to-date, no download needed...\n")
    except:
        error = sys.exc_info()[0]
        print("Error: " + str(error))
        print("Main function failed, retrying function...")
        main()

    try:
        if check_asn_ver():
            get_asn_file()
            print("Successfully acquired latest version of asnames.json...\n")
        else:
            print("asnames.json is up-to-date, no download needed...\n")
    except:
        error = sys.exc_info()[0]
        print("Error: " + str(error))
        print("Main function failed, retrying function...")
        main()

    # DEPRECATED
    '''try:
        if check_ipasn_ver():
            get_ipasn_file()
            print("Successfully acquired latest version of ipasn_20140513.dat...\n")
        else:
            print("ipasn_20140513.dat is up-to-date, no download needed...\n")
    except:
        error = sys.exc_info()[0]
        print("Error: " + str(error))
        print("Main function failed, retrying function...")
        main()'''

# Get GeoLite2-City.mmdb Hash
def get_geo_hash():
    try:
        # Reading Stored Database Hash
        print("Checking GeoLite2-City.mmdb...")
        current_hash = open(hash_dir + 'GeoLite2-City.mmdb md5 Hash.txt').read()
        print("Current Hash: " + current_hash)

        # Retrieving Online Database Hash
        http = urllib3.PoolManager()
        url = 'http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.md5'
        response = http.request('GET', url)
        online_hash = response.data
        print("Online Hash: " + online_hash + "\n")

        if current_hash == online_hash:
            print("Your current GeoLite2-City.mmdb is up-to-date...\n")
            return False
        else:
            print("Your file is out of date...\n")
            hash_file = open(hash_dir + 'GeoLite2-City.mmdb md5 Hash.txt', 'w+')
            hash_file.write(online_hash)
            return True
    except:
        error = sys.exc_info()[0]
        print("Error: " + str(error))
        print("Failed to retrieve and/or compare hash...")

# Gets the latest GeoLite2-City.mmdb file from MaxMind
def get_geo_file():
    try:
        print("Downloading new GeoLite2-City.mmdb.gz...")
        http = urllib3.PoolManager()
        url = 'http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz'
        r = http.request('GET', url, preload_content=False)
        with open(dir + "GeoLite2-City.mmdb.gz", 'wb') as out:
            while True:
                print("Writing GeoLite2-City.mmdb.gz file...")
                data = r.read()
                if not data:
                    break
                out.write(data)
        r.release_conn()
        print("Finished downloading new GeoLite2-City.mmdb.gz...")
    except:
        error = sys.exc_info()[0]
        print("Error: " + str(error))
        print("Failed to retrieve GeoLite2-City.mmdb...")

# Extracts GeoLite2-City.mmdb file to replace the current older file
def extract_geo_file():
    try:
        print("Extracting GeoLite2-City.mmdb...")

        for src_name in glob.glob(os.path.join(dir, '*.gz')):
            base = os.path.basename(src_name)
            dest_name = os.path.join(dir, base[:-3])
            temp_name = os.path.join(dir, 'Temp.mmdb')
            with gzip.open(src_name, 'rb') as infile:
                with open(temp_name, 'wb') as outfile:
                    for line in infile:
                        outfile.write(line)
        shutil.copy(dir + "Temp.mmdb", dir + "GeoLite2-City.mmdb")

        print("Removing GeoLite2-City.mmdb.gz...")
        print("Updating Hash...\n")
        os.remove(dir + "GeoLite2-City.mmdb.gz")
        os.remove(dir + "Temp.mmdb")
    except:
        error = sys.exc_info()[0]
        print("Error: " + str(error))
        print("Failed to extract GeoLite2-City.mmdb.gz...")

# Get asnames.json hash from GitHub
def check_asn_ver():
    try:
        print("Checking asnames.json...")
        # Get hash for current version of the ASN Database
        cur_ver_num = open(hash_dir + "asnames.json Hash.txt").read()
        print("Current Hash: " + cur_ver_num)

        # Get online hash for ASN Database
        http = urllib3.PoolManager()
        url = 'https://github.com/hadiasghari/pyasn/blob/master/data/asnames.json'
        response = http.request('GET', url)
        on_ver_num = response.data
        on_ver_num = re.findall('<a class="commit-tease-sha"\s.*x>\s+(\w+)\s+</a>', on_ver_num)
        on_ver_num = on_ver_num[0].strip()
        print("Online Hash: " + on_ver_num + "\n")

        if cur_ver_num == on_ver_num:
            print("Your current asnames.json is up-to-date...\n")
            return False
        else:
            print("Your file is out of date...\n")
            hash_file = open(hash_dir + 'asnames.json Hash.txt', 'w+')
            hash_file.write(on_ver_num)
            return True
    except:
        error = sys.exc_info()[0]
        print("Error: " + str(error))
        print("Failed to retrieve and/or compare hash...")

# Gets the latest asnames.json file from GitHub
def get_asn_file():
    try:
        print("Downloading new asnames.json...")
        http = urllib3.PoolManager()
        url = 'https://raw.githubusercontent.com/hadiasghari/pyasn/master/data/asnames.json'
        r = http.request('GET', url, preload_content=False)
        with open(dir + "asnames-temp.json", 'wb') as out:
            while True:
                print("Writing new asnames.json...")
                data = r.read()
                if not data:
                    break
                out.write(data)
        r.release_conn()
        print("Finished downloading new asnames.json...")
        shutil.copy(dir + "asnames-temp.json", dir + "asnames.json")
        os.remove(dir + "asnames-temp.json")
        print("Updating Hash...\n")
    except:
        error = sys.exc_info()[0]
        print("Error: " + str(error))
        print("Failed to retrieve asnames.json...")

# Get ipasn_20140513.dat hash from GitHub - DEPRECATED
'''def check_ipasn_ver():
    try:
        print("Checking ipasn_20140513.dat...")
        # Get hash for current version of the IPASN Database
        cur_ver_num = open(hash_dir + "ipasn_20140513.dat Hash.txt").read()
        print("Current Hash: " + cur_ver_num)

        # Get online hash for ASN Database
        on_ver = urllib2.Request('https://github.com/hadiasghari/pyasn/blob/master/data/ipasn_20140513.dat')
        on_ver_num = urllib2.urlopen(on_ver).read().replace("\n", "")
        on_ver_num = re.findall('<a class="commit-tease-sha"\s.*x>\s+(\w+)\s+</a>', on_ver_num)
        on_ver_num = on_ver_num[0].strip()
        print("Online Hash: " + on_ver_num + "\n")

        if cur_ver_num == on_ver_num:
            print("Your current ipasn_20140513.dat is up-to-date...\n")
            return False
        else:
            print("Your file is out of date...\n")
            hash_file = open(hash_dir + 'ipasn_20140513.dat Hash.txt', 'w+')
            hash_file.write(on_ver_num)
            return True
    except:
        error = sys.exc_info()[0]
        print("Error: " + str(error))
        print("Failed to retrieve and/or compare hash...")

# Gets the latest ipasn_20140513.dat  file from GitHub
def get_ipasn_file():
    try:
        print("Downloading new ipasn_20140513.dat...")

        file = urllib2.urlopen('https://raw.githubusercontent.com/hadiasghari/pyasn/master/data/ipasn_20140513.dat')
        data = file.read()
        with open(dir + "ipasn_20140513-temp.dat", "wb") as code:
            code.write(data)
        shutil.copy(dir + "ipasn_20140513-temp.dat", dir + "ipasn_20140513.dat")

        os.remove(dir + "ipasn_20140513-temp.dat")
        print("Updating Hash...\n")

    except:
        error = sys.exc_info()[0]
        print("Error: " + str(error))
        print("Failed to retrieve ipasn_20140513.dat...")'''

#main()