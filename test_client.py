
import httplib
import logging

httplib.HTTPConnection.debuglevel = 1
conn = httplib.HTTPConnection("localhost", 80)

# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


node_id = "2"
f = file("test_data.csv", "r")

request = conn.request("POST", "/node/" + node_id + "/data", f)

print request

response = conn.getresponse()

print response.read()
