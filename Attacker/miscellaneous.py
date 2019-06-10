import pygeoip

# Write to log result of attack?


# Map IP
def print_record(target):
    gi = pygeoip.GeoIP('/opt/GeopIP/Geo.dat')
    rec = gi.record_by_name(target)
    city = rec['city']
    region = rec['region_name']
    country = rec['country_name']
    long = rec['longitude']
    lat = rec['latitude']
    print("Target: " + target + "Geo-located.")
    print(str(city) + ', ' + str(region) + ", " + str(country))
    print("Latitude: " + str(lat) + ", Longitude " + str(long))
