import csv
import os
from outputBuilder import OutputBuilder


def main():
    output = OutputBuilder()
    cur_path = os.path.dirname(__file__)
    input_path = os.path.relpath("../inputs/input.csv", cur_path)

    try:
        # Assuming "input.csv" is simulating a real-time buffer
        stream = open(input_path, "r", newline="") 
        ireader = csv.reader(stream)
        while True:
            try:
                line = next(ireader)
                output.process_line(line)
            except StopIteration:
                print("task completed")
                break
    except:
        print("input file error")


if __name__ == "__main__":
    main()
