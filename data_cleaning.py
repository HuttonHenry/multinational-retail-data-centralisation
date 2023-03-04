import pandas as pd
from datetime import datetime

class DataCleaning:
        
        def __init__(self):
            pass

        def clean_user_data(self,data):            
            # Check for NULL values and replace with appropriate values
            data.fillna(value='', inplace=True)
            #data['date_of_birth'] = data.to_datetime(data['date_of_birth'], errors='coerce')
            # Check for incorrectly typed values and correct them
            data['first_name'] =data['first_name'].astype(str)
            # Check for rows filled with wrong information and drop them
            data = data[data['first_name'] != 'invalid_value']
            return data
        
        def clean_card_data(self,df):
                # path to PDF file
                df.fillna(value='', inplace=True)
                df['card_number'] = df['card_number'].apply(DataCleaning.clean_credit_card_number)
                # return the DataFrame
                # here we return the dataframe and do not return any null fields
                return df.dropna(how='any')

        def clean_credit_card_number(number):
            # Remove all non-numeric characters from the number
            number = str(number)
            cleaned_number = ''.join(filter(str.isdigit, number))
            length = len(number)
            # If the length is less than 16, add zeros to the end
            if length < 16:
                cleaned_number = cleaned_number + "0" * (16 - length)
            # If the length is greater than 16, remove the last characters
            elif length > 16:
                cleaned_number = cleaned_number[:16]
            return cleaned_number
        
        def clean_store_data(self,df):
                # path to PDF file
                df.fillna(value='', inplace=True)
                # here we return the dataframe and do not return any null fields
                return df.dropna(how='any')
     
        def clean_orders_data(self, data):
            # Remove unnecessary columns
            data = data.drop(columns=["first_name", "last_name", "1"])
            
            # Rename columns to remove spaces and make them lowercase
            data = data.rename(columns=lambda x: x.strip().lower().replace(" ", "_"))
            for col in data.columns:
                print(col)
            
            return data
        
        def convert_product_weights(df):
            # create a dictionary to map units to kg
            unit_dict = {
                "g": 0.001,
                "kg": 1.0,
                "ml": 0.001,
                "l": 1.0
            }
            
            # clean up the weight column and remove excess characters
            #df["weight"] = df["weight"].str.replace(",", ".").str.extract('(\d+\.?\d*)')[0].astype(float)
            
            # replace units with kg equivalent
            df.dropna()
            df["unit"] = df["weight"].str.extract('([a-zA-Z]+)')[0].str.lower()
            df["weight"] = df["weight"].str.extract('(\d+)')
            df["weight"] = pd.to_numeric(df["weight"])
            df["weight"] = df["weight"] * df["unit"].map(unit_dict)
            df.drop("unit", axis=1, inplace=True)
            
            return df
        
        def clean_products_data(df):
            print(df.info()) 
            df = df.dropna() # Drop any rows with missing values
            df = df.drop_duplicates() # Drop any duplicate rows
            df = df[df['weight'] > 0] # Drop any rows with weight <= 0
            return df.reset_index(drop=True)