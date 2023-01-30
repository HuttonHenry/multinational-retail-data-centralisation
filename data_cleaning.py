class DataCleaning:
        
        def __init__(self):
            print("in datacleaner init")

        def clean_user_data(self,data):            
            # Check for NULL values and replace with appropriate values
            data.fillna(value='', inplace=True)
            # Check for errors in date values and correct them
            data['date_of_birth'] = data.

            data['date_of_birth'] = data.to_datetime(data['date_of_birth'], errors='coerce')
            # Check for incorrectly typed values and correct them
            data['column_name'] =data['column_name'].astype(str)
            # Check for rows filled with wrong information and drop them
            data = data[data['column_name'] != 'invalid_value']
            return data