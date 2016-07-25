import json
import urllib2
from unidecode import unidecode

# For filtering string of unicode, and prepare for printing
def to_string(word):
    if isinstance(word, unicode) and word:
        return str(unidecode(word))
    else:
        return str(word)

# Uses Google Maps API to return missing GeoLocation Data
def backup_latlng(lat, long):
    google_city = None
    google_postal = None
    rev_latlng = urllib2.urlopen('http://maps.googleapis.com/maps/api/geocode/json?latlng=' + str(lat) + ',' + str(long) + '&sensor=true').read()
    latlng_json = json.loads(rev_latlng)

    city_found = False
    for results in latlng_json["results"]:
        if city_found:
            break
        for address in results["address_components"]:
            if city_found:
                break
            elif "locality" in address["types"]:
                google_city = address["long_name"]
                city_found = True
            elif "administrative_area_level_3" in address["types"]:
                google_city = address["long_name"]
                city_found = True
            elif "administrative_area_level_2" in address["types"]:
                google_city = address["long_name"]
                city_found = True
            elif "administrative_area_level_1" in address["types"]:
                google_city = address["long_name"]
                city_found = True
            else:
                google_city = "Unknown"

    postal_found = False
    for results in latlng_json["results"]:
        if postal_found:
            break
        for address in results["address_components"]:
            if postal_found:
                break
            elif "postal_code" in address["types"]:
                google_postal = address["long_name"]
                postal_found = True
            else:
                google_postal = "0000"

    google_info = {
        'city': to_string(google_city),
        'postal': to_string(google_postal)
    }

    return google_info

#backup_latlng('30.0355', '31.223')
#backup_latlng('41.7038','-73.9218')