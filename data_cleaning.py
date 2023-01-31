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