import os
import pandas as pd
import argparse


def merge_file(indir,outfile,n):
    lis = []
    file_dir = indir
    files = sorted(os.listdir(file_dir))
    df1 = pd.read_csv(os.path.join(file_dir, files[0]), header=None)
    e = files[0].split('.')[0]
    lis.append('seq')
    lis.append(e)
    df1.columns = ['seq', 'num']

    for i in files[1:]:
        df2 = pd.read_csv(os.path.join(file_dir, i),header=None)
        i = i.split('.')[0]
        lis.append(i)
        df2.columns = ['seq', 'num']
        data = df1 = pd.merge(df1, df2, on='seq', how='outer')

    del df2
    df1.columns = lis
    df1 = df1.set_index('seq', drop=True, append=False,
                        inplace=False, verify_integrity=False)

    data = data.set_index('seq', drop=True, append=False,
                          inplace=False, verify_integrity=False)

    df1 = df1.fillna(0)
    data = data.fillna(0)
    data[data > 0] = 1
    data['row_sum'] = data.apply(lambda x: x.sum(), axis=1)

    ll = data['row_sum'].tolist()
    df1['row_sum'] = ll
    df1 = df1[df1['row_sum'] > int(n) - 1]
    del df1['row_sum']
    df1.round(0)
    df1.sort_index(inplace=True)
    df1.to_csv(outfile,header=1,index=1,sep='\t',float_format='%.0f')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-i", "--indir", required=False, type=str, help="Input")
    parser.add_argument("-o", "--outfile", required=True, type=str, help="Output")
    parser.add_argument("-n", "--num", required=True, type=str, help="")
    Args = parser.parse_args()

    merge_file(Args.indir,Args.outfile,Args.num)