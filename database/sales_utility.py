import pandas as pd
import numpy as np
from database import db_utility
from database import transforms
import os

#df = transforms.get_files_data()
#print(df.shape)
if os.path.exists('./data/final_report.csv'):
    df = pd.read_csv('./data/final_report.csv')
    df.drop('Unnamed: 0', axis=1, inplace=True)
else:
    print('Upload data..')
    df = transforms.get_files_data()

def get_df():
    return df

#def get_df():
#    upload_dir = './data/upload_files/'
#    df = transforms.get_files_data()
#    return df


def year_wise_df(year_val, cat_val):
    if (year_val == 'ALL') & (cat_val == 'ALL'):
        return df
    elif (year_val != 'ALL') & (cat_val == 'ALL'):
        temp_df = df[(df['year']==year_val)]
        temp_df = temp_df[['item_type','year','month','SALE AMT.']]
        return temp_df
    elif (year_val != 'ALL') & (cat_val != 'ALL'):
        temp_df = df.loc[(df['year']==year_val) & (df['item_type']==cat_val)]
        return temp_df[['item_type','year','month','SALE AMT.']]
    elif (year_val == 'ALL') & (cat_val != 'ALL'):
        temp_df = df[df['item_type']==cat_val]
        return temp_df[['item_type','year','month','SALE AMT.']]
    #else:
    #    temp_df = df[(df['year']==year_val)][['year','month','SALE AMT.']]
    #    return temp_df[['year','month','SALE AMT.']]

def year_wise_df_1(year_val):
    if (year_val == 'ALL'):
        return df
    else:
        temp_df = df[(df['year']==year_val)]
        df_monthly_sales = temp_df.groupby(['year','month'])[['SALE AMT.','item_type']].sum().reset_index()
        df_monthly_sales['SALE AMT.'] = round(df_monthly_sales['SALE AMT.'])
        return df_monthly_sales

def cat_wise_df_1(cat_val):
    if (cat_val == 'ALL'):
        return df
    else:
        temp_df = df[df['item_type']==cat_val]
        df_monthly_sales = temp_df.groupby(['year','month'])[['SALE AMT.','item_type']].sum().reset_index()
        df_monthly_sales['SALE AMT.'] = round(df_monthly_sales['SALE AMT.'])
        return df_monthly_sales

def get_year_wise_sales(y_value, cat_val):
    df = year_wise_df(y_value, cat_val)
    df_monthly_sales = df.groupby(['year','month'])[['SALE AMT.','item_type']].sum().reset_index()
    df_monthly_sales['SALE AMT.'] = round(df_monthly_sales['SALE AMT.'])
    return df_monthly_sales

#-------------------------------------------------------------------------
