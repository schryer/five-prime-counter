import sys
import time
import os
import bz2file
import gzip
#from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
#    ProgressBar, ReverseBar, RotatingMarker, \
#    SimpleProgress, Timer

class ParseFastQ(object):
    """Returns a read-by-read fastQ parser analogous to file.readline()"""
    def __init__(self,filePath,headerSymbols=['@','+']):
        """Returns a read-by-read fastQ parser analogous to file.readline().
        Exmpl: parser.next()
        -OR-
        Its an iterator so you can do:
        for rec in parser:
            ... do something with rec ...
 
        rec is tuple: (seqHeader,seqStr,qualHeader,qualStr)
        """
        if filePath.endswith('.gz'):
            self._file = gzip.open(filePath)
        elif filePath.endswith('.bz2'):
            self._file = bz2file.open(filePath, 'rt')
        else:
            self._file = open(filePath, 'r+')
        self._currentLineNumber = 0
        self._hdSyms = headerSymbols
         
    def __iter__(self):
        return self
     
    def next(self):
        """Reads in next element, parses, and does minimal verification.
        Returns: tuple: (seqHeader,seqStr,qualHeader,qualStr)"""
        # ++++ Get Next Four Lines ++++
        elemList = []
        for i in range(4):
            line = self._file.readline()
            self._currentLineNumber += 1 ## increment file position
            if line:
                elemList.append(line.strip('\n'))
            else:
                elemList.append(None)
         
        # ++++ Check Lines For Expected Form ++++
        trues = [bool(x) for x in elemList].count(True)
        nones = elemList.count(None)
        # -- Check for acceptable end of file --
        if nones == 4:
            raise StopIteration
        # -- Make sure we got 4 full lines of data --
        assert trues == 4,\
               "** ERROR: It looks like I encountered a premature EOF or empty line.\n\
               Please check FastQ file near line number %s (plus or minus ~4 lines) and try again**" % (self._currentLineNumber)
        # -- Make sure we are in the correct "register" --
        assert elemList[0].startswith(self._hdSyms[0]),\
               "** ERROR: The 1st line in fastq element does not start with '%s'.\n\
               Please check FastQ file near line number %s (plus or minus ~4 lines) and try again**" % (self._hdSyms[0],self._currentLineNumber)
        assert elemList[2].startswith(self._hdSyms[1]),\
               "** ERROR: The 3rd line in fastq element does not start with '%s'.\n\
               Please check FastQ file near line number %s (plus or minus ~4 lines) and try again**" % (self._hdSyms[1],self._currentLineNumber)
        # -- Make sure the seq line and qual line have equal lengths --
        assert len(elemList[1]) == len(elemList[3]), "** ERROR: The length of Sequence data and Quality data of the last record aren't equal.\n\
               Please check FastQ file near line number %s (plus or minus ~4 lines) and try again**" % (self._currentLineNumber)
         
        # ++++ Return fatsQ data as list ++++
        return list(elemList)

file_path = raw_input("Enter the path of the reads file ")
parser = ParseFastQ(file_path)

output = open('output.fastq', 'w')



        # ++++ Set up the loading bar +++ #
#num_lines = sum(1 for line in open(file_path))
#widgets = [Bar('>'), ' ', ETA(), ' ', ReverseBar('<')]
#pbar = ProgressBar(widgets=widgets, maxval=num_lines).start()    
#i = 0

        # ++++ remove 2 nucleotides from 3'-end and all A nucleotides from 5'-end in .fastq++++ #
for record in parser:
    count = 0
    for x in record[1][::-1]:
        if x == 'A':
            count += 1
        else:
            continue
    record[1] = record[1][2:-count]   
    record[3] = record[3][2:-count]
        
    for line in record: 
        output.write("%s\n" % line)
#       i += 1
#       pbar.update(i)
#pbar.finish()

print 'FastQ modified!'

        # ++++ sets up indexing and aligning through 'bwa tools' ++++ #
def index_genome(reference_genome):
    output = os.system("bwa index -a is {0}".format(reference_genome))

def align(index):
    output = os.system("bwa mem %s %s > aligned.sam" % (index, 'output.fastq'))

while True:
    align_ask = raw_input('Do you want to align reads? ')

    if align_ask == 'y' or align_ask =='yes':
        index_ask = raw_input('Do you need to index a reference genome? ')
        if index_ask == 'y' or index_ask =='yes':
            reference_genome = raw_input('Enter the path of the reference genome ')
            count = 0
            for x in reference_genome:
                if x != '/':
                    count += 1
                else:
                    continue
            index = reference_genome[-count:]
            align(index)
        elif index_ask == 'n' or index_ask == 'no':
            index = raw_input('Enter the name of indexed genome ')
            align(index)
        else:
            print 'Sorry, {0} is a strange answer that I do not understand. Try again!'.format(align_ask)

    elif align_ask == 'n' or align_ask == 'no':
        print 'Bye then!'
        break
    else:
        print 'Sorry, {0} is a strange answer that I do not understand. Try again!'.format(align_ask)