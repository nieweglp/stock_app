import pandas as pd
import yaml

def read_yaml_file(file):
  with open('config.yaml') as file:
    yaml_content = yaml.load(file, Loader=yaml.FullLoader)
    return yaml_content

def read_stock_names_tickers(file):
  df_names = pd.read_csv('stocks_names.txt', sep = '#',  names = ['shortcut', 'name'])
  df_names.set_index('shortcut', inplace=True)
  return df_names