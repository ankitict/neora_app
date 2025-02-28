import pandas as pd
import numpy as np
from database import transforms
import os

upload_dir = './data/upload_files/'
#df = transforms.get_files_data()

df = pd.DataFrame()
if os.path.exists('./data/final_report.csv'):
    df = pd.read_csv('./data/final_report.csv')
    df.drop('Unnamed: 0', axis=1, inplace=True)
else:
    print('Upload data..')
    df = transforms.get_files_data()

def get_df():
    return df

df['DATE'] = pd.to_datetime(df['DATE'])
df.set_index('DATE', inplace=True)

top_product = ''
################################## ------------------ MALE ------------------- ####################################

#Get Top Male Product for Male Dashboard
def get_top_product(value, item_type):
    if value == 'ALL':
        top_male_product = df[(df['item_type']==item_type)]
        final_df = top_male_product.groupby('PRODUCT NAME')[['QTY.']].sum().sort_values('QTY.',
                                                                ascending=False).head(1).reset_index()
        #top_product = final_df['PRODUCT NAME'].values[0]
        return final_df['PRODUCT NAME'].values[0]
    else:
        top_male_product = df[(df['item_type']==item_type) & (df['year']==value)]
        final_df = top_male_product.groupby('PRODUCT NAME')[['QTY.']].sum().sort_values('QTY.',
                                                                ascending=False).head(1).reset_index()
        #top_product = final_df['PRODUCT NAME'].values[0]
        return final_df['PRODUCT NAME'].values[0]

#Get Top Male SIZE for That Top Product
def get_top_size(value, item_type):
    if value == 'ALL':
        top_male_product = df[(df['item_type']==item_type)]
        final_df = top_male_product.groupby('SIZE')[['QTY.']].sum().sort_values('QTY.',
                                                                ascending=False).head(1).reset_index()
        return final_df['SIZE']
    else:
        top_male_product = df[(df['item_type']==item_type) & (df['year']==value)]
        final_df = top_male_product.groupby('SIZE')[['QTY.']].sum().sort_values('QTY.',
                                                                ascending=False).head(1).reset_index()
        return final_df['SIZE']

#Get Top Male QTY. for That Top Product
def get_top_qty(value, item_type):
    if value == 'ALL':
        top_male_product = df[(df['item_type']==item_type)]
        final_df = top_male_product.groupby('PRODUCT NAME')[['QTY.']].sum().sort_values('QTY.',
                                                                ascending=False).head(1).reset_index()
        return final_df['QTY.']
    else:
        top_male_product = df[(df['item_type']==item_type) & (df['year']==value)]
        final_df = top_male_product.groupby('PRODUCT NAME')[['QTY.']].sum().sort_values('QTY.',
                                                                ascending=False).head(1).reset_index()
        return final_df['QTY.']

#Get Top BRAND
def get_top_brand(value, item_type):
    top_product = get_top_product(value, item_type)
    if value == 'ALL':
        top_male_product = df.loc[(df['item_type']==item_type) & (df['PRODUCT NAME']==top_product)]
        final_df = top_male_product.groupby('BRAND')[['QTY.']].sum().sort_values('QTY.',
                                                                ascending=False).head(1).reset_index()
        return final_df['BRAND']
    else:
        top_male_product = df.loc[(df['item_type']==item_type) & (df['year']==value) & (df['PRODUCT NAME']==top_product)]
        final_df = top_male_product.groupby('BRAND')[['QTY.']].sum().sort_values('QTY.',
                                                                ascending=False).head(1).reset_index()
        return final_df['BRAND']

#Graph for Male Items on Male Index paddingLeft
def get_all_items_with_qty(value, item_type):
    if value == 'ALL':
        top_male_product = df[(df['item_type']==item_type)]
        final_df = top_male_product.groupby(['PRODUCT NAME'])[['QTY.']].sum().sort_values('QTY.',
                                                                ascending=False).head(20).reset_index()
        return final_df
    else:
        top_male_product = df[(df['item_type']==item_type) & (df['year']==value)]
        final_df = top_male_product.groupby(['PRODUCT NAME'])[['QTY.']].sum().sort_values('QTY.',
                                                                ascending=False).head(20).reset_index()
        return final_df


