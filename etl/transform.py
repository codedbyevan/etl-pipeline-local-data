import pandas as pd

df = pd.read_csv('data/raw/taxi+_zone_lookup.csv')

df = df.rename(columns={
  'LocationID': 'location_id',
  'Borough': 'borough',
  'Zone': 'zone',
  'service_zone': 'service_zone'
})

print(df.head(5))

print(df['borough'].unique())

df = df.dropna(subset=['zone', 'service_zone'])

print(df.isnull().sum())

df.to_csv('data/processed/taxi_zone_lookup.csv', index=False)