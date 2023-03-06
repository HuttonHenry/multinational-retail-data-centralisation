# H1
Data Centralisation Project - Jan, 2023.


# multinational-retail-data-centralisation


Code created using Python 

Uses SQL Alchemy for SQL connectivity
https://docs.sqlalchemy.org/en/20/core/engines.html
pip install sqlalchemy


Postgres Connection
I needed to change the YAML file, as it used the same variable for both the postgres database type and databaase name, but the type had changed to 'postgresql'.  

I also had to install <conda install psycopg2>
https://anaconda.org/anaconda/psycopg2


PANDAS
Had to install <conda install pandas>

For this project:

(a) I messed up the database, wiping all records so had to use the code to recreate. 


The Product Dataframe was a problem, so had to use df.info() which provided the following information and


RangeIndex: 1853 entries, 0 to 1852
Data columns (total 10 columns):
 #   Column         Non-Null Count  Dtype 
---  ------         --------------  ----- 
 0   Unnamed: 0     1853 non-null   int64 
 1   product_name   1849 non-null   object
 2   product_price  1849 non-null   object
 3   weight         1849 non-null   object
 4   category       1849 non-null   object
 5   EAN            1849 non-null   object
 6   date_added     1849 non-null   object
 7   uuid           1849 non-null   object
 8   removed        1849 non-null   object
 9   product_code   1849 non-null   object


 df.describe()

 dtypes: int64(1), object(9)
memory usage: 144.9+ KB
None
        Unnamed: 0
count  1853.000000
mean    926.000000
std     535.059343
min       0.000000
25%     463.000000
50%     926.000000
75%    1389.000000
max    1852.000000

Finally after hours of toying with dirty data, got to the easy data change for Milestone 3.4"

(a) remove the £ symbol from the pricing

UPDATE dim_products
SET product_price = REPLACE(product_price, '£', '')

(b) add a new colum weight_class - Varchar(?)

ALTER TABLE dim_products
ADD weight_class VARCHAR(50)

(c) 
The team that handles the deliveries would like a new human-readable column added for the weight so they can quickly make decisions on delivery weights.

Add a new column weight_class which will contain human-readable values based on the weight range of the product.

--------------------------+-------------------+
| weight_class VARCHAR(?)  | weight range(kg)  |
+--------------------------+-------------------+
| Light                    | < 2               |
| Mid_Sized                | 3 - 40            |
| Heavy                    | 41 - 140          |
| Truck_Required           | > 141             |
+----------------------------+-----------------+

Which is this update query:

UPDATE dim_products
SET weight_class = 
  CASE
    WHEN weight < 2 THEN 'Light'
    WHEN weight >= 2 AND weight <= 40 THEN 'Mid_Sized'
    WHEN weight > 40 AND weight <= 141 THEN 'Heavy'
    WHEN weight > 141 THEN 'Truck_Required'
  END;

  
MS 3.6

Now update the date table with the correct types:

+-----------------+-------------------+--------------------+
| dim_date_times  | current data type | required data type |
+-----------------+-------------------+--------------------+
| month           | TEXT              | CHAR(?)            |
| year            | TEXT              | CHAR(?)            |
| day             | TEXT              | CHAR(?)            |
| time_period     | TEXT              | VARCHAR(?)         |
| date_uuid       | TEXT              | UUID               |
+-----------------+-------------------+--------------------+

Obviously the data is pretty dirty, with NULLS and non numerics.


