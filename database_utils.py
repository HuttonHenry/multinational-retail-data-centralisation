import yaml
from sqlalchemy import create_engine
from sqlalchemy import inspect
import pandas
import data_cleaning as dc
import data_extraction as de


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class DatabaseConnector:

    def read_db_creds(self):
        with open('db_creds.yaml','r') as f:
            self.creds = yaml.safe_load(f)
        return self.creds

    def init_db_engine(self):
        creds = self.read_db_creds()
        conn_string = (f"{creds['RDS_DBTYPE']}://{creds['RDS_USER']}:{creds['RDS_PASSWORD']}@{creds['RDS_HOST']}:{creds['RDS_PORT']}/{creds['RDS_DATABASE']}")
        print(conn_string)
        print(f"{bcolors.OKBLUE}Conencting to the ENGINE dude!")
        try:
            self.engine = create_engine(conn_string)
        except:
            print(f"{bcolors.FAIL}Issue connecting to the database dudes.")
        else:
            print(f"{bcolors.OKGREEN}Connected, no probs dudes.")
        return self.engine

    def list_db_tables(self,dbengine):
        inspector = inspect(dbengine)
        tables = []
        for table_name in inspector.get_table_names():
            print(table_name)
            tables.append(table_name)
        return tables

        
    def read_data_from_db(self, table_name):
        connection = self.engine.connect()
        query = f"SELECT * FROM {table_name}"
        result = connection.execute(query).fetchall()
        print(f"{bcolors.OKCYAN}Adding table to pandas dataframe")
        try:
            mypanda = pandas.DataFrame(result)
        except:
            print(f"{bcolors.FAIL}Adding data to panda Dataframe failed.")
        connection.close()
        return mypanda

    def upload_to_db(self, dataframe, table_name):
        try:
            self.engine = create_engine("postgresql://postgres:Misty123@localhost:5432/Sales_Data")
            conn = self.engine.connect()
            dataframe.to_sql(table_name, conn, if_exists='replace')
            print("Data uploaded successfully to the table:", table_name)
        except Exception as e:
                print(f"{bcolors.FAIL}Error while uploading data to the database:", e)
        finally:
                conn.close()


#Connect to the Postgres database in AWS
db = DatabaseConnector()
engine = db.init_db_engine()
#List the tables
tables = db.list_db_tables(engine)
#Copy the data from the table into a Pandas DF
pandaDF = db.read_data_from_db("legacy_users")
for col in pandaDF.columns:
    print(col)
# Clean the data.
print(f"{bcolors.OKGREEN}Cleaning the data dude!")
dcc = dc.DataCleaning()
cleandata = dcc.clean_user_data(pandaDF)
print(f"{bcolors.OKGREEN}Uploading the data dude!")
success = db.upload_to_db(cleandata,"dim_users")

print(f"{bcolors.OKGREEN}Reading a PDF to Dataframe!")
PDFdf = de.DataExtractor().retrieve_pdf_data("https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf")

print(f"{bcolors.OKGREEN}Cleaning PDF dataframe.")
cleanCCdata = dc.DataCleaning().clean_card_data(PDFdf)
print(cleanCCdata)

print(f"{bcolors.OKGREEN}Uploading credit card data!")
success = db.upload_to_db(cleanCCdata,"dim_card_details")

numberstores = de.DataExtractor.list_number_of_stores()
number_of_stores = numberstores.get('number_stores')

headers = {
            "x-api-key": "yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX"
        }

#Get the data from the API
print(f"Collecting data from {number_of_stores} stores.")

#Extra data from the API
APIdf = de.DataExtractor.retrieve_stores_data(number_of_stores,"https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/",headers)
#Clean the dataframe
cleanAPIdata = dc.DataCleaning().clean_store_data(APIdf)
#Upload to the Postgres database.
success = db.upload_to_db(cleanAPIdata,"dim_store_details")

# List all tables in the database
tables = db.list_db_tables(engine)

# Find the table containing all information about the product orders
orders_table_name = None

for table in tables:
    if "orders" in table:
        orders_table_name = table
        break

if orders_table_name is None:
    raise Exception("Could not find the orders table in the database")
else:
    print(f"Orders table is called: {orders_table_name}")

# Extract the orders data from the database and store it in a DataFrame
engine = db.init_db_engine()
orders_data = db.read_data_from_db(orders_table_name)
print("cleaning orders data!")
print(type(orders_data))
cleaned_orders_data  = dc.DataCleaning().clean_orders_data(orders_data)
print("Uploading data to local SQL database")
# Upload the cleaned data to the database
cleaned_orders_data = cleaned_orders_data.reset_index(drop=True)
cleaned_orders_data = cleaned_orders_data.rename(columns={"level_0": "dude"})
success = db.upload_to_db(cleaned_orders_data, "orders_table")

#collect JSON data from S3
print(f"Now copying json data from S3 and copying to local database.")
json_data=de.DataExtractor().retreive_sales_date_times("data-handling-public","date_details.json")
success = db.upload_to_db(json_data, "dim_date_times")

#So I missed the entire milestone, 2.6 - collect CSV data, convert the weigths and clean the data before uploading to the database.

# First extract the data from S3
products_data = de.DataExtractor.extract_from_s3('s3://data-handling-public/products.csv')

# Then clean the data
cleaned_data = dc.DataCleaning.convert_product_weights(products_data)
cleaned_data = dc.DataCleaning.clean_products_data(cleaned_data)

# Finally upload the data to the database
success = db.upload_to_db(cleaned_data, "dim_products")