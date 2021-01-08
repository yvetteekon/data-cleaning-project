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

# Data paths
import filepaths

def merge_data(outfile_path, extraction_date=None):
    #set default extraction date
    if extraction_date == None:
        extraction_date = '2018-05-09'
    
    #load data
    df_customers = pd.read_csv(filepaths.interim_customers_data)
    df_employees = pd.read_csv(filepaths.interim_employees_data)
    df_countries = pd.read_csv(filepaths.interim_countries_data)
    df_cities = pd.read_csv(filepaths.interim_cities_data)
    df_products = pd.read_csv(filepaths.interim_products_data_v2)
    df_sales = pd.read_csv(filepaths.interim_sales_data)

    #city + customer data
    df_cities = df_cities[['CityID', 'CityName', 'State.clean', 'Region', 'Division']]
    df_customers = df_customers[['CustomerID', 'CityID', 'FirstName', 'MiddleInitial', 'LastName', 'Gender']]
    df_customers = pd.merge(df_customers, df_cities, on='CityID', how ='left')
    df_customers = df_customers.rename(columns={'CityName':'CityName.customer', 'State.clean':'State.customer',
                                               'FirstName':'FirstName.customer', 'LastName':'LastName.customer',
                                               'Gender':'Gender.customer'})

    #city + employee data
    df_employees['EmployeeAge'] = round((pd.to_datetime(extraction_date) - pd.to_datetime(df_employees['BirthDate']))/np.timedelta64(1,'Y'))
    df_employees['EmployeeLengthOfService'] = round((pd.to_datetime(extraction_date) - 
                                                     pd.to_datetime(df_employees['HireDate']))/np.timedelta64(1, 'Y'))
    df_employees = df_employees[['EmployeeID','EmployeeAge','Gender', 'CityID', 'EmployeeLengthOfService']]
    df_employees = pd.merge(df_employees, df_cities, on='CityID', how ='left')
    df_employees = df_employees.rename(columns={'CityName':'CityName.employee', 'EmployeeID':'SalesPersonID'})
    
    #sales + employee data
    df = pd.merge(df_sales, df_employees, on='SalesPersonID', how ='left')   
    
    #sales + employee + products data
    df = pd.merge(df, df_products, on='ProductID', how ='left')
    df['TotalPrice.clean'] = np.where((df['Discount.clean'] != 0.00), 
                                      ((df['Price.clean'] - (df['Price.clean'] * df['Discount.clean'])) * df['Quantity']),
                                      (df['Price.clean'] * df['Quantity']))
    
    #sales + employee + products + customer data
    df = pd.merge(df, df_customers, on='CustomerID', how ='left', suffixes=['.employee', '.customer'])
    
    #clean data
    df.drop(['CityID.customer', 'CityID.employee', 'Quantity'], axis=1, inplace=True)
    size = len(df)
    df['Quantity.clean'] = [x for x in random.choices(range(2, 55), k=size)]
    
    df = df.rename(columns={'Discount.clean':'Discount', 'TotalPrice.clean':'TotalPrice', 'SalesDatetime.clean':'SalesDatetime', 
                        'SalesDate.clean': 'SalesDate', 'SalesID.clean':'SalesID', 'Gender':'SalesPersonGender', 
                        'CityName.employee':'SalesPersonCityName', 'State.clean':'SalesPersonState', 
                        'Region.employee':'SalesPersonRegion', 'EmployeeAge':'SalesPersonAge',
                        'EmployeeLengthOfService':'SalesPersonServiceYears',
                        'Division.employee':'SalesPersonDivision', 'CategoryName.clean':'ProductCategoryName',
                        'VitalityDays.clean':'VitalityDays', 'Price.clean':'Price', 'CityName.customer':'CustomerCityName',
                        'State.customer':'CustomerState', 'Region.customer':'CustomerRegion', 'Division.customer':'CustomerDivision',
                        'Quantity.clean':'Quantity'})          
    
    #export merged data
    df.to_csv(outfile_path, index=False)
              
    return df