
# Set paths
import os
import random

# Data manipulation
import pandas as pd
import numpy as np

# Date manipulation
import datetime as dt
import calendar
calendar.setfirstweekday(calendar.SUNDAY) 

# Geolocation
import geonamescache


def clean_date_format(df, date_list):
    for date in date_list:
        df[date] = df[date].str.split('.', n=1, expand=True)[0]
    return df

def impute_nan(df, features, nan_replacements=' '):
    for feature in features:
        df[feature] = df[feature].replace(to_replace=np.nan, value=nan_replacements)
    return df

def impute_missing_dates(df, identifier, dates, fillna_method='bfill'):
    for date in dates:
        df       = df.sort_values([identifier, date], ascending=True).reset_index(drop=True)
        df[date] = df[date].fillna(method=fillna_method)
        df       = df.sort_values([date], ascending=True).reset_index(drop=True)
    return df

def derive_datetime(df, date_list):
    for date in date_list:
        df[date]                   = pd.to_datetime(df[date])
        df[date+'.date']           = df[date].dt.date
        df[date+'.year']           = df[date].dt.year
        #df[date+'.month']          = df[date].dt.month.apply(lambda x: calendar.month_abbr[x])
        df[date+'.month_num']      = df[date].dt.month
        #df[date+'.year_month']     = df[date+'.year'].map(str) + " " + df[date+'.month'].map(str) 
        #df[date+'.year_month_num'] = df[date+'.year'].map(str) + " " + df[date+'.month_num']
        df[date+'.hour']           = df[date].dt.hour
        df[date+'.day']            =df[date].dt.day
        #df[date+'.weekday']        = df[date].dt.weekday_name
    return df

def drop_selected_columns(df, features):
    df = df.drop(features, axis=1)
    return df

def create_invoice_no(df, date, identifier):
    df['InvoiceNo'] = df.groupby([date, identifier]).ngroup()+1
    return df

def create_sequential_identifier(df, identifier):
    df[identifier+'.clean'] = np.nan
    df[identifier+'.clean'] = df.index + 1
    df.reset_index(drop=True, inplace=True)
    return df

def generate_state_given_city(df, city_list, col_name):
#     import geonamescache
    gc = geonamescache.GeonamesCache()
    state_list = []  
    
    for city in city_list:
        info = gc.get_cities_by_name(city)
        if info == []:
            state_list.append(np.nan)
        else:
            for dictionary in list(info[0].values()):
                state = list(dictionary.values())
                state_list.append(state[7])
    df[col_name] = state_list
    return df

def categorize_items(df, item_feature, new_category_feature, items_dict): 
    category = ' '
    df[new_category_feature] = category

    for k, v in items_dict.items():
        pat = '|'.join(v)
        df[item_feature] = df[item_feature].str.strip()
        df[item_feature] = df[item_feature].str.title()
        mask = df[item_feature].str.contains(pat, case=True)

        df.loc[mask, new_category_feature] = k
    return df

   
        


