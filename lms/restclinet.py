import urllib
import urllib2
import base64

url = "http://127.0.0.1:5000"
authKey = base64.b64encode("username:password")
headers = {"Content-Type":"application/json", "Authorization":"Basic " + authKey}
data = { "param":"value"}

request = urllib2.Request(url)

# post form data
# request.add_data(urllib.urlencode(data))

for key,value in headers.items():
  request.add_header(key,value)

response = urllib2.urlopen(request)

print response.info().headers