def get_filter_df_on_item_type(item):
    filter_df = df.groupby(['year','month','item_type','PRODUCT NAME',
                            pd.Grouper(freq="M")])[['SALE AMT.','QTY.']].sum().reset_index()
    filter_df = filter_df.loc[(filter_df['item_type']==item)]
    filter_df = filter_df.groupby(['year','month','PRODUCT NAME'])[['SALE AMT.','QTY.']].sum().reset_index()
    return filter_df

def df_timeframe(value, item_type):
    filter_df = df.sort_values(by='DATE', ascending=True) \
            .last(value+'M')
    filter_df = filter_df.loc[filter_df['item_type']==item_type]
    filter_df = filter_df.groupby(['PRODUCT NAME'])[['SALE AMT.','QTY.']].sum().sort_values(by='QTY.',
                                                    ascending=False).reset_index()
    filter_df['SALE AMT.'] = round(filter_df['SALE AMT.'])

    return filter_df

def brand_timeframe(value, item_type):
    filter_df = df.sort_values(by='DATE', ascending=True) \
            .last(value+'M')
    filter_df = filter_df.loc[filter_df['item_type']==item_type]
    filter_df = filter_df.groupby(['BRAND'])[['SALE AMT.','QTY.']].sum().sort_values(by='QTY.',
                                                    ascending=False).reset_index().head(10)
    filter_df['SALE AMT.'] = round(filter_df['SALE AMT.'])

    return filter_df

def brand_wise_df(value, item_name, item_type):
    filter_df = df.sort_values(by='DATE', ascending=True) \
            .last(value+'M')
    filter_df = filter_df.loc[(filter_df['PRODUCT NAME']==item_name) & (filter_df['item_type']==item_type)]
    filter_df = filter_df.groupby(['BRAND'])[['SALE AMT.','QTY.']].sum().sort_values(by='QTY.',
                                                    ascending=False).reset_index()
    filter_df['SALE AMT.'] = round(filter_df['SALE AMT.'])

    return filter_df


def get_all_items_dropdown(item_type):
    return [{'label':i,'value':i} for i in df[df['item_type']==item_type]['PRODUCT NAME'].unique()]

def sizewise_items_list(timeframe_val,value,item_type):
    filter_df = df.sort_values(by='DATE', ascending=True) \
            .last(timeframe_val+'M')
    temp = filter_df[(filter_df['PRODUCT NAME']==value) & (filter_df['item_type']==item_type)][['SIZE','QTY.','SALE AMT.']].sort_values(
                                by='QTY.', ascending=False)
    final_df = temp.groupby('SIZE')[['SIZE','QTY.','SALE AMT.']].sum().sort_values(
                                by='QTY.', ascending=False).reset_index().head(10)
    final_df['SALE AMT.'] = round(final_df['SALE AMT.'])
    return final_df

def rangewise_items_df(timeframe_val, value,item_type):
    filter_df = df.sort_values(by='DATE', ascending=True) \
            .last(timeframe_val+'M')
    temp = filter_df[(filter_df['PRODUCT NAME']==value) & (filter_df['item_type']==item_type)][['RATE','SIZE','QTY.','SALE AMT.']].sort_values(
                                by='RATE', ascending=False)
    final_df = temp.groupby('RATE')[['QTY.','SALE AMT.']].sum().sort_values(by='RATE', ascending=False).reset_index()
    return final_df

