import pandas as pd
import dash
import os

upload_dir = './data/upload_files/'

def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            return f

def get_files_data():

    upload_dir = './data/upload_files/'
    li = []

    for filename in os.listdir(upload_dir):
        if not filename.startswith('.'):
            if (filename.startswith('sale')) & (filename.endswith('.xls')):
                path = os.path.join(upload_dir, filename)
                df = pd.read_excel(path)
                li.append(df)
        else:
            return 'File Name Should be Start with sale & only allowed .xls file'

    if len(li)!=0:
        combine = pd.concat(li, axis=0, ignore_index=True)
        combine.drop(['BARCODE','DIS%','SCH%','SCH AMT%'], axis=1, inplace=True)
        combine['DATE'] = pd.to_datetime(combine['DATE'], format='%d/%m/%Y')
        combine.drop(combine[combine['DATE'].isnull()].index, inplace = True)

        combine['year'] = combine.DATE.dt.year
        combine['month'] = combine.DATE.dt.month
        combine['day'] = combine.DATE.dt.day

        item_type = []

        for i in combine['PRODUCT NAME']:
            if '.' not in i:
                item_type.append('other')
            else:
                split_val = i.split('.')[0]
                if split_val == 'M':
                    item_type.append('male')
                elif split_val == 'L':
                    item_type.append('female')
                elif split_val == 'B':
                    item_type.append('boy')
                elif split_val == 'G':
                    item_type.append('girl')
        combine['item_type'] = item_type
    return combine
