import argparse
import json
import networkx
import matplotlib.pyplot as plotTool
import datetime
import statistics
import math


parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("output")
arguments = parser.parse_args()

decoder = json.JSONDecoder()
plotTool.ion()
tranSet = []
maxTimeProcessed = datetime.datetime.fromtimestamp(0)
output_stream = open(arguments.output, "w")

with open(arguments.input, "r") as input_stream:
    for json_line in input_stream:
        transactionLine = decoder.decode(json_line)
        currentTranTime = datetime.datetime.strptime(transactionLine['created_time'], '%Y-%m-%dT%H:%M:%SZ')
        maxTimeProcessed = max(maxTimeProcessed, currentTranTime)
        minTime = maxTimeProcessed + datetime.timedelta(seconds=-60)
        transaction = (currentTranTime, (transactionLine['target'], transactionLine['actor']))
        tranSet.append(transaction)
        tranSet = [(time, (t, a)) for (time, (t, a)) in tranSet if minTime < time <= maxTimeProcessed]
        pairsInWindow = [(t, a) for (time, (t, a)) in tranSet]
        tranMultiGraph = networkx.Graph(pairsInWindow)
        degrees = [degree[1] for degree in tranMultiGraph.degree()]
        median = "%.2f\n" % statistics.median(degrees)
        output_stream.write(median)
        networkx.draw_circular(tranMultiGraph)
        plotTool.show()
        plotTool.pause(5)
        plotTool.close()


output_stream.close()

'''

How should I account for transactions that are missing an "actor" field?
These errors in the input should be ignored by your program with correct exception handling. They should not affect your graph, and should not result in a new line in the output file. For simplicity, we have removed these entries from the sample file we have provided.
'''
