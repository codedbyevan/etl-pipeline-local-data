import pandas as pd

df = pd.read_csv('data/raw/taxi+_zone_lookup.csv')

df = df.rename(columns={
  'LocationID': 'location_id',
  'Borough': 'borough',
  'Zone': 'zone',
  'service_zone': 'service_zone'
})

print('First 5 rows')
print(df.head(5))

print('Check for null value in each column')
print('Null value of service_zone' ,df['service_zone'].isnull().sum())
print('Null value of borough' ,df['borough'].isnull().sum())
print('Null value of zone' ,df['zone'].isnull().sum())

df['service_zone'] = df['service_zone'].fillna('Unknown')

print('Null value of service_zone' ,df['service_zone'].isnull().sum())

df.to_csv('data/processed/taxi_zone_lookup.csv', index=False)