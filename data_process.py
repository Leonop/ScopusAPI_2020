import pandas as pd
import numpy as np

url = '/Users/leono1/OneDrive/Research_2019/Jared_Project/'
data = pd.read_csv(url+'outcome4.csv')

data_unique = data[['AuthorID', 'Last Name', 'First Name', 'Affiation', 'outcomeNum']]
print(data_unique)

data_unique = data_unique.drop_duplicates(keep='first')
print(data)
print(data_unique)

data_unique=data_unique.sort_values(by=['outcomeNum'])

data_unique.to_csv(url+'unique_list.csv')

