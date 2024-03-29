import os

project_parent_directory = '..'


RAW_DIR = os.path.join(project_parent_directory, 'data', 'raw')
EXTERNAL_DIR = os.path.join(project_parent_directory, 'data', 'external')
INTERIM_DIR  = os.path.join(project_parent_directory, 'data', 'interim')
PROCESSED_DIR = os.path.join(project_parent_directory, 'data', 'processed')
VIZ_DIR = os.path.join(project_parent_directory, 'visualizations')

#raw data directories
raw_customers_data = os.path.join(RAW_DIR, 'customers.csv')
raw_employees_data = os.path.join(RAW_DIR, 'employes.csv')
raw_countries_data = os.path.join(RAW_DIR, 'countries.csv')
raw_cities_data = os.path.join(RAW_DIR, 'cities.csv')
raw_categories_data = os.path.join(RAW_DIR, 'categories.csv')
raw_sales_data = os.path.join(RAW_DIR, 'sales.csv')
interim_products_data_v1 = os.path.join(INTERIM_DIR, 'products_cleaned_v1.csv')

#external data directories
external_us_regions_data = os.path.join(EXTERNAL_DIR, 'us census bureau regions and divisions.csv')
external_names_and_gender_data = os.path.join(EXTERNAL_DIR, 'SSA_Names_DB.xlsx')
external_us_state_lat_long_data = os.path.join(EXTERNAL_DIR, 'statelatlong.csv')

#interim data directories
interim_customers_data = os.path.join(INTERIM_DIR, 'customers_cleaned_v1.csv')
interim_employees_data = os.path.join(INTERIM_DIR, 'employees_cleaned_v1.csv')
interim_countries_data = os.path.join(INTERIM_DIR, 'countries_cleaned_v1.csv')
interim_cities_data = os.path.join(INTERIM_DIR, 'cities_cleaned_v1.csv')
interim_sales_data = os.path.join(INTERIM_DIR, 'sales_cleaned_v1.csv')
interim_products_data_v2 = os.path.join(INTERIM_DIR, 'products_cleaned_v2.csv')
interim_sales_db = os.path.join(INTERIM_DIR, 'salesdb.sqlite')

#processed data directories
processed_merged_data = os.path.join(PROCESSED_DIR, 'master_file.csv')
processed_produce_data = os.path.join(PROCESSED_DIR, 'produce_data.csv')
processed_produce_customer_segments = os.path.join(PROCESSED_DIR, 'produce_purchase_customer_segments.csv')

