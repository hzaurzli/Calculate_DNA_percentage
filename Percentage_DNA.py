#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Percentage_DNA.py 
#
#  Copyright 2022 Small runze
#  <small.runze@gmail.com> Small runze
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., Xishuangbanna tropical botanical garden.




import argparse
import os,sys,csv
import subprocess as sub
from subprocess import *
import pandas as pd


def fq2fa(fq1, fq2):
    file_path = Args.fq_1
    list_path = file_path.split('/')
    list_path = [i for i in list_path if i != '']
    if len(list_path) == 1:
        output_file = list_path[0]
        output_file = output_file.split('.')[0]
        output_file = output_file.split('_')[0]
        path = sub.getoutput('pwd') + '/'
    else:
        lines = ""
        for i in range(0, len(list_path) - 1):
            line = "/" + list_path[i]
            lines = lines + line
        path = lines + '/'
        output_file = list_path[len(list_path) - 1]
        output_file = output_file.split('.')[0]
        output_file = output_file.split('_')[0]
    os.system('cat %s %s > %s' % (fq1,fq2,Args.workdir + output_file +'.fq'))
    os.system("sed -n '1~4s/^@/>/p;2~4p' %s > %s" % (Args.workdir + output_file +'.fq',
                                                    Args.workdir + output_file +'.fa'))


def k_mers(fa,k,s):
    with open(fa, "r") as sequences:
        lines = sequences.readlines()
        k_seq = int(k)
        seq_list = []
        for line in lines:
            if line.startswith(">"):
                pass
            else:
                for i in range(0, len(line) - k_seq - 1, int(s)+1):
                    seq = line[i:i + k_seq]
                    seq_list.append(seq)

    result = pd.value_counts(seq_list)
    result.to_csv('./' + output_file +'_tmp.csv')
    os.system("sed -i '1d' %s" % ('./' + output_file +'_tmp.csv'))

def DNA_reversal_complement(sequence):

    comp_dict = {
        "A":"T",
        "T":"A",
        "G":"C",
        "C":"G",
        "N":"N"
    }

    sequence_list = list(sequence)
    sequence_list = [comp_dict[base] for base in sequence_list]
    string = ''.join(sequence_list)
    return string[::-1]

def sort_table(input,output):
    dict_unsort = {}

    with open(input, mode='r') as inp:
        reader = csv.reader(inp)
        dict_unsort = {rows[0]: rows[1] for rows in reader}

    new_sys = sorted(dict_unsort.items(),key=lambda x:x[0])
    dict_sort = dict(new_sys)
    dict_sort_1 = dict(new_sys)

    with open(output, mode='w') as f:
        for i in dict_sort.keys():
            if 'N' in i:
                pass
            else:
                rev_seq = DNA_reversal_complement(i)
                if i in dict_sort_1.keys() and rev_seq in dict_sort_1.keys():
                    line = i + ',' + str(int(dict_sort_1[i]) + int(dict_sort_1[rev_seq])) + '\n'
                    del dict_sort_1[rev_seq]
                    f.write(line)
                elif i in dict_sort_1.keys() and rev_seq not in dict_sort_1.keys():
                    line = i + ',' + str(int(dict_sort_1[i])) + '\n'
                    f.write(line)
    f.close()


