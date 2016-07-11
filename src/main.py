import argparse
import tranprocfunctions as function_tool

function_tool.plot_tool.ion()
PAUSE_TIME_FOR_PLOT_VIEW = 0.0

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("output")
arguments = parser.parse_args()

transaction_set = []
max_time_processed = function_tool.datetime.datetime.fromtimestamp(0)

try:
    with open(arguments.input, "r") as input_stream, open(arguments.output, "w") as output_stream:
        for json_line in input_stream:
            transaction = function_tool.parse_transaction_line(json_line)
            if transaction is None:
                continue
            else:
                max_time_processed = function_tool.update_rolling_window(transaction, max_time_processed)
                transaction_set = function_tool.update_transaction_set(transaction_set, transaction, max_time_processed)
                median = function_tool.plot_network_return_median(transaction_set, PAUSE_TIME_FOR_PLOT_VIEW)
                output_stream.write(median)
except IOError:
    print "Error reading or writing to files %s, %s.  Exiting program." % (arguments.input, arguments.output)