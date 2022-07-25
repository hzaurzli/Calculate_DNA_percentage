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
        li = list_path[0]
        output_file = li.split('.')[0]
        output_file = output_file.split('_')[0:len(output_file) - 3]
        output_file = '_'.join(output_file)
        path = sub.getoutput('pwd') + '/'
    else:
        lines = ""
        for i in range(0, len(list_path) - 1):
            line = "/" + list_path[i]
            lines = lines + line
        path = sub.getoutput('pwd') + '/'
        li = list_path[len(list_path) - 1]
        if len(li.split('.')) == 2:
            output_file = li.split('.')[0]
            output_file = output_file.split('_')
            output_file = output_file[0:len(output_file)-1]
            output_file = '_'.join(output_file)
            os.system("cat %s %s | sed -n '1~4s/^@/>/p;2~4p' > %s" % (fq1, fq2, path + output_file + '.fa'))

        if len(li.split('.')) == 3 and li.split('.')[2] == 'gz':
            output_file = li.split('.')[0]
            output_file = output_file.split('_')
            output_file = output_file[0:len(output_file) - 1]
            output_file = '_'.join(output_file)
            os.system("zcat %s %s | sed -n '1~4s/^@/>/p;2~4p' > %s" % (fq1, fq2, path + output_file + '.fa'))

def memory(infile,m,name):
    m = m[0:len(m) - 1]
    m = ''.join(m)

    if 0 < int(m) < 20 or int(m) == 20:
        n = 30
        fa = infile
        nrow = sub.getoutput('cat %s | wc -l' % (fa))
        a = round(int(nrow) / n, 0)
        dir = sub.getoutput('pwd')
        if os.path.isdir(dir + '/' + name + '_index') == True:
            os.system('rm -r %s' % (dir + '/' + name + '_index'))
            os.mkdir(dir + '/' + name + '_index')
        else:
            os.mkdir(dir + '/' + name + '_index')
        for i in range(0, int(nrow), int(a)):
            spl = str(format(i + 1, '.0f')) + ',' + str(format(i + a, '.0f')) + 'p'
            if i + a > int(nrow):
                spl = str(format(i + 1, '.0f')) + ',' + str(format(nrow)) + 'p'
            # print(spl)
            os.system("sed -n %s %s > %s" % (spl, fa, dir + '/' + name + '_index/' + name + '_' + spl + '.index'))

    elif 20 < int(m) < 40 or int(m) == 40:
        n = 25
        fa = infile
        nrow = sub.getoutput('cat %s | wc -l' % (fa))
        a = round(int(nrow) / n, 0)
        dir = sub.getoutput('pwd')
        if os.path.isdir(dir + '/' + name + '_index') == True:
            os.system('rm -r %s' % (dir + '/' + name + '_index'))
            os.mkdir(dir + '/' + name + '_index')
        else:
            os.mkdir(dir + '/' + name + '_index')
        for i in range(0, int(nrow), int(a)):
            spl = str(format(i + 1, '.0f')) + ',' + str(format(i + a, '.0f')) + 'p'
            if i + a > int(nrow):
                spl = str(format(i + 1, '.0f')) + ',' + str(format(nrow)) + 'p'
            # print(spl)
            os.system("sed -n %s %s > %s" % (spl, fa, dir + '/' + name + '_index/' + name + '_' + spl + '.index'))

    elif 40 < int(m) < 60 or int(m) == 60:
        n = 15
        fa = infile
        nrow = sub.getoutput('cat %s | wc -l' % (fa))
        a = round(int(nrow) / n, 0)
        dir = sub.getoutput('pwd')
        if os.path.isdir(dir + '/' + name + '_index') == True:
            os.system('rm -r %s' % (dir + '/' + name + '_index'))
            os.mkdir(dir + '/' + name + '_index')
        else:
            os.mkdir(dir + '/' + name + '_index')
        for i in range(0, int(nrow), int(a)):
            spl = str(format(i + 1, '.0f')) + ',' + str(format(i + a, '.0f')) + 'p'
            if i + a > int(nrow):
                spl = str(format(i + 1, '.0f')) + ',' + str(format(nrow)) + 'p'
            # print(spl)
            os.system("sed -n %s %s > %s" % (spl, fa, dir + '/' + name + '_index/' + name + '_' + spl + '.index'))

    elif 40 < int(m) < 60 or int(m) == 60:
        n = 10
        fa = infile
        nrow = sub.getoutput('cat %s | wc -l' % (fa))
        a = round(int(nrow) / n, 0)
        dir = sub.getoutput('pwd')
        if os.path.isdir(dir + '/' + name + '_index') == True:
            os.system('rm -r %s' % (dir + '/' + name + '_index'))
            os.mkdir(dir + '/' + name + '_index')
        else:
            os.mkdir(dir + '/' + name + '_index')
        for i in range(0, int(nrow), int(a)):
            spl = str(format(i + 1, '.0f')) + ',' + str(format(i + a, '.0f')) + 'p'
            if i + a > int(nrow):
                spl = str(format(i + 1, '.0f')) + ',' + str(format(nrow)) + 'p'
            # print(spl)
            os.system("sed -n %s %s > %s" % (spl, fa, dir + '/' + name + '_index/' + name + '_' + spl + '.index'))

    elif int(m) > 60:
        n = 5
        fa = infile
        nrow = sub.getoutput('cat %s | wc -l' % (fa))
        a = round(int(nrow) / n, 0)
        dir = sub.getoutput('pwd')
        if os.path.isdir(dir + '/' + name + '_index') == True:
            os.system('rm -r %s' % (dir + '/' + name + '_index'))
            os.mkdir(dir + '/' + name + '_index')
        else:
            os.mkdir(dir + '/' + name + '_index')
        for i in range(0, int(nrow), int(a)):
            spl = str(format(i + 1, '.0f')) + ',' + str(format(i + a, '.0f')) + 'p'
            if i + a > int(nrow):
                spl = str(format(i + 1, '.0f')) + ',' + str(format(nrow)) + 'p'
            # print(spl)
            os.system("sed -n %s %s > %s" % (spl, fa, dir + '/' + name + '_index/' + name + '_' + spl + '.index'))


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


