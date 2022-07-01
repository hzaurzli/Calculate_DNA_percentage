import os
import argparse
import sys
import subprocess as sub
from subprocess import *

# def k_mers():

class mapping:
    def __init__(self, bowtie2_build, bowtie2, samtools, bedtools):
        self.bowtie2_build = '/data/home/huanfan/miniconda3/envs/bowtile2/bin/bowtie2-build'
        self.bowtie2 = '/data/home/huanfan/miniconda3/envs/bowtile2/bin/bowtie2'
        self.samtools = '/data/home/huanfan/miniconda3/envs/bowtile2/bin/samtools'
        self.bedtools = '/data/home/huanfan/miniconda3/envs/bowtile2/bin/bedtools'

    def run(self, cmd, wkdir=None):
        sys.stderr.write("Running %s ...\n" % cmd)
        p = Popen(cmd, shell=True, cwd=wkdir)
        p.wait()
        return p.returncode

    def make_index(self, ref_genome, ref_index):
        cmd = '%s -f %s %s' % (self.bowtie2_build, ref_genome, ref_index)
        return cmd

    def aliment(self, ref_index, fq_1, fq_2, sam, log):
        cmd = '%s -x %s -1 %s -2 %s -S %s 2>%s' % (self.bowtie2, ref_index, fq_1, fq_2, sam, log)
        return cmd

    def sam2bam(self, sam, bam):
        cmd = '%s view -b %s >%s' % (self.samtools, sam, bam)
        return cmd

    def pair_mapped(self, bam, pair_mapped_bam):
        cmd = '%s view -bF 12 %s >%s' % (self.samtools, bam, pair_mapped_bam)
        return cmd

    def bam2fastq(self,pair_mapped_bam,fq1,fq2):
        cmd = '%s bamtofastq -i %s -fq %s -fq2 %s' % (self.bedtools, pair_mapped_bam, fq1, fq2)
        return cmd

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DNA persentage")
    parser.add_argument("-rg", "--ref_genome", required=False, type=str, help="reference genome")
    parser.add_argument("-ri", "--ref_index", required=False, type=str, help="reference genome index")
    parser.add_argument("-wkdir", "--workdir", required=True, type=str, help="work dir")
    parser.add_argument("-fq1", "--fq_1", required=True, type=str, help="Fastq1")
    parser.add_argument("-fq2", "--fq_2", required=True, type=str, help="Fastq2")
    Args = parser.parse_args()

    mp = mapping()
    if Args.ref_genome == None:
        if Args.ref_index == None:
            raise 'Please add reference index path!!!'
        else:
            # step1 aliment
            file_path = Args.fq_1
            list = file_path.split('/')
            list = [i for i in list if i != '']
            if len(list) == 1:
                output_file = list[0]
                output_file = output_file.split('.')[0]
                output_file = output_file.split('_')[0]
                path = sub.getoutput('pwd') + '/'
            else:
                lines = ""
                for i in range(0, len(list) - 1):
                    line = "/" + list[i]
                    lines = lines + line
                path = lines + '/'
                output_file = list[len(list) - 1]
                output_file = output_file.split('.')[0]
                output_file = output_file.split('_')[0]

            os.mkdir(Args.workdir)
            sam = Args.workdir + '/' + output_file + '.sam'

            log = Args.workdir + '/log/' + output_file + '.log'
            os.mkdir(Args.workdir + '/log/')
            cmd_2 = mp.aliment(Args.ref_index, Args.fq_1, Args.fq_2, sam, log)

            # step3 sam2bam
            bam = Args.workdir + '/' + output_file + '.bam'
            cmd_3 = mp.sam2bam(sam, bam)
            mp.run(cmd=cmd_3)

            # step4 pick pair mapped reads
            pair_mapped_bam = Args.workdir + '/' + output_file + '_pair_mapped.bam'
            cmd_4 = mp.pair_mapped(bam, pair_mapped_bam)

            # step5 pick pair mapped reads
            fq1 = Args.workdir + '/pair_mapped_' + output_file + '_R1.fq'
            fq2 = Args.workdir + '/pair_mapped_' + output_file + '_R2.fq'
            cmd_5 = mp.bam2fastq(pair_mapped_bam, fq1, fq2)

    else:
        if Args.ref_index == None:
            raise 'Please add reference index path!!!'
        else:
            # step1 make reference index
            cmd_1 = mp.make_index(Args.ref_genome, Args.ref_index)
            mp.run(cmd=cmd_1)

            # step2 aliment
            file_path = Args.fq_1
            list = file_path.split('/')
            list = [i for i in list if i != '']
            if len(list) == 1:
                output_file = list[0]
                output_file = output_file.split('.')[0]
                output_file = output_file.split('_')[0]
                path = sub.getoutput('pwd') + '/'
            else:
                lines = ""
                for i in range(0, len(list) - 1):
                    line = "/" + list[i]
                    lines = lines + line
                path = lines + '/'
                output_file = list[len(list) - 1]
                output_file = output_file.split('.')[0]
                output_file = output_file.split('_')[0]

            os.mkdir(Args.workdir)
            sam = Args.workdir + '/' + output_file + '.sam'

            log = Args.workdir + '/log/' + output_file + '.log'
            os.mkdir(Args.workdir + '/log/')
            cmd_2 = mp.aliment(Args.ref_index, Args.fq_1, Args.fq_2, sam, log)

            # step3 sam2bam
            bam = Args.workdir + '/' + output_file + '.bam'
            cmd_3 = mp.sam2bam(sam, bam)
            mp.run(cmd=cmd_3)

            # step4 pick pair mapped reads
            pair_mapped_bam = Args.workdir + '/' + output_file + '_pair_mapped.bam'
            cmd_4 = mp.pair_mapped(bam, pair_mapped_bam)

            # step5 pick pair mapped reads
            fq1 = Args.workdir + '/pair_mapped_' + output_file + '_R1.fq'
            fq2 = Args.workdir + '/pair_mapped_' + output_file + '_R2.fq'
            cmd_5 = mp.bam2fastq(pair_mapped_bam, fq1, fq2)

    os.remove(sam)
    os.remove(bam)
    os.remove(pair_mapped_bam)



