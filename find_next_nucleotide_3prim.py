import pysam
from Bio import SeqIO
for seq_record in SeqIO.parse("refgenome.fasta", "fasta"):
    sequence=seq_record.seq
samfile = pysam.Samfile("aligned.sam", "r" )

output_correct=pysam.Samfile('aligned_right.sam', 'w', template = samfile)
output_sketchy=pysam.Samfile('aligned_sketchy.sam', 'w', template = samfile)

n = 0
for read in samfile:
    if read.is_reverse == True:
        check_pos = read.pos - 1
        if sequence[check_pos] == 'T':
            output_sketchy.write(read)
        else:
            output_correct.write(read)
    else:
        check_pos = read.pos + read.qlen
        if sequence[check_pos] == 'T':
            output_sketchy.write(read)
        else:
            output_correct.write(read)
        

    n += 1
    if n < 100:
        continue
    else:
        break