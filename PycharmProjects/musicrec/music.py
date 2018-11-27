import os
import sys
import sqlite3
import json


def sanitize(tag):
    """
    sanitize a tag so it can be included or queried in the db
    """
    tag = tag.replace("'","''")
    return tag


def die_with_usage():
    """ HELP MENU """
    sys.exit(0)

def get_songs(songName):

    dbfile = "lastfm_tags.db"
    
    conn = sqlite3.connect(dbfile)
    #find tid from song name
    with open('data.json', 'r') as fp:
        songdata = json.load(fp)
    fp.close()
    tid = songdata[songName]
    sql = "SELECT tags.tag, tid_tag.val FROM tid_tag, tids, tags WHERE tags.ROWID=tid_tag.tag AND tid_tag.tid=tids.ROWID and tids.tid='%s'" % tid
    res = conn.execute(sql)
    data = res.fetchall()
    print (data)
    size = len(data)
    #print(size)
    d = {}
    #for each tag
    for k in data:
        tag = k[0]  #0 is the tag, k[1] = value
        sql2 = "SELECT tids.tid FROM tid_tag, tids, tags WHERE tids.ROWID=tid_tag.tid AND tid_tag.tag=tags.ROWID AND tags.tag='%s'" % sanitize(tag)
        res2 = conn.execute(sql2)
        data2 = res2.fetchall()    #all track names with the tag
        maximum = 0
        for str in data2:      #str is for every tag
            if d.get(str) == None:
                d[str] = 1
            else: 
                d[str] = d[str] + 1
                if d[str] > maximum and d[str] != size:
                    maximum = d[str]
    topten = []
    while len(topten) < 5:
        for str in data2:
            if d[str] == maximum:
                topten.append(d[str])
        maximum = maximum - 1

    conn.close()
    return topten
    #print(topten)
    #for k in topten:
    #    print(songdata[k[0]])
