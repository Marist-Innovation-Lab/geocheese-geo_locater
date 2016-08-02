import gzip
import glob
import os.path
import urllib2
import sys

dir = "./"

# Main function to call all others
def main():
    try:
        if get_hash():
            get_file()
            extract_file()
            print("Successfully acquired latest version of GeoLite2-City.mmdb...\n")
        else:
            print("All files up-to-date, no download needed...\n")
    except:
        error = sys.exc_info()[0]
        print("Error: " + str(error))
        print("Main function failed, retrying function...")
        main()

# Get GeoLite2-City.mmdb Hash
def get_hash():
    try:
        current_hash = open(dir + 'GeoLite2-City.mmdb md5 Hash.txt').read()
        print("Current Hash: " + current_hash)
        online_hash = urllib2.urlopen('http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.md5').read()
        print("Online Hash: " + online_hash + "\n")

        if current_hash == online_hash:
            print("Your current GeoLite2-City.mmdb is up-to-date...\n")
            return False
        else:
            print("Your file is out of date...\n")
            hash_file = open(dir + 'GeoLite2-City.mmdb md5 Hash.txt', 'w+')
            hash_file.write(online_hash)
            return True
    except:
        error = sys.exc_info()[0]
        print("Error: " + str(error))
        print("Failed to retrieve and/or compare hash...")

# Gets the latest GeoLite2-City.mmdb file from MaxMind
def get_file():
    try:
        print("Downloading new GeoLite2-City.mmdb.gz...")

        file = urllib2.urlopen('http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz')
        data = file.read()
        with open(dir + "GeoLite2-City.mmdb.gz", "wb") as code:
            code.write(data)

    except:
        error = sys.exc_info()[0]
        print("Error: " + str(error))
        print("Failed to retrieve GeoLite2-City.mmdb...")

# Extracts GeoLite2-City.mmdb file to replace the current older file
def extract_file():
    try:
        print("Extracting GeoLite2-City.mmdb...")

        for src_name in glob.glob(os.path.join(dir, '*.gz')):
            base = os.path.basename(src_name)
            dest_name = os.path.join(dir, base[:-3])
            with gzip.open(src_name, 'rb') as infile:
                with open(dest_name, 'wb') as outfile:
                    for line in infile:
                        outfile.write(line)

        print("Removing GeoLite2-City.mmdb.gz...")
        print("Updating Hash...\n")
        os.remove(dir + "GeoLite2-City.mmdb.gz")
    except:
        error = sys.exc_info()[0]
        print("Error: " + str(error))
        print("Failed to extract GeoLite2-City.mmdb.gz...")

main()