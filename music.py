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
    print ('demo_tags_db.py')
    sys.exit(0)

if __name__ == '__main__':

    #if len(sys.argv) != 2:
    #    die_with_usage()

    # param
    dbfile = "lastfm_tags.db"

    # sanity check
    #if not os.path.isfile(dbfile):
    #    print ('ERROR: db file %s does not exist?') % dbfile
    #    die_with_usage()

    # open connection
    conn = sqlite3.connect(dbfile)

   

    #find tid from song name
    with open('data.json', 'r') as fp:
        songdata = json.load(fp)
    fp.close()
    print("Song Name: " + songdata["TRCCILA128F42BA535"])
    print("Track ID: " + songdata[songdata["TRCCILA128F42BA535"]])
    tid = songdata[songdata["TRCCILA128F42BA535"]]
    print ('We get all tags (with value) for track: %s' % tid)
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
    topten = {}
    while len(topten) < 5:
        for str in data2:
            if d[str] == maximum:
                topten[str] = d[str]
        maximum = maximum - 1
    print(topten)
    for k in topten:
        print(songdata[k[0]])



    #print(d)

    # EXAMPLE 1
    print ('************** DEMO 1 **************')
    print ('Get the list of all unique tags')
    sql = "SELECT tag FROM tags"
    res = conn.execute(sql)
    data = res.fetchall()
    for k in range(10):
        print (data[k])
    print ('...')
    print ('(total number of tags: %d)' % len(data))
    
        # EXAMPLE 2
    print ('************** DEMO 2 **************')
    print ('We get all tracks with at least one tag')
    sql = "SELECT tid FROM tids"
    res = conn.execute(sql)
    data = res.fetchall()
    for k in range(10):
        tid = data[k][0]
        tid = (tid)
        #tid = list(tid[2:20])
        print (tid)
        print ('We get all tags (with value) for track: %s' % tid)
        sql2 = "SELECT tags.tag, tid_tag.val FROM tid_tag, tids, tags WHERE tags.ROWID=tid_tag.tag AND tid_tag.tid=tids.ROWID and tids.tid='%s'" % tid
        res2 = conn.execute(sql2)
        data2 = res2.fetchall()
        print (data2)
    print ('...')
    print ('(total number of track IDs: %d)' % len(data))

    # EXAMPLE 3
    print ('************** DEMO 3 **************')
    tid = ('TRCCOFQ128F4285A9E')
    print ('We get all tags (with value) for track: %s' % tid)
    sql = "SELECT tags.tag, tid_tag.val FROM tid_tag, tids, tags WHERE tags.ROWID=tid_tag.tag AND tid_tag.tid=tids.ROWID and tids.tid='%s'" % tid
    res = conn.execute(sql)
    data = res.fetchall()
    print (data)

    # EXAMPLE 4
    print ('************** DEMO 4 - tracks for each tag **************')
    tag = 'classic rock'
    print ('We get all tracks for the tag: %s' % tag)
    sql = "SELECT tids.tid FROM tid_tag, tids, tags WHERE tids.ROWID=tid_tag.tid AND tid_tag.tag=tags.ROWID AND tags.tag='%s'" % sanitize(tag)
    res = conn.execute(sql)
    data = res.fetchall()
    #print (list(map(str,data)))
    #d = {}
    #for str in data:
    #    if d.get(str) == None:
    #        d[str] = 1
    #    else: d[str] = d[str] + 1
    #print(d)

    # EXAMPLE 5
    #print ('************** DEMO 5 **************')
    #print ("We get all tags and the number of tracks they're applied to")
    #sql = "SELECT tags.tag, COUNT(tid_tag.tid) FROM tid_tag, tags WHERE tid_tag.tag=tags.ROWID GROUP BY tags.tag"
    #res = conn.execute(sql)
    #data = res.fetchall()
    #data = sorted(data, key=lambda x: x[1], reverse=True)
    #print ('after sorting...')
    #for k in range(10):
    #    print (data[k])
    #print ('...')

    # done, close connection
    conn.close()