def clean_fa_gz(infile,outfile):
    import gzip
    with gzip.open(infile,'rt') as f:
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


def k_mers(fa,k,s,out):
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
    result.to_csv(out +'_tmp.csv')
    os.system("sed -i '1d' %s" % (out +'_tmp.csv'))

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
    parser = argparse.ArgumentParser(description="kmers count")
    parser.add_argument("-fq1", "--fq_1", required=False, type=str, help="Input Fastq1")
    parser.add_argument("-fq2", "--fq_2", required=False, type=str, help="Input Fastq2")
    parser.add_argument("-fa", "--fasta", required=False, type=str, help="Input Fasta")
    parser.add_argument("-k", "--k_num", required=True, type=str, help="kmers number")
    parser.add_argument("-s", "--shift", required=True, type=str, help="kmers shift number")
    parser.add_argument("-m", "--memory", required=False, type=str, help="limition,unit 'g'")
    Args = parser.parse_args()

    if Args.memory == None:
        if Args.fq_1 != None and Args.fq_2 != None and Args.fasta == None:
            start = time.time()

            file_path = Args.fq_1
            list_path = file_path.split('/')
            list_path = [i for i in list_path if i != '']
            if len(list_path) == 1:
                li = list_path[0]
                output_file = li.split('.')[0]
                output_file = output_file.split('_')
                output_file = output_file[0:len(output_file) - 1]
                output_file = '_'.join(output_file)
                path = sub.getoutput('pwd') + '/'
            else:
                lines = ""
                for i in range(0, len(list_path) - 1):
                    line = "/" + list_path[i]
                    lines = lines + line
                path = sub.getoutput('pwd') + '/'
                li = list_path[len(list_path) - 1]
                output_file = li.split('.')[0]
                output_file = output_file.split('_')
                output_file = output_file[0:len(output_file) - 1]
                output_file = '_'.join(output_file)

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
            k_mers(fa=path + output_file + '.fa', k=Args.k_num, s=Args.shift,out=path + output_file)
            sort_table(input=path + output_file + '_tmp.csv',
                       output=path + output_file + '_k' + Args.k_num + '_s' + Args.shift + '.csv')
            os.remove(path + output_file + '_tmp.csv')
            os.remove(path + output_file + '.fa')
            end = time.time()
            print(str(end - start) + 's')

        elif Args.fq_1 == None and Args.fq_2 == None and Args.fasta != None:
            start = time.time()

            file_path = Args.fasta
            list_path = file_path.split('/')
            list_path = [i for i in list_path if i != '']
            if len(list_path) == 1:
                li = list_path[0]
                suffix = li.split('.')[1]
                output_file = li.split('.')[0]
                path = sub.getoutput('pwd') + '/'
            else:
                lines = ""
                for i in range(0, len(list_path) - 1):
                    line = "/" + list_path[i]
                    lines = lines + line
                path = sub.getoutput('pwd') + '/'
                li = list_path[len(list_path) - 1]
                suffix = li.split('.')[1]
                output_file = li.split('.')[0]

            if Args.fasta[0:2] == './':
                dir = os.path.abspath(Args.fasta)
            elif Args.fasta[0:1] == '/':
                dir = os.path.abspath('.' + Args.fasta)
            elif Args.fasta[0:1] != './':
                dir = os.path.abspath('./' + Args.fasta)
            elif Args.fasta[0:3] == '../':
                dir = os.path.abspath(Args.fasta)

            if len(li.split('.')) == 3 and li.split('.')[2] == 'gz':
                clean_fa_gz(infile=dir, outfile=path + output_file + '_clean.fa')
            elif len(li.split('.')) == 2:
                clean_fa(infile=dir, outfile=path + output_file + '_clean.fa')
            k_mers(fa=path + output_file + '_clean.fa', k=Args.k_num, s=Args.shift,out=path + output_file)
            sort_table(input=path + output_file + '_tmp.csv',
                       output=path + output_file + '_k' + Args.k_num + '_s' + Args.shift + '.csv')

            os.remove(path + output_file + '_tmp.csv')
            os.remove(path + output_file + '_clean.fa')
            end = time.time()
            print(str(end - start) + 's')

        else:
            raise "Please add correct parameters!!!"

    if Args.memory != None:
        if Args.fq_1 != None and Args.fq_2 != None and Args.fasta == None:
            start = time.time()

            file_path = Args.fq_1
            list_path = file_path.split('/')
            list_path = [i for i in list_path if i != '']
            if len(list_path) == 1:
                li = list_path[0]
                output_file = li.split('.')[0]
                output_file = output_file.split('_')
                output_file = output_file[0:len(output_file) - 1]
                output_file = '_'.join(output_file)
                path = sub.getoutput('pwd') + '/'
            else:
                lines = ""
                for i in range(0, len(list_path) - 1):
                    line = "/" + list_path[i]
                    lines = lines + line
                path = sub.getoutput('pwd') + '/'
                li = list_path[len(list_path) - 1]
                output_file = li.split('.')[0]
                output_file = output_file.split('_')
                output_file = output_file[0:len(output_file) - 1]
                output_file = '_'.join(output_file)

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
            memory(path + output_file + '.fa',Args.memory,output_file)
            path_index = path + output_file + '_index'
            files = os.listdir(path_index)
            for file in files:
                k_mers(fa=path_index + '/' + file, k=Args.k_num, s=Args.shift,out=path_index + '/' + file)
                sort_table(input=path_index + '/' + file + '_tmp.csv',
                           output=path_index + '/' + file + '_k' + Args.k_num + '_s' + Args.shift + '.csv')
                os.remove(path_index + '/' + file + '_tmp.csv')
                os.remove(path_index + '/' + file)

            lis = []
            files_csv = os.listdir(path_index)
            df1 = pd.read_csv(os.path.join(path_index, files_csv[0]), header=None)
            e = files[0].split('.')[0]
            lis.append('seq')
            lis.append(e)
            df1.columns = ['seq', 'num']
            for i in files_csv[1:]:
                df2 = pd.read_csv(os.path.join(path_index, i), header=None)
                i = i.split('.')[0]
                lis.append(i)
                df2.columns = ['seq', 'num']
                df1 = pd.merge(df1, df2, on='seq', how='outer')

            del df2
            df1.columns = lis
            df1 = df1.set_index('seq', drop=True, append=False,
                                inplace=False, verify_integrity=False)
            df1 = df1.fillna(0)
            df1['row_sum'] = df1.apply(lambda x: x.sum(), axis=1)
            df1.sort_index(inplace=True)
            df1['row_sum'].to_csv(path + output_file + '_k' + Args.k_num + '_s' + Args.shift + '.csv',
                                  header=0,index=1,float_format='%.0f')

            os.system('rm -r %s' % (path + output_file + '_index'))
            os.remove(path + output_file + '.fa')
            end = time.time()
            print(str(end - start) + 's')

        elif Args.fq_1 == None and Args.fq_2 == None and Args.fasta != None:
            start = time.time()

            file_path = Args.fasta
            list_path = file_path.split('/')
            list_path = [i for i in list_path if i != '']
            if len(list_path) == 1:
                li = list_path[0]
                suffix = li.split('.')[1]
                output_file = li.split('.')[0]
                path = sub.getoutput('pwd') + '/'
            else:
                lines = ""
                for i in range(0, len(list_path) - 1):
                    line = "/" + list_path[i]
                    lines = lines + line
                path = sub.getoutput('pwd') + '/'
                li = list_path[len(list_path) - 1]
                suffix = li.split('.')[1]
                output_file = li.split('.')[0]

            if Args.fasta[0:2] == './':
                dir = os.path.abspath(Args.fasta)
            elif Args.fasta[0:1] == '/':
                dir = os.path.abspath('.' + Args.fasta)
            elif Args.fasta[0:1] != './':
                dir = os.path.abspath('./' + Args.fasta)
            elif Args.fasta[0:3] == '../':
                dir = os.path.abspath(Args.fasta)

            if len(li.split('.')) == 3 and li.split('.')[2] == 'gz':
                clean_fa_gz(infile=dir, outfile=path + output_file + '_clean.fa')
            elif len(li.split('.')) == 2:
                clean_fa(infile=dir, outfile=path + output_file + '_clean.fa')

            memory(path + output_file + '_clean.fa', Args.memory, output_file)
            path_index = path + output_file + '_index'
            files = os.listdir(path_index)
            for file in files:
                k_mers(fa=path_index + '/' + file, k=Args.k_num, s=Args.shift, out=path_index + '/' + file)
                sort_table(input=path_index + '/' + file + '_tmp.csv',
                           output=path_index + '/' + file + '_k' + Args.k_num + '_s' + Args.shift + '.csv')
                os.remove(path_index + '/' + file + '_tmp.csv')
                os.remove(path_index + '/' + file)

            lis = []
            files_csv = os.listdir(path_index)
            df1 = pd.read_csv(os.path.join(path_index, files_csv[0]), header=None)
            e = files[0].split('.')[0]
            lis.append('seq')
            lis.append(e)
            df1.columns = ['seq', 'num']
            for i in files_csv[1:]:
                df2 = pd.read_csv(os.path.join(path_index, i), header=None)
                i = i.split('.')[0]
                lis.append(i)
                df2.columns = ['seq', 'num']
                df1 = pd.merge(df1, df2, on='seq', how='outer')

            del df2
            df1.columns = lis
            df1 = df1.set_index('seq', drop=True, append=False,
                                inplace=False, verify_integrity=False)
            df1 = df1.fillna(0)
            df1['row_sum'] = df1.apply(lambda x: x.sum(), axis=1)
            df1.sort_index(inplace=True)
            df1['row_sum'].to_csv(path + output_file + '_k' + Args.k_num + '_s' + Args.shift + '.csv',
                                  header=0, index=1, float_format='%.0f')

            os.system('rm -r %s' % (path + output_file + '_index'))
            os.remove(path + output_file + '_clean.fa')
            end = time.time()
            print(str(end - start) + 's')

        else:
            raise "Please add correct parameters!!!"


