import yaml
from sqlalchemy import create_engine

class DatabaseConnector:
    def read_db_creds(self):
        with open('db_creds.yaml','r') as f:
            self.creds = yaml.safe_load(f)
        return self.creds

    def init_db_engine(self):
        creds = self.read_db_creds()
        conn_string = (f"{creds['RDS_DBTYPE']}://{creds['RDS_USER']}:{creds['RDS_PASSWORD']}@{creds['RDS_HOST']}:{creds['RDS_PORT']/}/{creds['RDS_DATABASE']}"
        print(conn_string)
        print("Conencting to the ENGINE dude!")
        try:
            self.engine = create_engine(conn_string)
        except:
            print("Issue connecting to the database dudes.")
        else:
            print("Connected, no probs dudes.")
        return self.engine

db = DatabaseConnector()
engine = db.init_db_engine()