class mapping:
    def __init__(self):
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
    parser.add_argument("-rg", "--ref_genome", required=False, type=str, help="Reference genome")
    parser.add_argument("-ri", "--ref_index", required=False, type=str,
                        help="Reference genome index,if you use -rg please add genome index's suffix;eg 'genome';if not,please add path and suffix;eg '/.../index/genome'")
    parser.add_argument("-wkdir", "--workdir", required=True, type=str, help="Work dir")
    parser.add_argument("-k", "--k_num", required=True, type=str, help="kmers number")
    parser.add_argument("-fq1", "--fq_1", required=True, type=str, help="Input Fastq1")
    parser.add_argument("-fq2", "--fq_2", required=True, type=str, help="Input Fastq2")
    Args = parser.parse_args()

    mp = mapping()
    if Args.ref_genome == None:
        if Args.ref_index == None:
            raise 'Please add reference index path!!!'
        else:
            # step1 aliment
            file_path = Args.fq_1
            list_path = file_path.split('/')
            list_path = [i for i in list_path if i != '']
            if len(list_path) == 1:
                output_file = list_path[0]
                output_file = output_file.split('.')[0]
                output_file = output_file.split('_')[0]
                path = sub.getoutput('pwd') + '/'
            else:
                lines = ""
                for i in range(0, len(list_path) - 1):
                    line = "/" + list_path[i]
                    lines = lines + line
                path = lines + '/'
                output_file = list_path[len(list_path) - 1]
                output_file = output_file.split('.')[0]
                output_file = output_file.split('_')[0]

            if os.path.isdir(Args.workdir) == True:
                pass
            else:
                os.mkdir(Args.workdir)
            sam = Args.workdir + output_file + '.sam'

            log = Args.workdir + 'log/' + output_file + '.log'
            if os.path.isdir(Args.workdir + 'log/') == True:
                pass
            else:
                os.mkdir(Args.workdir + 'log/')
            cmd_2 = mp.aliment(Args.ref_index, Args.fq_1, Args.fq_2, sam, log)
            mp.run(cmd=cmd_2)

            # step2 sam2bam
            bam = Args.workdir + output_file + '.bam'
            cmd_3 = mp.sam2bam(sam, bam)
            mp.run(cmd=cmd_3)

            # step3 pick pair mapped reads
            pair_mapped_bam = Args.workdir + output_file + '_pair_mapped.bam'
            cmd_4 = mp.pair_mapped(bam, pair_mapped_bam)
            mp.run(cmd=cmd_4)

            # step4 pick pair mapped reads
            fq1 = Args.workdir + 'pair_mapped_' + output_file + '_R1.fq'
            fq2 = Args.workdir + 'pair_mapped_' + output_file + '_R2.fq'
            cmd_5 = mp.bam2fastq(pair_mapped_bam, fq1, fq2)
            mp.run(cmd=cmd_5)

            # step5 fq2fa and combine
            print('fastq to fasta!!!')
            fq2fa(fq1, fq2)

            # step6 kmers statstic
            print('kmers table!!!')
            k_mers(fa=Args.workdir + output_file + '.fa', k=Args.k_num,s=Args.shift)
            sort_table(input=Args.workdir + output_file +'_tmp.csv',
                       output=Args.workdir + output_file +'.csv')

    else:
        if Args.ref_index == None:
            raise 'Please add reference index path!!!'
        else:
            # step1 make reference index
            if os.path.isdir(Args.workdir) == True:
                pass
            else:
                os.mkdir(Args.workdir)

            if os.path.isdir(Args.workdir + Args.ref_index + '_index/') == True:
                pass
            else:
                os.mkdir(Args.workdir + Args.ref_index + '_index/')

            cmd_1 = mp.make_index(Args.ref_genome,
                                  Args.workdir + Args.ref_index + '_index/' + Args.ref_index)
            mp.run(cmd=cmd_1)

            # step2 aliment
            file_path = Args.fq_1
            list_path = file_path.split('/')
            list_path = [i for i in list_path if i != '']
            if len(list_path) == 1:
                output_file = list_path[0]
                output_file = output_file.split('.')[0]
                output_file = output_file.split('_')[0]
                path = sub.getoutput('pwd') + '/'
            else:
                lines = ""
                for i in range(0, len(list_path) - 1):
                    line = "/" + list_path[i]
                    lines = lines + line
                path = lines + '/'
                output_file = list_path[len(list_path) - 1]
                output_file = output_file.split('.')[0]
                output_file = output_file.split('_')[0]

            sam = Args.workdir + output_file + '.sam'

            log = Args.workdir + 'log/' + output_file + '.log'
            if os.path.isdir(Args.workdir + 'log/') == True:
                pass
            else:
                os.mkdir(Args.workdir + 'log/')

            cmd_2 = mp.aliment(Args.workdir + Args.ref_index + '_index/' + Args.ref_index,
                               Args.fq_1, Args.fq_2, sam, log)
            mp.run(cmd=cmd_2)

            # step3 sam2bam
            bam = Args.workdir + output_file + '.bam'
            cmd_3 = mp.sam2bam(sam, bam)
            mp.run(cmd=cmd_3)

            # step4 pick pair mapped reads
            pair_mapped_bam = Args.workdir + output_file + '_pair_mapped.bam'
            cmd_4 = mp.pair_mapped(bam, pair_mapped_bam)
            mp.run(cmd=cmd_4)

            # step5 pick pair mapped reads
            fq1 = Args.workdir + 'pair_mapped_' + output_file + '_R1.fq'
            fq2 = Args.workdir + 'pair_mapped_' + output_file + '_R2.fq'
            cmd_5 = mp.bam2fastq(pair_mapped_bam, fq1, fq2)
            mp.run(cmd=cmd_5)

            # step6 fq2fa and combine
            print('fastq to fasta!!!')
            fq2fa(fq1,fq2)

            # step7 kmers statstic
            print('kmers table!!!')
            k_mers(fa=Args.workdir + output_file +'.fa',k=Args.k_num,s=Args.shift)
            sort_table(input=Args.workdir + output_file + '_tmp.csv',
                       output=Args.workdir + output_file + '.csv')


    os.remove(sam)
    os.remove(bam)
    os.remove(pair_mapped_bam)
    os.remove(Args.workdir + output_file + '.fa')
    os.remove(Args.workdir + output_file + '.fq')
    os.remove(Args.workdir + output_file + '_tmp.csv')






