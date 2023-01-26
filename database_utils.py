import yaml
from sqlalchemy import create_engine
from sqlalchemy import inspect

class DatabaseConnector:
    def read_db_creds(self):
        with open('db_creds.yaml','r') as f:
            self.creds = yaml.safe_load(f)
        return self.creds

    def init_db_engine(self):
        creds = self.read_db_creds()
        conn_string = (f"{creds['RDS_DBTYPE']}://{creds['RDS_USER']}:{creds['RDS_PASSWORD']}@{creds['RDS_HOST']}:{creds['RDS_PORT']}/{creds['RDS_DATABASE']}")
        print(conn_string)
        print("Conencting to the ENGINE dude!")
        try:
            self.engine = create_engine(conn_string)
        except:
            print("Issue connecting to the database dudes.")
        else:
            print("Connected, no probs dudes.")
        return self.engine

    def list_db_tables(self,dbengine):
        inspector = inspect(dbengine)
        for table_name in inspector.get_table_names():
            print(table_name)
        
    def read_data_from_db(self, table_name):
        connection = self.engine.connect()
        query = f"SELECT * FROM {table_name}"
        result = connection.execute(query).fetchall()
        connection.close()
        return result


db = DatabaseConnector()
engine = db.init_db_engine()
tables = db.list_db_tables(engine)