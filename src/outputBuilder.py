import csv
import os

# Throughout class, "row" is used to denote data from the output file 
# e.g, "new_row" is data to be written to the output file

class OutputBuilder:
    
   #class attributes to represent fields of the csv file
    __iTime = 0
    __iSymbol = 1
    __iQuant = 2
    __iPrice = 3
    
    __oSymbol = 0
    __oTime = 1
    __oQuant = 2
    __oAvg = 3
    __oPrice = 4

    def __init__(self):
        cur_path = os.path.dirname(__file__)
        output_path = os.path.relpath("../outputs/output.csv", cur_path)
        self.time_diff = dict() #always of format {symbol: (timestamp, max)}

        try:
            self.output = open(output_path, "w+", newline="")
            self.writer = csv.writer(self.output, delimiter=",")
            self.reader = csv.reader(self.output)
        except:
            print("output file creation error")
    
    def find_in_output(self, symbol):
        self.output.seek(0)
        value = None
        method = None
        old_row = None
        i = 0
        for row in self.reader:
            if row[OutputBuilder.__oSymbol] == symbol:
                value = i
                method = "update"
                old_row = row
                break
            elif symbol > row[OutputBuilder.__oSymbol]:
                None
            else: 
                value = i
                method = "insert"
                break
            i += 1
        return value, method, old_row

    # Creates an average, rounded, using the round even rule
    def rnd_avg(self, sum, count):
        dec_avg = sum/count
        int_avg = int(sum/count)
        if dec_avg-int_avg > 0.5:
            int_avg += 1
        elif dec_avg-int_avg == 0.5:
            if int_avg%2 == 1:
                int_avg += 1
        return int_avg

    def max_interval(self, old_timeinfo, new_timestamp):
        old_timestamp = int(old_timeinfo[0])
        time_max = old_timeinfo[1]
        time_diff = int(new_timestamp) - old_timestamp
        if time_diff > time_max:
            return time_diff
        else:
            return time_max

    def build_row(self, line, max):
        avg = self.rnd_avg(
                           int(line[OutputBuilder.__iPrice]),
                           int(line[OutputBuilder.__iQuant])
                          )
        new_row = [
                   line[OutputBuilder.__iSymbol], max, line[OutputBuilder.__iQuant],
                   avg, line[OutputBuilder.__iPrice]
                  ]
        return new_row

    def insert_line(self, line, location, method):
        # In a scenario where the output file is too large for memory,
        # write lines to an external file and rename file at end of process
        self.output.seek(0)
        i = 0
        temp_list=[]
        for row in self.reader:
            if i == location and method == "insert":
                symbol = line[OutputBuilder.__iSymbol]           
                self.time_diff[symbol] = (line[OutputBuilder.__iTime], 0)
                new_row = self.build_row(line, 0)
                temp_list.append(new_row)
                temp_list.append(row)
            elif i == location and method == "update":
                temp_list.append(line)
            else:
                temp_list.append(row)
            i+=1

        self.output.seek(0)
        self.writer.writerows(temp_list)

    def update_line(self, line, location, old_row):
        symbol = line[OutputBuilder.__iSymbol]
        new_timestamp = line[OutputBuilder.__iTime]
        old_timeinfo = self.time_diff[symbol]
        time_max = self.max_interval(old_timeinfo, new_timestamp)

        quantity = (int(line[OutputBuilder.__iQuant])
                   + int(old_row[OutputBuilder.__oQuant]))
        old_total = (int(old_row[OutputBuilder.__oQuant])
                   * int(old_row[OutputBuilder.__oAvg]))
        new_total = int(line[OutputBuilder.__iPrice])
        avg = self.rnd_avg(old_total+new_total, quantity)
        price_max = old_row[OutputBuilder.__oPrice]
        if line[OutputBuilder.__iPrice] > price_max:
            price_max = line[OutputBuilder.__iPrice]

        self.time_diff[symbol] = (new_timestamp, time_max)
        new_row = [symbol, time_max, quantity, avg, price_max]
        self.insert_line(new_row, location, "update")

    def process_line(self, line):
        symbol = line[OutputBuilder.__iSymbol]
        line_num, method, old_row = self.find_in_output(symbol)
        if method == "insert":
            self.insert_line(line, line_num, method)
        elif method == "update":
            self.update_line(line, line_num, old_row)
        else:
            self.time_diff[symbol] = (line[OutputBuilder.__iTime], 0)
            new_row = self.build_row(line, 0)
            self.writer.writerow(new_row)

