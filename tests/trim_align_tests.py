import os

def test_trim_align_script():

    cmd = 'python trim_align.py -i fastq/fastq_test.fastq -r fastq/refgenome.fasta'
    output = os.system(cmd)

    assert os.path.exists('generated/fastq_test_aligned.sam')