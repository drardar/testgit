import time
import datetime
import requests
import sqlite3 as lite
import os
from multiprocessing.dummy import Pool
pool = Pool(processes=2)

#URL: https://api.lendingclub.com/api/investor/<version>/accounts/<investor id>/detailednotes
#Authorization: JWHAUeua+ZDDGLsJzWIqagyVOEU=

acctNum = 56732213
version = "v1"
auth = "JWHAUeua+ZDDGLsJzWIqagyVOEU="
reqAdd = "https://api.lendingclub.com/api/investor/" + version + "/accounts/" + str(acctNum) + "/detailednotes"


# Setup database information
dbPath = os.path.join(os.path.dirname(os.getcwd()), 'Python34', 'lcDb.sqlite')
dbTable = 'detailednotes'

def test():
    r=requests.get(reqAdd, headers={"Authorization": auth})
    #tempList = [None, str(time.strftime("%I:%M:%S")),
    tempList = r.json()['myNotes']
    for i in tempList:
        print i['loanId']

    #time.sleep(1)
    #return tempList
    #print tempList
    #return (time.strftime("%I:%M:%S") + " " + str(r.json()['availableCash']))

test()


