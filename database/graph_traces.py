from database import db_utility
import plotly.graph_objs as go

# Male Traces

def timeframe_traces(value, item_type):
    final_df = db_utility.df_timeframe(value, item_type)
    traces = {}
    for product in final_df['PRODUCT NAME'].unique():
        traces['trace_' + product] = go.Bar(x=[str(product)],
                       y=final_df[final_df['PRODUCT NAME']==product]['QTY.'],
                       name=str(product))
    return list(traces.values())

def timeframe_brand_traces(value, item_type):
    final_df = db_utility.brand_timeframe(value, item_type)
    traces = {}
    for brand in final_df['BRAND'].unique():
        traces['trace_' + brand] = go.Bar(x=[str(brand)],
                       y=final_df[final_df['BRAND']==brand]['QTY.'],
                       name=str(brand))
    return list(traces.values())


def brandwise_items_traces(value, selected_item, item_type):
    temp_df = db_utility.brand_wise_df(value, selected_item, item_type)
    traces = {}
    for brand in temp_df['BRAND'].unique():
        traces['trace_' + brand] = go.Bar(x=[str(brand)],
                       y=temp_df[temp_df['BRAND']==brand]['QTY.'],
                       text=temp_df[temp_df['BRAND']==brand]['QTY.'],
                       texttemplate='%{text:.2s}',
                       textposition='outside',
                       name=str(brand))
    return list(traces.values())


def sizewise_items_traces(timeframe_val, value,item_type):
    final_df = db_utility.sizewise_items_list(timeframe_val, value,item_type)
    traces = {}
    for size in final_df['SIZE'].unique():
        traces['trace_'+size] = go.Bar(x=[str(size)],
                                       y = final_df[final_df['SIZE']==size]['QTY.'],
                                       name=str(size))
    return list(traces.values())

def rangewise_items_traces(timeframe_val,value,item_type):
    final_df = db_utility.add_range_df(timeframe_val,value,item_type)
    traces = {}
    for item in final_df['weightage'].unique():
        traces['trace_'+item] = go.Bar(x=[str(item)],
                                       y = final_df[final_df['weightage']==item]['QTY.'],
                                       name=str(item))
    return list(traces.values())

def timeframe_wise_item_traces(value, item_type):
    final_df = db_utility.get_all_items_with_qty(value,item_type)
    traces = {}
    for product in final_df['PRODUCT NAME'].unique():
        traces['trace_' + product] = go.Bar(x=[str(product)],
                       y=final_df[final_df['PRODUCT NAME']==product]['QTY.'],
                       name=str(product))
    return list(traces.values())

def timeframe_all_items_traces(value, item_type, timeframe):
    final_df = db_utility.get_all_items_by_timeframe(value, item_type)
    traces = {}
    for product in final_df['PRODUCT NAME'].unique():
        traces['trace_' + product] = go.Scatter(x=final_df[timeframe].unique(),
                       y=final_df[final_df['PRODUCT NAME']==product]['QTY.'],
                       mode='markers',
                       name=str(product),
                       opacity=0.6,
                       marker=dict(
                            size=20,
                      ))
    return list(traces.values())

def timeframe_all_item_bar_traces(value, item_type):
    final_df = db_utility.df_timeframe(value, item_type)
    traces = {}
    for product in final_df['PRODUCT NAME'].unique():
        traces['trace_'+product] = go.Bar(x=[str(product)],
                                       y = final_df[final_df['PRODUCT NAME']==product]['QTY.'],
                                       text=final_df[final_df['PRODUCT NAME']==product]['QTY.'],
                                       texttemplate='%{text:.2s}',
                                       textposition='outside',
                                       name=str(product)
                                       )
    return list(traces.values())
