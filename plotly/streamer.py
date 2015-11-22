#!/usr/bin/python
import urllib
import json

url = 'https://api.particle.io/v1/devices/events?access_token=efb277ba1f27b2633698de75bf6f9b9b1f8fe775'
f = urllib.urlopen(url)

# initiating response is :ok\n

print f.readline()
while True:
    a = f.readline().rstrip()
    if "event:" in a:
        event = a
        event = a[7:]
        data = f.readline().rstrip()
        data = data[6:]
        try:
            jdata = json.loads(data)
        except ValueError as e:
            print "-----BROKEN-----"
            print "EVENT:", event
            print "DATA:", data
            print "----------------"
        print event, ":", jdata["data"]
