from pybedtools import BedTool
from collections import Counter
import matplotlib
import matplotlib.pyplot as plt
import pylab as pl
import numpy as np
import csv


print """This script will take a .bed file as input, find the starting points of all reads 
and output a table containing all thestarting points and the number of reads that start at this point"""

filepath = raw_input("Enter the path of the file you wish to analyze: ")
tool1 = BedTool(filepath)


# Finds the start positions of all reads and stores these to a list 
# called "storage"
# Counts the occurrences of every start position and stores the 
# position and the number of occurrences in a dictionary called "result"

storage = []

for feature in tool1:

    if feature.strand == '+':
        start_pos = (feature.start)
        storage.append(start_pos)
    elif feature.strand == '-':
        start_pos = (feature.stop - 1)
        storage.append(start_pos)

result = Counter(storage)

# Draws a histogram of the data from the file. So far haven't figured out how to add labels to every starting point.

length = len(storage)
fig = plt.figure(figsize=(80,40), dpi=100)   
pl.hist(storage, length, histtype = "step", align = "mid", color = "black", label = "reads")
plt.legend()
plt.show()

# Outputs a table with the starting points and the number of its occurrences.
output = csv.writer(open("output.csv", "w"))
for key, val in result.items():
    output.writerow([key, val])
print "Analysis complete"

