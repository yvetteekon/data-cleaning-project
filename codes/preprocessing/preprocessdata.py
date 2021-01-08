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


def preprocess_customer_data(outfile_path):
    #load data
    df = pd.read_csv(filepaths.raw_customers_data, sep=';')
    df_names_and_gender = pd.read_excel(filepaths.external_names_and_gender_data, sheet_name='Sheet1')
    
    #clean data
    df = pd.merge(df, df_names_and_gender[['Name', 'Gender']], left_on='FirstName', right_on='Name', how='left')
    df = df.drop_duplicates(subset=['CustomerID'])
    feature_list = ['Gender']
    nan_replacements = 'F'
    df = pp.impute_nan(df, feature_list, nan_replacements=nan_replacements)
    df.drop(['Name'], axis=1, inplace=True)
    
    #export data
    df.to_csv(outfile_path, index=False)
    
    return df

def preprocess_employee_data(outfile_path):
    #load data
    df = pd.read_csv(filepaths.raw_employees_data, sep=';')
    
    #clean data
    date_list = ['HireDate','BirthDate']
    df = pp.clean_date_format(df, date_list)
    df = pp.derive_datetime(df, date_list)
    
    #export data
    df.to_csv(outfile_path, index=False)
    
    return df

def preprocess_country_data(outfile_path):
    #load data
    df = pd.read_csv(filepaths.raw_countries_data, sep=';')
    
    #clean data
    feature_list = ['CountryCode']
    nan_replacements = 'AV'
    df = pp.impute_nan(df, feature_list, nan_replacements=nan_replacements)
    
    #export data
    df.to_csv(outfile_path, index=False)
    
    return df
  
def preprocess_city_data(outfile_path):
    #load data
    df = pd.read_csv(filepaths.raw_cities_data, sep=';')
    df_us_regions = pd.read_csv(filepaths.external_us_regions_data, sep=',')
    
    #clean data
    city_list = df['CityName'].to_list()
    col_name = 'State'
    feature_list = ['State']
    nan_replacements = '0'

    df = pp.generate_state_given_city(df, city_list, col_name)
    df = pp.impute_nan(df, feature_list, nan_replacements=nan_replacements)
    df[col_name] = np.where(((df['CityName'] == 'New York') & (df[col_name] == '0')), 'NY',
                              np.where(((df['CityName'] == 'Kansas') & (df[col_name] == '0')), 'MO',
                                       np.where(((df['CityName'] == 'Oklahoma') & (df[col_name] == '0')), 'OK',
                                                np.where(((df['CityName'] == 'St. Paul') & (df[col_name] == '0')), 'MN',
                                                         np.where(((df['CityName'] == 'Jersey') & (df[col_name] == '0')), 'NJ',
                                                                  df[col_name])))))
    
    df[col_name+'.clean'] = np.where(((df['CityName'] == 'Toledo') & (df[col_name] == '18')) , 'OH',
                             np.where(((df['CityName'] == 'Colorado') & (df[col_name] == '18')), 'TX',
                                   np.where(((df['CityName'] == 'Lincoln') & (df[col_name] == '01')), 'NE',
                                       np.where(((df['CityName'] == 'Boston') & (df[col_name] == 'ENG')), 'MA',
                                            np.where(((df['CityName'] == 'Washington') & (df[col_name] == 'ENG')), 'UT',
                                               np.where(((df['CityName'] == 'Fresno') & (df[col_name] == '28')), 'CA',
                                                  np.where(((df['CityName'] == 'Richmond') & (df[col_name] == '07')), 'VA',
                                                   np.where(((df['CityName'] == 'San Francisco') & (df[col_name] == '05')), 'CA',
                                                      np.where(((df['CityName'] == 'Rochester') & (df[col_name] == 'ENG')), 'NY',
                                                         np.where(((df['CityName'] == 'Santa Ana') & (df[col_name] == '08')), 'CA',
                                                            np.where(((df['CityName'] == 'San Antonio') & (df[col_name] == '01')), 'TX',
                                                               np.where(((df['CityName'] == 'Birmingham') & (df[col_name] == 'ENG')), 'AL',
                                                                 np.where(((df['CityName'] == 'San Diego') & (df[col_name] == '02')), 'CA',
                                                               np.where(((df['CityName'] == 'Sacramento') & (df[col_name] == '15')), 'CA',
                                                                 np.where(((df['CityName'] == 'Aurora') & (df[col_name] == '08')), 'CO',
                                                                  np.where(((df['CityName'] == 'San Jose') & (df[col_name] == '05')), 'CA',
                                                                           df[col_name]))))))))))))))))
    df.drop([col_name], axis=1, inplace=True)
    df = pd.merge(df, df_us_regions, left_on=[col_name+'.clean'], right_on=['State Code'], how='left' )
    
    #export data
    df.to_csv(outfile_path, index=False)
    
    return df

