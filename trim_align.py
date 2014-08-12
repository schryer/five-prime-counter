import os
import sys
import glob
import time
import textwrap
import argparse

import bz2file
import gzip


def make_argument_parser():
    '''Returns argument parser for this script.
    '''
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=textwrap.dedent('''
                                     This script trims sequences from an input file and aligns these to a reference genome.                                     
                                     '''),
                                     fromfile_prefix_chars='@')

    dpg = parser.add_argument_group('Directory and file parameters')
        
    dpg.add_argument('-r', '--reference-genome', 
                     dest='reference_genome', default=None, metavar='S', 
                     help='Reference genome file.')
    
    dpg.add_argument('-i', '--input-file', 
                     dest='input_filename', default=None, metavar='S', 
                     help='Input filename containing fasta sequences.')
        
    return parser


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

def perform_trim(read_file_path, output_filename):
    parser = ParseFastQ(read_file_path)    

    print('Performing trim. Making trim file: {}'.format(output_filename))
    output_file = open(output_filename, 'w')

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
            output_file.write("%s\n" % line)

def index_genome(reference_genome):
    cmd = "bwa index -a is {0}".format(reference_genome)
    print('Running external command: {}'.format(cmd))
    output = os.system(cmd)

def perform_alignment(reference_genome, read_filename, output_filename):

    # Test if index files exist.
    index_list = glob.glob('{}*'.format(reference_genome))
    if len(index_list) != 6:
        print('No index files found. Generating...')
        cmd = "bwa index {}".format(reference_genome)
        print('Running external command: {}'.format(cmd))
        output = os.system(cmd)

    # Run the alignment.
    cmd = "bwa mem {} {} > {}".format(reference_genome, read_filename, output_filename)
    print('Running external command: {}'.format(cmd))
    output = os.system(cmd)

    print('Created alignment file: {}'.format(output_filename))


def process_arguments(args):

    # Get the root file name for the ref. genome
    base_name = os.path.basename(args.input_filename)

    # Get the root and extention of the base_name
    root_ext = os.path.splitext(base_name)

    # Make the trimmed base filename based on the read genome name
    trimmed_output_base_filename = root_ext[0] + root_ext[1].replace('.', '_trimmed.')

    # Make alignment filename.
    alignment_output_base_filename = root_ext[0] + '_aligned.sam'

    # Put these in the generation dir...
    trimmed_output_filename = os.path.join('generated', trimmed_output_base_filename)
    alignment_output_filename = os.path.join('generated', alignment_output_base_filename)

    # Perform the trim operation.
    perform_trim(args.input_filename, trimmed_output_filename)

    # Perform the alignment.
    perform_alignment(args.reference_genome, trimmed_output_filename, alignment_output_filename)

            
if __name__ == '__main__':

    p = make_argument_parser()
    args = p.parse_args()
    process_arguments(args)