weightage_arr = []
def conditions_for_range(t_df, min, max):
    conditions = [
    (t_df['RATE'] >= max),
    (t_df['RATE'] >= min) & (t_df['RATE'] < max),
    (t_df['RATE'] < min)]
    choices = ['high ({}+)'.format(max), 'medium ({}-{})'.format(min,max), 'low (<{})'.format(min)]
    #df['weightage'] = np.select(conditions, choices)
    #print(len(np.select(conditions, choices)))
    return pd.Series(np.select(conditions, choices))

def get_weightage_column(timeframe_val, value, item_type):

    if item_type == 'male':
        final_df = rangewise_items_df(timeframe_val,value,item_type)
        if value == 'M.BOXER':
            final_df['weightage'] = conditions_for_range(final_df,300, 500)
        elif value == 'M.BRIEF':
            final_df['weightage'] = conditions_for_range(final_df,150, 300)
        elif value == 'M.CAPRI':
            final_df['weightage'] = conditions_for_range(final_df,500, 700)
        elif value == 'M.TRUNK':
            final_df['weightage'] = conditions_for_range(final_df,150, 300)
        elif value == 'M.TRACKPANT':
            final_df['weightage'] = conditions_for_range(final_df,600, 1000)
        elif value == 'M.BARMUDA':
            final_df['weightage'] = conditions_for_range(final_df,300, 340)
        elif value == 'M.SHORT':
            final_df['weightage'] = conditions_for_range(final_df,350, 500)
        elif value == 'M.TSHIRT':
            final_df['weightage'] = conditions_for_range(final_df,350, 530)
        elif value == 'M.VEST':
            final_df['weightage'] = conditions_for_range(final_df,120, 180)
        elif value == 'M.SPORT VEST':
            final_df['weightage'] = conditions_for_range(final_df,170, 300)
        elif value == 'M.NIGHTSUIT':
            final_df['weightage'] = conditions_for_range(final_df,600, 700)
        elif value == 'M.THERMAL':
            final_df['weightage'] = conditions_for_range(final_df,650, 700)
        return final_df
    elif item_type == 'female':
        final_df = rangewise_items_df(timeframe_val,value,item_type)
        if value == 'L.BRA':
            final_df['weightage'] = conditions_for_range(final_df,200, 400)
        elif value == 'L.BRIEF':
            final_df['weightage'] = conditions_for_range(final_df,200, 400)
        elif value == 'L.NIGHTY':
            final_df['weightage'] = conditions_for_range(final_df,600, 800)
        elif value == 'L.CAPRI':
            final_df['weightage'] = conditions_for_range(final_df,450, 650)
        elif value == 'L.NIGHTSUIT':
            final_df['weightage'] = conditions_for_range(final_df,700, 1000)
        elif value == 'L.TSHIRT':
            final_df['weightage'] = conditions_for_range(final_df,350, 530)
        elif value == 'L.TRACKPANT':
            final_df['weightage'] = conditions_for_range(final_df,650, 850)
        elif value == 'L.SLIP':
            final_df['weightage'] = conditions_for_range(final_df,150, 200)
        elif value == 'L.SHORT':
            final_df['weightage'] = conditions_for_range(final_df,200, 400)
        elif value == 'L.BODYSHAPER':
            final_df['weightage'] = conditions_for_range(final_df,500, 600)
        return final_df
    elif item_type == 'boy':
        final_df = rangewise_items_df(timeframe_val,value,item_type)
        if value == 'B.NIGHTSUIT':
            final_df['weightage'] = conditions_for_range(final_df,480, 600)
        elif value == 'B.BRIEF':
            final_df['weightage'] = conditions_for_range(final_df,150, 250)
        elif value == 'B.TRACK':
            final_df['weightage'] = conditions_for_range(final_df,400, 500)
        elif value == 'B.BOXER':
            final_df['weightage'] = conditions_for_range(final_df,120, 390)
        elif value == 'B.TRUNK':
            final_df['weightage'] = conditions_for_range(final_df,100, 400)
        elif value == 'B.TSHIRT':
            final_df['weightage'] = conditions_for_range(final_df,230, 250)
        elif value == 'B.VEST':
            final_df['weightage'] = conditions_for_range(final_df,60, 70)
        elif value == 'B.SHORT':
            final_df['weightage'] = conditions_for_range(final_df,370, 400)
        return final_df
    elif item_type == 'girl':
        final_df = rangewise_items_df(timeframe_val,value,item_type)
        if value == 'G.NIGHTSUIT':
            final_df['weightage'] = conditions_for_range(final_df,500, 700)
        elif value == 'G.BRIEF':
            print('No Item available')
            pass
            #final_df['weightage'] = conditions_for_range(final_df,200, 300)
        return final_df

