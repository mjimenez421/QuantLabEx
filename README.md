QuantLabEx
==========
Written using python 3.5

Source Code
-----------
Source code is found in /src, and run from main.py. Input and output file are currently hardcoded.

Code was written assuming input.csv is simulating a buffer from a socket stream. It is mostly assumed that output data is also too large for memory, with the exception of the three fields that make up the time_diff dictionary. This was done as a mid-ground between performance time and storage space.

Inputs and Outputs
------------------
Input and output files are found in /inputs and /outputs, respectively. outputMini.csv is used for testing purposes **ONLY**, and was created by running the source code on inputMini.csv

Tests
-----
Unit tests can be found in /tests. There is one unit test file at the time, for testing the outputBuilder class
