import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("output")
args = parser.parse_args()

with open(args.output, "w") as file_stream:
    file_stream.write("1.00")
