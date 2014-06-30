#import pybedtools
from pybedtools import BedTool
from collections import Counter


# The chosen input file is a random test file I got from the Internet 
# and modified for testing my code. Gets the total number of reads from file.
tool1 = BedTool("test2.bed")
reads = tool1.count()


# Finds the start positions of all reads and stores these to a list 
# called "Storage"

storage = []
<<<<<<< HEAD
for x in range(0, reads-1):
    feature = tool1[x]
=======
for feature in tool1:
>>>>>>> 6a51dd6641be4396dca894c778472e5e54c9b200
    if feature.strand == '+':
        start_pos = (feature.start)
        storage.append(start_pos)
    elif feature.strand == '-':
        start_pos = (feature.stop)
        storage.append(start_pos)

# Counts the occurrences of a start position and stores the 
# position and the number of occurrences in a dictionary.
"""result = {} 
for x in storage:
    count = storage.count(x)
    result[x] = count
    while count > 1:
        storage.remove(x)
        count = count - 1 
        
for x in result:
    print x, result[x]"""

result = Counter(storage)
print result