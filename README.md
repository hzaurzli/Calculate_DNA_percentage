# Calculate_DNA_percentage
## How to use this software
**step 1:**

If you don't establish genome's index:
```
/data/home/huanfan/miniconda3/bin/python3 /data/home/huanfan/pycharm/venv/Percentage_DNA.py -wkdir /test/ -rg <refence genome;eg /.../genome.fa> 
-ri <refence index;eg genome(genome is suffix)> -fq1 <fastq1> -fq2 <fastq2> -k 8
```

If you establish genome's index:
```
/data/home/huanfan/miniconda3/bin/python3 /data/home/huanfan/pycharm/venv/Percentage_DNA.py -wkdir /test/ -ri <refence index adding suffix;eg /.../index/genome(genome is suffix)> -fq1 <fastq1> -fq2 <fastq2> -k 8
```
Notice:format of fastq is ```<file name>```_R1.fq or ```<file name>```_R2.fq

**step 2:**
calculate ratio：
```
/data/home/huanfan/miniconda3/envs/R/bin/Rscript deconvolution.R -s /data/home/huanfan/dna_persentage/single_9/ -m /data/home/huanfan/dna_persentage/mix_9/ -o test.txt -p 0

Usage: This Script is a test for arguments!


Options:
        -s SINGLE, --single=SINGLE
                single sequencing data! format .csv

        -m MIX, --mix=MIX
                mix sequencing data! format .csv

        -o OUTPUT, --output=OUTPUT
                ratio of single sample

        -p PERM, --perm=PERM
                number of permutations

        -h, --help
                Show this help message and exit

```
