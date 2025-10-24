import pandas as pd

df = pd.read_csv('data/raw/taxi+_zone_lookup.csv')

print(df.head(5))

print(df.info())

print(df.describe())