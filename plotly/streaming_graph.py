#!/usr/bin/python2
import plotly.plotly as ply
import plotly.tools as tools
import plotly.graph_objs as go
import random
import math
import datetime
import time

max_streams = 4

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
    stream_ids, traces = getTraces()

    names = ['plot1','plot2','plot3','plot4'
             'plot5','plot6','plot7','plot8']
    fig = tools.make_subplots(
            rows=2,
            cols=2,
            subplot_titles=tuple(names[:max_streams]))

    # gets the closest-fitting square matrix
    def getMatrixSize(x):
        a = b = int(round(math.sqrt(x)))
        if a*b < x:
            a+=1
        return a, b

    x_max, y_max = getMatrixSize(max_streams)
    tr_n = 0  # trace index
    for x in xrange(x_max):
        x+=1  # because plotly's figures starts at 1
        for y in xrange(y_max):
            y+=1
            if tr_n <= max_streams:
                fig.append_trace(traces[tr_n], x, y)
            tr_n +=1

    url = ply.plot(fig, filename='s7_first-stream')

    testStreams(stream_ids)
