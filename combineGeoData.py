import sqlite3
import sys
import json

print sqlite3.version

#  http://mapit.mysociety.org/

try:
    
    jsonFile = open('mapData.geoJSON','wb')
    
    
    con = sqlite3.connect('rewiredState.sqlite')
    
    cur = con.cursor()
    curInput = con.cursor()
    
    
    query="""
        SELECT
        g.ONSconstID,
        g.geoJSON
        FROM
        geoData g
        """
    
    #join and like added when NI poylgons failed
    
    cur.execute(query)
    
    data = cur.fetchall()
    
    
    
    featureCollection ={}
    featureCollection["type"] = "FeatureCollection"
    
    featureList=[]
    
    i=0
    
    for d in data:
        print i
        i=i+1

        feature = {}

        
        feature["geometry"]=json.loads(d[1])
        
        
        properties={}
        properties["id"] = d[0]
        feature["properties"]=properties
        feature["type"] = "Feature"

        featureList.append(feature)


    featureCollection["features"]=featureList

    data_string = json.dump(featureCollection,jsonFile)

    jsonFile.flush()


    jsonFile.close()

except sqlite3.Error, e:
    
    print "Error %s:" % e.args[0]
    sys.exit(1)

finally:
    
    if con:
        con.close()

