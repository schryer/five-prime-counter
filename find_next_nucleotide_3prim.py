import pysam
from Bio import SeqIO
for seq_record in SeqIO.parse("refgenome.fasta", "fasta"):
    sequence=seq_record.seq
    

n = 0
for read in samfile:
    if read.is_reverse == True:
        check_pos = read.pos - 1
        if sequence[check_pos] == 'A':
            print 'fuckered'
        else:
            print 'unfuckered'
    else:
        check_pos = read.pos + read.qlen
        if sequence[check_pos] == 'A':
            print 'fuckered'
        else:
            print 'unfuckered'
        

    n += 1
    if n < 100:
        continue
    else:
        break