#!/usr/bin/python2
import urllib
import json
import plotly.plotly as ply
import plotly.tools as tools
import plotly.graph_objs as go
import random
import math
import datetime
import time

max_streams = 6

# test data generator
def testStreams(stream_ids):
    def gen_xy(i):
        x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        y = (math.cos(5*i/50.)*math.cos(i/50.)+random.randint(0,1))
        return dict(x=x, y=y)

    i = 0
    while True:
        i+=1
        for stream_id in stream_ids:
            s = ply.Stream(stream_id)
            s.open()
            s.write(gen_xy(i))
            s.close()

def getTraces():
    stream_ids = tools.get_credentials_file()['stream_ids']
    stream_ids = stream_ids[:max_streams]
    traces = list()
    for stream_id in stream_ids:
        stream = go.Stream(token=stream_id, maxpoints=200)
        trace = go.Scatter(
            x=[],
            y=[],
            mode='lines+markers',
            stream=stream)
        traces.append(trace)
    return stream_ids, traces

if __name__== '__main__':
                         ############# SETUP #############
    stream_ids, traces = getTraces()

            ### This entire commented section was for automatic graph setup, with the only necessary input being max_streams at the top ###

    # gets the closest-fitting square matrix
    # x_max = y_max = int(round(math.sqrt(max_streams)))
    # if x_max*y_max < max_streams:
    #     x_max += 1

    # names = ['plot1','plot2','plot3','plot4'
    #          'plot5','plot6','plot7','plot8']
    # fig = tools.make_subplots(
    #         rows=2,
    #         cols=2,
    #         subplot_titles=tuple(names[:max_streams]))

    # tr_n = 0  # trace index
    # for x in xrange(x_max):
    #     x+=1  # because plotly's figures starts at 1
    #     for y in xrange(y_max):
    #         y+=1
    #         if tr_n <= max_streams:
    #             fig.append_trace(traces[tr_n], x, y)
    #         tr_n +=1

    # url = ply.plot(fig, filename='s7_first-stream')

    fig = tools.make_subplots(
            rows=2,
            cols=3,
            subplot_titles=("Humidity", "Temperature", "Water Height",
                            "pH level", "MQ2 ppm", "CO2 ppm"))
    the_map = {"HUM": stream_ids[0],
               "TMP": stream_ids[1],
               "Water Height": stream_ids[2],

               "pH" : stream_ids[3],
               "MQ2 ppm": stream_ids[4],
               "CO2 ppm": stream_ids[5]}

    url = 'https://api.particle.io/v1/devices/events?access_token=efb277ba1f27b2633698de75bf6f9b9b1f8fe775'
    f = urllib.urlopen(url)

    fig.append_trace(traces[0], 1, 1)
    fig.append_trace(traces[1], 1, 2)
    fig.append_trace(traces[2], 1, 3)
    fig.append_trace(traces[3], 2, 1)
    fig.append_trace(traces[4], 2, 2)
    fig.append_trace(traces[5], 2, 3)

    url = ply.plot(fig, filename='s7_first-stream')


                        ############# DO WORK #############
    while True:
        a = f.readline().rstrip()
        if "event:" in a:
            event = a
            event = a[7:]  # get rid of "event: ", so we just have the name
            data = f.readline().rstrip()
            data = data[6:]  # gets rid of "data: ", so we just have the json
            try:
                jdata = json.loads(data)
            except ValueError as e:
                print "-----BROKEN JSON PARSE-----"
                print "EVENT:", event
                print "DATA:", data
                print "---------------------------"

            if event in the_map:
                streamid = the_map[event]
                s = ply.Stream(streamid)
                s.open()
                try:
                    s.write(dict(y=jdata["data"], x=time.time()))
                except ValueError as e:
                    print e
                    print "------FAILED WRITE-----"
                    print "EVENT:", event
                    if "data" in jdata and "published_at" in jdata:
                        print jdata["data"]
                        print jdata["published_at"]
                    print "-----------------------"
                    s.close()
                s.close()
            else:
                print "NOT IN DICT:", event
        else:
            print "SKIPPED DATA: ", a
