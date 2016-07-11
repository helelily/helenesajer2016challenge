import argparse
import json
import matplotlib.pyplot as plot_tool
import datetime
import tranprocfunctions as function_tool

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("output")
arguments = parser.parse_args()

plot_tool.ion()

decoder = json.JSONDecoder()
transaction_set = []
max_time_processed = datetime.datetime.fromtimestamp(0)


try:
    with open(arguments.input, "r") as input_stream, open(arguments.output, "w") as output_stream:
        for json_line in input_stream:
            transaction_line = decoder.decode(json_line)
            try:
                transaction = function_tool.parse_transaction_line(transaction_line)
            except ValueError:
                continue
            max_time_processed = function_tool.update_rolling_window(transaction, max_time_processed)
            transaction_set = function_tool.update_transaction_set(transaction_set, transaction, max_time_processed)
            median = function_tool.plot_network_return_median(transaction_set)
            output_stream.write(median)
except IOError:
    print "Error reading or writing to files %s, %s.  Exiting program." % (arguments.input, arguments.output)
