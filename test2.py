import json
import urllib2
json.load(urllib2.urlopen("https://api.lendingclub.com/api/investor/v1/accounts/56732213/summary"))
