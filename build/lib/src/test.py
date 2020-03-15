import unittest
import csv
import os
from outputBuilder import OutputBuilder


class TestBuilder(unittest.TestCase):
    # Output file and reader needed to test find_in_output
    cur_path = os.path.dirname(__file__)
    output_path = os.path.relpath("../outputs/outputMini.csv", cur_path) 
    output = open(output_path, "r", newline="")
    reader = csv.reader(output)

    # A copy of rnd_avg from OutputBuilder to run test_build_row
    def rnd_avg(self, sum, count):
        dec_avg = sum/count
        int_avg = int(sum/count)
        if dec_avg-int_avg > 0.5:
            int_avg += 1
        elif dec_avg-int_avg == 0.5:
            if int_avg%2 == 1:
                int_avg += 1
        return int_avg    

    def test_avg(self):
        sum = 5
        count = 2
        result = OutputBuilder.rnd_avg(self, sum, count)
        self.assertEqual(result, 2)
        sum = 7
        count = 2
        result = OutputBuilder.rnd_avg(self, sum, count)
        self.assertEqual(result, 4)

    def test_max_interval(self):
        old_timeinfo = ('36', 4)
        new_timestamp = '45'
        result = OutputBuilder.max_interval(self, old_timeinfo, new_timestamp)
        self.assertEqual(result, 9)
        new_timestamp = '37'
        result = OutputBuilder.max_interval(self, old_timeinfo, new_timestamp)
        self.assertEqual(result, 4)

    def test_build_row(self):
        line = [51300355437,"gfd",135,255]
        max = 69
        result = OutputBuilder.build_row(self, line, max)
        self.assertEqual(result, ["gfd",69,135,2,255])
 
    def test_find_in_output(self):
        symbol = "bgf"
        result = OutputBuilder.find_in_output(self, symbol)
        self.assertEqual(result, 
                         (45 ,'update', ['bgf', '0', '122', '1', '130']))
        symbol = "hij"
        result = OutputBuilder.find_in_output(self, symbol)
        self.assertEqual(result, (None, None, None)) 
        symbol = "def"
        result = OutputBuilder.find_in_output(self, symbol)
        self.assertEqual(result, (83, 'insert', None))

if __name__ == "__main__":
    unittest.main()

