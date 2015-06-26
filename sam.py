import csv
import sqlite3 as lite
import os
import sys

'''
execute in the directory with the csv file

'''


def readCSVfile(csvName):
    # Read csv file into list
    with open(csvName, 'rb') as f:
        tmpList = []
        reader = csv.reader(f)
        i = 0
        for row in reader:
            if i > 0:
                tmpList.append(row)
            i += 1
    return tmpList


def runUpload(csvName):
    # create table dictionary
    dbDict = {
        'signal': 'cRawData',
        'alpha': 'cAlphaData',
        'hfri': 'cHFRIData',
    }

    importList = readCSVfile(csvName)

    # Setup database information
    dbPath = os.path.join(os.path.dirname(os.getcwd()), 'sqlite3',
                          'hfsignalsV1.sqlite')
    con = lite.connect(dbPath)

    with con:
        cur = con.cursor()

        # delete all hfri data prior to import
        dbTable = dbDict['hfri']
        cur.execute("Delete from " + dbTable)

        # loop list
        insertNum = 0  # counter for uploads
        for row in importList:
            dbTable = dbDict[row[0]]
            # confirm that the record does not already exist
            # if it does then skip, unless overwrite has been selected
            cur.execute("Select count(*) from " + dbTable + " where cTickID=? \
                        and cDate=?", (row[1], row[2]))
            if cur.fetchone()[0] > 0:
                print "Duplicate: " + ", ".join(row)
                continue

            print "Inserted: " + ", ".join(row)
            insertNum += 1
            row[0] = None
            dbString = "INSERT INTO " + dbTable + \
                " VALUES(?,?,?,?,?)"  # create database string
            cur.execute(dbString, row)

        print str(insertNum) + "/" + str(len(importList)) + " imported"

if __name__ == '__main__':
    # readCSVfile(sys.argv[1])
    runUpload(sys.argv[1])
