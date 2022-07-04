import os
import subprocess as sub

samples = []
for i in os.listdir("/data/home/huanfan/runze/mix_cleandata/"):
    i = i.split("_")
    sample = i[0]
    samples.append(sample)
    samples = list(set(samples))

print(samples)

for i in samples:
    with open("/data/home/huanfan/runze/codes/" + i + ".sh", "w") as w:
        line = "#!/bin/bash" + "\n"
        line = line + "/data/home/huanfan/miniconda3/bin/python3 "
        line = line + "/data/home/huanfan/pycharm/venv/Percentage_DNA.py -wkdir ~/runze/test/ "
        line = line + "-ri ~/runze/ref/index/chloroplast -fq1 ~/runze/mix_cleandata/" + i + "_R1.fq.gz "
        line = line + "-fq2 ~/runze/mix_cleandata/" + i + "_R2.fq.gz -k 8"
        w.write(line)



import os
import subprocess as sub

samples = []
for i in os.listdir("/data/home/huanfan/runze/cleandata/"):
    i = i.split("_")
    sample = i[0]
    samples.append(sample)
    samples = list(set(samples))

print(samples)

for i in samples:
    with open("/data/home/huanfan/runze/codes_single/job_" + i + ".sh", "w") as w:
        line = "#!/bin/bash" + "\n"
        line = line + "/data/home/huanfan/miniconda3/bin/python3 "
        line = line + "/data/home/huanfan/pycharm/venv/Percentage_DNA.py -wkdir ~/runze/test_single/ "
        line = line + "-rg ~/runze/ref/" + i + '.fasta '
        line = line + "-ri "  + i + " -fq1 ~/runze/cleandata/" + i + "_R1.fq.gz "
        line = line + "-fq2 ~/runze/cleandata/" + i + "_R2.fq.gz -k 8"
        w.write(line)

