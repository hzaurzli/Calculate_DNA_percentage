# Calculate_DNA_percentage
## How to use this software
**step 1:**

If you don't establish genome'index:
```
/data/home/huanfan/miniconda3/bin/python3 /data/home/huanfan/pycharm/venv/Percentage_DNA.py -wkdir /test/ -rg <refence genome;eg /.../genome.fa> 
-ri <refence index;eg /.../index/> -fq1 <fastq1> -fq2 <fastq2> -k 8
```

If you establish genome'index:
```
/data/home/huanfan/miniconda3/bin/python3 /data/home/huanfan/pycharm/venv/Percentage_DNA.py -wkdir /test/ -ri <refence index adding suffix;eg /.../index/genome> -fq1 <fastq1> -fq2 <fastq2> -k 8
```
Notice:format of fastq is ```<file name>```_R1.fq or ```<file name>```_R2.fq

