#Gets local timezone and stores in /config/timezone

import geocoder

g = geocoder.ip('me')
timezone = g.geojson['features'][0]['properties']['raw']['timezone']

f = open("/config/timezone.h", "w")

print >>f, "char local_tz[30] = \"" + timezone + "\";"

