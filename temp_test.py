import pandas as pd

df_names = pd.read_csv('stocks_names.txt', sep = '#',  names = ['shortcut', 'name'], skipinitialspace=True)
df_names.set_index('shortcut', inplace=True)
df_names = df_names.to_dict()['name']


for company in df_names:
    print(company + '->' + df_names[company])