def preprocess_product_data(outfile_path):
    #load data
    df = pd.read_csv(filepaths.interim_products_data_v1, sep=';')
    
    #clean data
    date_list = ['ModifyDate']
    feature_list = ['Resistant', 'IsAllergic']
    nan_replacements = '_blank'
    df.rename(columns={'VitalityDays,':'VitalityDays'},inplace=True)
    df.replace({'Dc Hikiage Hira Huba':'Bread'}, inplace=True)
    
    category0='Unknown'
    category1='Meat & Sausages'
    category2='Fish & Seafood'
    category3='Baking'
    category4='Produce'
    category5='Poultry'
    category6='Beans, Pasta, Rice & Assorted Grains'
    category7='Beverages'
    category8='Beer, Wine & Spirits'
    category9='Disposable/ Paper Products'
    category10='Condiment, Sauces & Spices'
    category11='Breakfast & Cereal'
    category12='Frozen'
    category13='Oils'
    category14='Bakery'
    category15='Dairy'
    category16='Snacks'
    category17='Canned Foods/ Preserves'
    category18='Cleaning Products'
    category19='Pharmacy'
    category20='Equipment'
    category = ' '

    items0 = []
    items1 = ['Beef', 'Lamb', 'Steak', 'Ribs', 'Pork', 'Veal', 'Sausage', 'Rabbit']
    items2 = ['Fish', 'Crab', 'Squid', 'Scallops', 'Scampi', 'Fillet', 'Sea Bass', 'Sardines', 'Shrimp', 'Salmon', 'Scallop',
         'Grouper', 'Sole - Dover Whole Fresh', 'Barramundi', 'Halibut - Fletches', 'Mussels - Cultivated']
    items3 = ['Flavouring', 'Extract', 'Cookie Dough', 'Cookie - Dough', 'Truffle Cups - Brown', 'Flour', 'Sugar', 'Black Currants',                      'Icing', 'Fond - Neutral', 'Phyllo Dough', 'Puree - Passion Fruit', 'Isomalt', 'Chocolate - Compound Coating',
         'Chocolate', 'Tofu - Firm', 'Baking Powder', 'Coconut - Shredded Sweet', 'Liners - Banana Paper']
    items4 = ['Onions', 'Artichoke', 'Grapes', 'Papayas', 'Eggplant', 'Blackberries', 'Kiwi', 'Blueberries', 'Turnip', 'Mangoes',
         'Oranges - Navel', 'Loquat', 'Durian', 'Lettuce', 'Spinach', 'Pomello', 'Fuji Apples', 'Banana', 'Pears',  
              'Salsify Organic', 'Langers - Ruby Red Grapfruit', 'Sprouts - Alfalfa', 'Raspberries - Fresh', 'Beets - Candy Cane Organic',
         'Sprouts - Baby Pea Tendrils', 'Tomato', 'Potatoes', 'Apricot', 'Beets - Mini Golden', 'Zucchini - Yellow']
    items5 = ['Chicken', 'Turkey', 'Guinea Fowl', 'Duck']
    items6 = ['Rice', 'Beans', 'Pasta', 'Corn Meal', 'Broom - Corn', 'Pasta - Cheese / Spinach Bauletti']
    items7 = ['Tea', 'Coffee', 'Soda', 'Juice', 'Water', 'Carbonated', 'Pepsi', 'Lemonade', 'Hot Chocolate', 
         'Island Oasis - Mango Daiquiri', 'Grenadine', 'Jolt Cola - Electric Blue', 'Puree - Mocha', 'Sobe - Tropical Energy',
         'antucket - Pomegranate Pear', 'Gatorade - Xfactor Berry', 'V8 - Berry Blend', 'Ocean Spray', 'Nantuket Peach Orange']
    items8 = ['Wine', 'Beer', 'Brandy', 'Rum', 'Smirnoff', 'Cognac', 'Campari', 'Remy Red', 'Cassis', 'Pernod', 'Pina Colada',
         'Creme De Banane - Marie', 'Tia Maria', 'Lime Cordial', 'Jagermeister', 'Bacardi Breezer - Tropical']
    items9 = ['Spoon', 'Towel', 'Table Cloth', 'Napkin', 'Plastic', 'Foam', 'Cup', 'Doilies - 5 Paper', 'Chef Hat 20Cm',
         'Steam Pan - Half Size Deep', 'Skirt', 'Sword Pick Asst', 'Tray - 16In Rnd Blk']
    items10 = ['Sauce', 'Primerba', 'Pepper', 'Ketchup', 'Mayonnaise', 'Smoked Paprika', 'Bay Leaf', 'Garlic',
         'Cumin', 'Sage', 'Wasabi', 'Thyme', 'Frenngreek', 'Onion Powder', 'Dry', 'Dried', 'Seed', 'Vinegar',
         'Wiberg Super Cure', 'Tahini Paste', 'Hickory Smoke Liquid', 'Otomegusa Dashi Konbu', 'Anchovy Paste', 
          'Browning Caramel Glace', 'Mustard Prepared', 'Rambutan', 'Olive - Spread Tapenade', 'Curry Paste - Madras']
    items11 = ['Cereal', 'Cornflakes']
    items12 = ['Egg Roll', 'Wrap', 'Ice Cream', 'Frozen']
    items13 = ['Oil']
    items14 = ['Bread', 'Pastry', 'Tart', 'Cake', 'Bagel', 'Muffin', 'Quiche', 'Brulee', 'Cinnamon Buns Sticky', 
          'Vol Au Vents', 'Assorted Desserts']
    items15 = ['Milk', 'Cheese', 'Eggs', 'Yoghurt', 'Yogurt', 'Butter', 'Hersey Shakes']
    items16 = ['Crackers', 'Chips', 'Nut', 'Cookie Chocolate', 'Cookies', 'Macaroons - Two Bite Choc', 'Kellogs All Bran Bars']
    items17 = ['Soup', 'Canned', 'Tuna - Salad Premix', 'Olives - Stuffed', 'Clam Nectar', 'Sauerkraut', 'Pie Filling', 
         'Cattail Hearts', 'Olives - Kalamata']
    items18 = ['Ecolab', 'Garbage Bags - Clear', 'Garbag Bags', 'Vaccum Bag', 'Gloves']
    items19 = ['Thermometer Digital', 'Bandage']
    items20 = ['Ice - Clear 300 Lb For Carving', 'Pail With Metal Handle 16L White', 'Pail For Lid', 'Whmis - Spray Bottle Trigger',
          'General Purpose Trigger', 'Hinge W Undercut', 'Ezy Change Mophandle']

    products_dict = {category0:items0, category1:items1, category2:items2, category3:items3, category4:items4, category5:items5, 
                 category6:items6, category7:items7, category8:items8, category9:items9, category10:items10, category11:items11,
                 category12:items12, category13:items13, category14:items14, category15:items15,category16:items16, 
                 category17:items17, category18:items18, category19:items19, category20:items20}
    
    df = pp.categorize_items(df, 'ProductName', 'CategoryName.clean', products_dict)
    
    df['ProductName'] = df['ProductName'].replace('\s+', ' ', regex=True) #replace one or more whitespace with an single space
    
    df['VitalityDays.clean'] = df['VitalityDays'].fillna(0).astype('int64')
    
    df = pp.clean_date_format(df, date_list)
    df = pp.impute_nan(df, feature_list, nan_replacements=nan_replacements)
    
    grouped_products = []
    unique_categories = list(df['CategoryName.clean'].unique())
    for category in unique_categories:
        products = list(df.loc[df['CategoryName.clean'] == category, 'ProductName'])
        grouped_products.append(products)

    category_products_dict = dict(zip(unique_categories, grouped_products))
    price_dict = {}
    random.seed(10)
    for category in category_products_dict:
        if category == 'Oils':
            products = category_products_dict[category]
            for item in products:            
                price = random.choice(np.arange(8.99, 16.00)) 
                price_dict[item] = price
        if category == 'Condiment, Sauces & Spices' or category == 'Canned Foods/ Preserves':
            products = category_products_dict[category]
            for item in products:            
                price = random.choice(np.arange(10.99, 20.00)) 
                price_dict[item] = price
        if category == 'Fish & Seafood' or category == 'Meat & Sausages' or category == 'Poultry':
            products = category_products_dict[category]
            for item in products:            
                price = random.choice(np.arange(30.99, 60.00)) 
                price_dict[item] = price
        if category == 'Cleaning Products':
            products = category_products_dict[category]
            for item in products:            
                price = random.choice(np.arange(50.99, 70.00)) 
                price_dict[item] = price
        if category == 'Disposable/ Paper Products':
            products = category_products_dict[category]
            for item in products:            
                price = random.choice(np.arange(8.99, 15.00)) 
                price_dict[item] = price
        if category == 'Breakfast & Cereal' or category == 'Dairy':
            products = category_products_dict[category]
            for item in products:            
                price = random.choice(np.arange(10.99, 30.00)) 
                price_dict[item] = price
        if category == 'Beverages':
            products = category_products_dict[category]
            for item in products:            
                price = random.choice(np.arange(9.99, 30.00)) 
                price_dict[item] = price
        if category == 'Snacks':
            products = category_products_dict[category]
            for item in products:            
                price = random.choice(np.arange(9.99, 20.00)) 
                price_dict[item] = price
        if category == 'Produce':
            products = category_products_dict[category]
            for item in products:            
                price = random.choice(np.arange(5.99, 30.00)) 
                price_dict[item] = price
        if category == 'Beans, Pasta, Rice & Assorted Grains' :
            products = category_products_dict[category]
            for item in products:            
                price = random.choice(np.arange(10.99, 20.00, 2)) 
                price_dict[item] = price
        if category == 'Baking':
            products = category_products_dict[category]
            for item in products:            
                price = random.choice(np.arange(10.99, 20.00)) 
                price_dict[item] = price
        if category ==  'Frozen':
            products = category_products_dict[category]
            for item in products:            
                price = random.choice(np.arange(7.99, 40.00, 2)) 
                price_dict[item] = price
        if category == 'Equipment':
            products = category_products_dict[category]
            for item in products:            
                price = random.choice(np.arange(20.99, 50.00)) 
                price_dict[item] = price
        if category == 'Beer, Wine & Spirits':
            products = category_products_dict[category]
            for item in products:            
                price = random.choice(np.arange(30.99, 60.00)) 
                price_dict[item] = price
        if category == 'Bakery':
            products = category_products_dict[category]
            for item in products:            
                price = random.choice(np.arange(15.99, 30.00)) 
                price_dict[item] = price
        if category == 'Pharmacy':
            products = category_products_dict[category]
            for item in products:            
                price = random.choice(np.arange(10.99, 30.00, 2)) 
                price_dict[item] = price
    
    df['Price.clean'] = df['ProductName'].copy()
    df['Price.clean'] = df['Price.clean'].replace(price_dict)

    df = df.drop(['Price', 'CategoryID', 'VitalityDays'], axis=1)
    
    #export data
    df.to_csv(outfile_path, index=False)
    
    return df

def preprocess_sales_data(outfile_path):
    #load data
    df = pd.read_csv(filepaths.raw_sales_data, sep=';')

    #clean data
    date_list = ['SalesDate']
    df = pp.clean_date_format(df, date_list)
    df['SalesDate'] = pd.to_datetime(df['SalesDate'], format='%Y-%m-%d %H:%M:%S')
    df['Discount.clean'] = df['Discount'].replace(np.nan, 0.00)
    df['TotalPrice.clean'] = df['TotalPrice'].replace('0,00', np.nan)
    df = df.sort_values(['CustomerID', 'SalesDate'], ascending=True).reset_index(drop=True)
    df = df.dropna(axis=0, subset=['SalesDate']).reset_index(drop=True)
    df['SalesDate.clean'] = df['SalesDate'].dt.date
    df['SalesDate.clean'] = pd.to_datetime(df['SalesDate.clean'])
    
    df = pp.create_invoice_no(df, 'SalesDate.clean', 'CustomerID')
    
    df = pp.create_sequential_identifier(df, 'SalesID.clean')
    
    df = df.drop(['Discount', 'TotalPrice', 'SalesDate', 'SalesID'], axis=1)
    
    #export data
    df.to_csv(outfile_path, index=False)
    
    return df

