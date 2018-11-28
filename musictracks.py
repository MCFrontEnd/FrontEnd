import json

d = {}
with open("unique_tracks.txt", encoding="utf8") as f:
    for line in f:
       (tid, sid, artistname, songname) = line.split("<SEP>")
       d[tid] = songname[:-1]
       d[songname[:-1]] = tid
f.close()

with open("data.json", "w") as outfile:
	json.dump(d, outfile)
outfile.close()