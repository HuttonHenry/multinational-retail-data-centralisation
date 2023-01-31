import pandas as pd
import yaml

def yaml_to_df(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return pd.DataFrame.from_dict(data)
    
myyaml = yaml_to_df("yaml_example.yaml")
print(myyaml)