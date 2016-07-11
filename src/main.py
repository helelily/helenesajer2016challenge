import argparse
import json
import networkx
import matplotlib.pyplot as plot_tool
import datetime
import statistics

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("output")
arguments = parser.parse_args()


def parse_transaction_line(transaction_line):
    created_time = datetime.datetime.strptime(transaction_line['created_time'], '%Y-%m-%dT%H:%M:%SZ')
    target = transaction_line['target']
    actor = transaction_line['actor']
    parsed_transaction = (created_time, (target, actor))
    return parsed_transaction


def update_rolling_window(transaction, max_time_processed):
    return max(transaction[0], max_time_processed)


def update_transaction_set(transaction_set, transaction, max_time_processed):
    min_time = max_time_processed + datetime.timedelta(seconds= -60)
    transaction_set.append(transaction)
    transaction_set = [(time, (t, a)) for (time, (t, a)) in transaction_set if min_time < time <= max_time_processed]
    return transaction_set


def plot_network_return_median(transaction_set):
    pairsInWindow = [(t, a) for (time, (t, a)) in transaction_set]
    transactionGraph = networkx.Graph(pairsInWindow)
    networkx.draw_circular(transactionGraph)
    plot_tool.show()
    plot_tool.close()

    degrees = [degree[1] for degree in transactionGraph.degree()]
    median = "%.2f\n" % statistics.median(degrees)
    return median

decoder = json.JSONDecoder()
plot_tool.ion()
transaction_set = []
max_time_processed = datetime.datetime.fromtimestamp(0)
try:
    with open(arguments.input, "r") as input_stream, open(arguments.output, "w") as output_stream:
        for json_line in input_stream:
            transaction_line = decoder.decode(json_line)
            try:
                transaction = parse_transaction_line(transaction_line)
            except ValueError:
                continue

            max_time_processed = update_rolling_window(transaction, max_time_processed)
            transaction_set = update_transaction_set(transaction_set, transaction, max_time_processed)
            median = plot_network_return_median(transaction_set)
            output_stream.write(median)
except IOError:
    print "Error reading or writing to files %s, %s.  Exiting program." % (arguments.input, arguments.output)
