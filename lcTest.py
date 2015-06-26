import time
import datetime
import requests
import sqlite3 as lite
import os
from multiprocessing.dummy import Pool
pool = Pool(processes=2)

#URL: https://api.lendingclub.com/api/investor/<version>/accounts/<investor id>/availablecash
#Authorization: Vkqakl1lAygRyXRwlKCOyHWG4DE

acctNum = 8927319
version = "v1"
auth = "8EHjso6/6mmO8WfMGGEiqvtpdCU="
reqAdd = "https://api.lendingclub.com/api/investor/" + version + "/accounts/" + str(acctNum) + "/availablecash"

# Setup database information
dbPath = os.path.join(os.path.dirname(os.getcwd()), 'lcTestStuff', 'lcDb.sqlite')
dbTable = 'lcMain'

def test():
    r=requests.get(reqAdd, headers={"Authorization": auth})
    tempList = [None, str(time.strftime("%I:%M:%S")), str(r.json()['availableCash'])]
    time.sleep(1)
    return tempList
    #return (time.strftime("%I:%M:%S") + " " + str(r.json()['availableCash']))

def addToDb(tempList):
    con = lite.connect(dbPath)
    dbString = "INSERT INTO " + dbTable + \
        " VALUES(?,?,?)"  # create database string

    with con:
        cur = con.cursor()
        cur.execute(dbString, tempList)
        print "Inserted: " + ", ".join(tempList[1:])

while True:
    time.sleep(1)
    pool.apply_async(test, callback=addToDb)
