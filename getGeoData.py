import sqlite3
import sys
import urllib2
import time

print sqlite3.version

turnout_all = 0.44

try:
    
    
    con = sqlite3.connect('rewiredState.sqlite')
    
    cur = con.cursor()
    curInput = con.cursor()
    
    
    query="""
        SELECT
        e.ONSconstID
        FROM
        ElectionResults e
        left JOIN geoData g
        on e.ONSconstID = g.ONSconstID
        where g.ONSconstID is null
        and e.ONSconstID not like "N%"
        """
    
    #join and like added when NI poylgons failed
    
    cur.execute(query)
    
    data = cur.fetchall()
   
    
    print "constID"
    
    
    url = "http://mapit.mysociety.org/area/"
    
    i=0
    
    for d in data:
        print url+d[0]+".geojson"
        
        response = urllib2.urlopen(url+d[0]+".geojson")
        geoData = response.read()
        
        print "sleeping... ",i
        time.sleep(1) #time limited to avoid overloading server
        i=i+1
        
        print len(geoData)

        curInput.execute("INSERT INTO geoData (ONSconstID , geoJSON) VALUES (?,?)",(d[0],geoData))

        con.commit()



except sqlite3.Error, e:
    
    print "Error %s:" % e.args[0]
    sys.exit(1)

finally:
    
    if con:
        con.close()

