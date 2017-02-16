import sqlite3
import sys
#import decimal
import csv

print sqlite3.version

turnout_all = 0.44

try:

    csvFile = open('voteData.csv','wb')
    csvWriter = csv.writer(csvFile)

    con = sqlite3.connect('rewiredState.sqlite')

    cur = con.cursor()


    query="""
        SELECT
        e.ONSconstID,
        e.Majority,
        e.ConstituencyName,
        e.RegionName,
        e.PartyShortName,
        a.`Age15-19`,
        a.`Age20-24`
        FROM
        ElectionResults e
        JOIN
        AgeEstimates2010 a
        ON
        a.ConstituencyID = e.ONSconstID
        """
    


    cur.execute(query)

    data = cur.fetchall()

    print "constID, missingVoters, majority, constName, regionName, partyName"

    csvWriter.writerow(("constID", "missingVoters", "majority", "constName", "regionName", "partyName"))

    for d in data:
        age18_20 =  int(d[5].replace(',', '')) *0.4
        age20_24 =  int(d[6].replace(',', ''))
        maj = int(d[1].replace(',', ''))
        missingVoters = (age18_20 + age20_24) 
        name = unicode(d[2]).encode("utf-8")
        print d[0], missingVoters, maj, name, d[3], d[4]
        csvWriter.writerow((d[0], missingVoters, maj, name, d[3], d[4]))


    csvFile.close()

except sqlite3.Error, e:
    
    print "Error %s:" % e.args[0]
    sys.exit(1)

finally:
    
    if con:
        con.close()

