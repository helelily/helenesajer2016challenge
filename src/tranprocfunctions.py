import json
import networkx
import matplotlib.pyplot as plot_tool
import datetime
import statistics


decoder = json.JSONDecoder()


def parse_transaction_line(json_line):
    try:
        transaction_line = decoder.decode(json_line)
    except ValueError:
        return None

    try:
        created_time = transaction_line['created_time']
        target = transaction_line['target']
        actor = transaction_line['actor']
    except KeyError:
        return None

    try:
        transaction_time = datetime.datetime.strptime(created_time, '%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        return None

    if not transaction_time or not target or not actor:
        return None

    else:
        parsed_transaction = (transaction_time, (target, actor))
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
    plot_tool.pause(0.0001)
    plot_tool.close()

    degrees = [degree[1] for degree in transactionGraph.degree()]
    median = "%.2f\n" % statistics.median(degrees)
    return median
