from pybedtools import BedTool
from collections import Counter
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import csv


print """This script will take a .bed file as input, find the starting points of all reads 
and output a table containing all thestarting points and the number of reads that start at this point"""

#filepath = raw_input("Enter the path of the file you wish to analyze: ")
filepath = 'test2.bed'
tool1 = BedTool(filepath)


# Finds the start positions of all reads and stores these to a list 
# called "storage"
# Counts the occurrences of every start position and stores the 
# position and the number of occurrences in a dictionary called "result"

def get_position_counts(bed_file, direction):

    positions = []
    
    for feature in bed_file:

        if direction != feature.strand:
            continue
        
        if direction == '+':
            start_pos = (feature.start)
        elif direction == '-':
            start_pos = (feature.stop - 1)

        positions.append(start_pos)

    return Counter(positions)

pc = get_position_counts(tool1, '+')

x = []
y = []
ptcnt = 0
for index in range(min(pc), max(pc)):
    if ptcnt > 20:
        continue
        
    if index in pc:
        ptcnt += 1
        y.append(pc[index])
    else:
        y.append(0)
    x.append(index)    

# Draws a histogram of the data from the file. So far haven't figured out how to add labels to every starting point.

fig = plt.figure(figsize=(8,6))   
plt.scatter(x, y)#, histtype = "step", align = "mid", color = "black", label = "reads")
plt.savefig('test2.pdf')

# Outputs a table with the starting points and the number of its occurrences.
output = csv.writer(open("output.csv", "w"))
for key, val in pc.items():
    output.writerow([key, val])
print "Analysis complete"

