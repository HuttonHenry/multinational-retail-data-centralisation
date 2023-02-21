import tabula 
import pandas as pd
import requests 
import boto3


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

    def retrieve_stores_data(number_stores,retrieve_store_endpoint, header):
        stores_data = []
        for i in range(number_stores):
            store_url = retrieve_store_endpoint+str(i)
            try:
                response = requests.get(store_url, headers=header)
            except:
                print("there was an error!")    
            stores_data.append(response.json())
            if i % 10 == 0:
                print(f"Collected record {i}")
            df = pd.DataFrame(stores_data)
        return df