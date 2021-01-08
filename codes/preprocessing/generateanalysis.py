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

# Custom package for data preprocessing
import preprocessing as pp

# Data paths
import filepaths

def rfm_analysis(outfile_path):
    EXTRACTION_DATE = dt.datetime(2018,5,10)
    
    df_produce = pd.read_csv(filepaths.processed_produce_data)
    df_customer = pd.read_csv(filepaths.interim_customers_data)
    
    df_produce['SalesDate'] = pd.to_datetime(df_produce['SalesDate'])
    
    rfm= df_produce.groupby('CustomerID', as_index=False).agg({'SalesDate': lambda date: (EXTRACTION_DATE - date.max()).days,
                                        'InvoiceNo': lambda num: len(num),
                                        'TotalPrice': lambda price: price.sum()})
    
    rfm.rename(columns={'SalesDate':'recency', 'InvoiceNo':'frequency', 'TotalPrice':'monetary'}, inplace=True)
    
    rfm['r_quartile'] = pd.qcut(rfm['recency'], 4, ['1','2','3','4'])
    rfm['f_quartile'] = pd.qcut(rfm['frequency'], 4, ['4','3','2','1'])
    rfm['m_quartile'] = pd.qcut(rfm['monetary'], 4, ['4','3','2','1'])
    
    rfm['RFM_Score'] = rfm.r_quartile.astype(str)+ rfm.f_quartile.astype(str) + rfm.m_quartile.astype(str)
    
    df_customer_produce = df_produce[['CustomerID', 'CustomerCityName', 'CustomerState', 
                                      'CustomerRegion', 'CustomerDivision']].drop_duplicates(subset=['CustomerID']).reset_index(drop=True)
    
    df_customer = pd.merge(df_customer_produce, df_customer, on='CustomerID', how='left')
    
    df_customer_rfm = pd.merge(rfm, df_customer, on='CustomerID', how='left')
    
    df_customer_rfm['customer_segment'] = df_customer_rfm['RFM_Score'].apply(pp.categorize_customers)    
    
    df_customer_rfm['customer_segment'] = np.where(((df_customer_rfm['customer_segment'] == 'other') & 
                                                    (df_customer_rfm['m_quartile'] == '1')), 'big spender',
                                               np.where(((df_customer_rfm['customer_segment'] == 'other') & 
                                                         (df_customer_rfm['f_quartile'] == '1')), 'loyal customers',
                                                       df_customer_rfm['customer_segment']))
    
    df_customer_rfm[['CustomerID', 'customer_segment']].to_csv(outfile_path)
    
    return df_customer_rfm