import tabula 

class DataExtractor:
    def retrieve_pdf_data(self, PDFLink):
        dfs = tabula.read_pdf("https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf")
        return dfs


