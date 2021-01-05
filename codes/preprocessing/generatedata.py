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

def generate_produce_data(outfile_path):
    #load data
    df = pd.read_csv(filepaths.processed_merged_data)
    
    #subset data
    df = df.loc[df['ProductCategoryName'] == 'Produce']
    
    #clean data
    category0='Unknown'
    category1='Fruit'
    category2='Vegetable'


    category = ' '

    items0 = []
    items1 = ['Blueberries','Pears','Banana','Grapes','Apricots','Loquat','Mangoes','Kiwi','Blackberries','Apples','Raspberries',
                 'Grapfruit','Papayas','Fruit','Pomello','Oranges']
    items2 = ['Eggplant','Lettuce','Tomato','Potatoes','Turnip','Sprouts','Lettuce','Artichokes','Zucchini','Beets','Spinach',
                 'Onions','Salsify Organic']

    products_dict = {category0:items0, category1:items1, category2:items2}
    
    df = pp.categorize_items(df, 'ProductName', 'ProduceSubGroup', products_dict)       
        
    unique_produce_type = list(df['ProduceSubGroup'].unique())
    size_fruit = df.loc[df['ProduceSubGroup'] == 'Fruit'].shape[0]
    size_vegetable = df.loc[df['ProduceSubGroup'] == 'Vegetable'].shape[0]
    quantity_dict = {}
    random.seed(10)
    for produce_type in unique_produce_type: 
        if produce_type == 'Fruit':   
            quantity = np.random.choice(np.arange(start = 2, stop =7), size=size_fruit, replace=True, p=[0.02, 0.05, 0.33, 0.45, 0.15]) 
            quantity_dict[produce_type] = quantity
        if produce_type == 'Vegetable':   
            quantity = np.random.choice(np.arange(start = 10 , stop =18), size=size_vegetable, replace=True, 
                                        p=[0.09, 0.11, 0.15, 0.25, 0.35, 0.03, 0.005, 0.015]) 
            quantity_dict[produce_type] = quantity 
            
    df['Quantity.new'] = df['ProduceSubGroup'].copy()
    df['Quantity.new'] = df['Quantity.new'].replace(quantity_dict)
    
    df = df.drop(['Quantity'], axis=1)

    df = df.rename(columns={'Quantity.new':'Quantity'})

    df_sample1 = df[df['ProduceSubGroup'] == 'Fruit'].sample(200000)

    df_sample = df[~df.index.isin(df_sample1.index)]

    df_sample['ProduceSubGroup'].value_counts(dropna=False)

    df_sample.reset_index(drop=True, inplace=True)
    
    #export data
    df_sample.to_csv(outfile_path, index=False)
    
    return df_sample
    