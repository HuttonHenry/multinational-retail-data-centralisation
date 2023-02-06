import tabula 
import pandas as pd
import requests 

class DataExtractor:

    def __init__(self) -> None:
        pass

    def retrieve_pdf_data(self, PDFLink):
        dfs = pd.DataFrame(tabula.read_pdf(PDFLink, pages ='all')[0])
        print(type(dfs))
        return dfs

    def list_number_of_stores():
        headers = {
            "x-api-key": "yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX"
        }

        response = requests.get("https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores", headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return None
