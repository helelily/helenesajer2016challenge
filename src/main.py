import argparse
import json
import networkx
import matplotlib.pyplot as plotTool
import datetime
import statistics

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("output")
arguments = parser.parse_args()

decoder = json.JSONDecoder()
plotTool.ion()
transactionSet = []
maxTimeProcessed = datetime.datetime.fromtimestamp(0)
output_stream = open(arguments.output, "w")

with open(arguments.input, "r") as input_stream:
    for json_line in input_stream:
        transactionLine = decoder.decode(json_line)
        currentTranTime = datetime.datetime.strptime(transactionLine['created_time'], '%Y-%m-%dT%H:%M:%SZ')
        maxTimeProcessed = max(maxTimeProcessed, currentTranTime)
        minTime = maxTimeProcessed + datetime.timedelta(seconds=-60)
        transaction = (currentTranTime, (transactionLine['target'], transactionLine['actor']))
        transactionSet.append(transaction)
        transactionSet = [(time, (t, a)) for (time, (t, a)) in transactionSet if minTime < time <= maxTimeProcessed]
        pairsInWindow = [(t, a) for (time, (t, a)) in transactionSet]
        transactionGraph = networkx.Graph(pairsInWindow)
        degrees = [degree[1] for degree in transactionGraph.degree()]
        median = "%.2f\n" % statistics.median(degrees)
        output_stream.write(median)
        networkx.draw_circular(transactionGraph)
        plotTool.show()
        plotTool.close()

output_stream.close()

'''
exception handling and separate into functions
'''
