import networkx
import matplotlib.pyplot as plot_tool
import datetime
import statistics


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
