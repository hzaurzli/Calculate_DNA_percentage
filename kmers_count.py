import argparse
import os,sys,csv
import pandas as pd
import subprocess as sub
import time


def fq2fa(fq1, fq2):
    file_path = fq1
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
        path = sub.getoutput('pwd') + '/'
        output_file = list_path[len(list_path) - 1]
        output_file = output_file.split('.')[0]
        output_file = output_file.split('_')[0]

    os.system('cat %s %s > %s' % (fq1,fq2,path + output_file +'.fq'))
    os.system("sed -n '1~4s/^@/>/p;2~4p' %s > %s" % (path + output_file +'.fq',
                                                     path + output_file +'.fa'))
def clean_fa(infile,outfile):
    with open(infile) as f:
        Dict = {}
        for line in f:
            if line[0] == ">":
                key = line.strip()
                Dict[key] = []
            else:
                Dict[key].append(line.strip())

    with open(outfile, 'w') as o:
        for key, value in Dict.items():
            o.write("{}\n{}\n".format(key, ''.join(value)))


def k_mers(fa,k,s):
    with open(fa, "r") as sequences:
        lines = sequences.readlines()
        k_seq = int(k)
        seq_list = []
        for line in lines:
            if line.startswith(">"):
                pass
            else:
                for i in range(0, len(line) - k_seq, int(s)+1):
                    seq = line[i:i + k_seq]
                    seq_list.append(seq)

    result = pd.value_counts(seq_list)
    result.to_csv(path + output_file +'_tmp.csv')
    os.system("sed -i '1d' %s" % (path + output_file +'_tmp.csv'))


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

    dict_unsort_1 = {}

    for i in dict_unsort.keys():
        if 'N' in i:
            pass
        else:
            rev_seq = DNA_reversal_complement(i)
            if i in dict_unsort.keys() and rev_seq in dict_unsort.keys():
                if i < rev_seq or i == rev_seq:
                    dict_unsort_1[i] = int(dict_unsort[i]) + int(dict_unsort[rev_seq])
                elif i > rev_seq:
                    dict_unsort_1[rev_seq] = int(dict_unsort[i]) + int(dict_unsort[rev_seq])
            elif i in dict_unsort.keys() and rev_seq not in dict_unsort.keys():
                if i < rev_seq or i == rev_seq:
                    dict_unsort_1[i] = int(dict_unsort[i])
                elif i > rev_seq:
                    dict_unsort_1[rev_seq] = int(dict_unsort[i])

    new_sys = sorted(dict_unsort_1.items(), key=lambda x: x[0])
    dict_sort = dict(new_sys)

    df = pd.DataFrame.from_dict(dict_sort,orient='index',columns=['num'])
    df = df.reset_index().rename(columns={'index': 'seq'})
    df.to_csv(output,header=None,index=None)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DNA persentage")
    parser.add_argument("-fq1", "--fq_1", required=False, type=str, help="Input Fastq1")
    parser.add_argument("-fq2", "--fq_2", required=False, type=str, help="Input Fastq2")
    parser.add_argument("-fa", "--fasta", required=False, type=str, help="Input Fasta")
    parser.add_argument("-k", "--k_num", required=True, type=str, help="kmers number")
    parser.add_argument("-s", "--shift", required=True, type=str, help="kmers shift number")
    Args = parser.parse_args()

    if Args.fq_1 != None and Args.fq_2 != None and Args.fasta == None:
        start = time.time()

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
            path = sub.getoutput('pwd') + '/'
            output_file = list_path[len(list_path) - 1]
            output_file = output_file.split('.')[0]
            output_file = output_file.split('_')[0]

        if Args.fq_1[0:2] == './':
            dir_1 = os.path.abspath(Args.fq_1)
        elif Args.fq_1[0:1] == '/':
            dir_1 = os.path.abspath('.' + Args.fq_1)
        elif Args.fq_1[0:1] != './':
            dir_1 = os.path.abspath('./' + Args.fq_1)
        elif Args.fq_1[0:3] == '../':
            dir_1 = os.path.abspath(Args.fq_1)

        if Args.fq_2[0:2] == './':
            dir_2 = os.path.abspath(Args.fq_2)
        elif Args.fq_2[0:1] == '/':
            dir_2 = os.path.abspath('.' + Args.fq_2)
        elif Args.fq_2[0:1] != './':
            dir_2 = os.path.abspath('./' + Args.fq_2)
        elif Args.fq_2[0:3] == '../':
            dir_2 = os.path.abspath(Args.fq_2)

        fq2fa(dir_1, dir_2)
        k_mers(fa= path + output_file + '.fa', k=Args.k_num,s=Args.shift)
        sort_table(input= path + output_file + '_tmp.csv',
                   output= path + output_file + '_k' + Args.k_num + '_s' + Args.shift + '.csv')
        os.remove(path + output_file + '_tmp.csv')
        os.remove(path + output_file +'.fq')
        os.remove(path + output_file + '.fa')

        end = time.time()
        print(str(end-start) + 's')

    elif Args.fq_1 == None and Args.fq_2 == None and Args.fasta != None:
        start = time.time()

        file_path = Args.fasta
        list_path = file_path.split('/')
        list_path = [i for i in list_path if i != '']
        if len(list_path) == 1:
            output_file = list_path[0]
            suffix = output_file.split('.')[1]
            output_file = output_file.split('.')[0]
            output_file = output_file.split('_')[0]
            path = sub.getoutput('pwd') + '/'
        else:
            lines = ""
            for i in range(0, len(list_path) - 1):
                line = "/" + list_path[i]
                lines = lines + line
            path = sub.getoutput('pwd') + '/'
            output_file = list_path[len(list_path) - 1]
            suffix = output_file.split('.')[1]
            output_file = output_file.split('.')[0]
            output_file = output_file.split('_')[0]

        if Args.fasta[0:2] == './':
            dir = os.path.abspath(Args.fasta)
        elif Args.fasta[0:1] == '/':
            dir = os.path.abspath('.' + Args.fasta)
        elif Args.fasta[0:1] != './':
            dir = os.path.abspath('./' + Args.fasta)
        elif Args.fasta[0:3] == '../':
            dir = os.path.abspath(Args.fasta)

        clean_fa(infile=dir,outfile=path + output_file+'_clean.fa')
        k_mers(fa= path + output_file+'_clean.fa', k=Args.k_num, s=Args.shift)
        sort_table(input= path + output_file + '_tmp.csv',
               output= path + output_file + '_k' + Args.k_num + '_s' + Args.shift + '.csv')

        os.remove(path + output_file + '_tmp.csv')
        os.remove(path + output_file+'_clean.fa')
        end = time.time()
        print(str(end - start) + 's')

    else:
        raise "Please add correct parameters!!!"
        
        