def add_range_df(timeframe_val,value, item_type):

    final_df = get_weightage_column(timeframe_val,value, item_type)
    #final_df['range'] = range_arr
    grouped_df = final_df.groupby('weightage')[['QTY.','SALE AMT.']].sum().sort_values(by='QTY.'
                                                , ascending=False).reset_index()
    grouped_df['SALE AMT.'] = round(grouped_df['SALE AMT.'])
    return grouped_df

def get_weightage_top_list(timeframe_val,value, item_type, weightage_val):
    weightage_df = get_weightage_column(timeframe_val,value, item_type)
    final_df = weightage_df[(weightage_df['weightage']==weightage_val)].sort_values(by='QTY.', ascending=False).head(5)
    final_df['SALE AMT.'] = round(final_df['SALE AMT.'])
    return final_df

def items_qty(timeframe, item, item_type):
    if int(timeframe) == 7:
        filter_df = df.sort_values(by='DATE', ascending=True) \
                    .last(timeframe+'D')
    else:
        filter_df = df.sort_values(by='DATE', ascending=True) \
                    .last(timeframe+'M')

    filter_df = filter_df.loc[(filter_df['PRODUCT NAME']==item) & (filter_df['item_type']==item_type)]
    final_df = filter_df['QTY.'].sum()
    return final_df

def items_brand(timeframe, item, item_type):
    if int(timeframe) == 7:
        filter_df = df.sort_values(by='DATE', ascending=True) \
                    .last(timeframe+'D')
    else:
        filter_df = df.sort_values(by='DATE', ascending=True) \
                    .last(timeframe+'M')

    filter_df = filter_df.loc[(filter_df['PRODUCT NAME']==item) & (filter_df['item_type']==item_type)]
    final_df = filter_df.groupby(['BRAND'])[['QTY.']].sum().sort_values(by='QTY.',
                                                    ascending=False).head(1).reset_index()
    if (final_df['QTY.'] is 0) | (final_df.empty) :
        return '-'
    else:
        return final_df['BRAND']

def items_size(timeframe, item, item_type):
    if int(timeframe) == 7:
        filter_df = df.sort_values(by='DATE', ascending=True) \
                    .last(timeframe+'D')
    else:
        filter_df = df.sort_values(by='DATE', ascending=True) \
                    .last(timeframe+'M')

    filter_df = filter_df.loc[(filter_df['PRODUCT NAME']==item) & (filter_df['item_type']==item_type)]
    final_df = filter_df.groupby(['SIZE'])[['QTY.']].sum().sort_values(by='QTY.',
                                                    ascending=False).head(1).reset_index()
    if (final_df['QTY.'] is 0) | (final_df.empty) :
        return '-'
    else:
        return final_df['SIZE']

############# ALL MALE ITEMS PAGE ################

def get_all_items_by_timeframe(value, item_type):
        filter_df = df.sort_values(by='DATE', ascending=True) \
                .last(value+'M')
        filter_df = filter_df.loc[filter_df['item_type']==item_type]
        filter_df = filter_df.groupby(['month','day','PRODUCT NAME'])[['SALE AMT.','QTY.']].sum().sort_values(by='QTY.',
                                                        ascending=False).reset_index()
        filter_df['SALE AMT.'] = round(filter_df['SALE AMT.'])

        return filter_df
