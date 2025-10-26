from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models.connection import Connection
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
import os

def fix_engine_if_invalid_params(engine):
    invalid_param = '__extra__'
    query_items = engine.url.query.items()
    if invalid_param in [k for (k, v) in query_items]:
        from sqlalchemy.engine.url import URL
        from sqlalchemy.engine import create_engine
        import logging

        modified_query_items = {k: v for k, v in query_items if k != invalid_param}
        modified_url = URL.create(
            drivername=engine.url.drivername,
            username=engine.url.username,
            password=engine.url.password,
            host=engine.url.host,
            port=engine.url.port,
            database=engine.url.database,
            query=modified_query_items
        )
        logging.info(f'Note: {invalid_param} removed from {query_items} in engine url')
        engine = create_engine(modified_url)
    return engine

@dag(
  dag_id='load_taxi_zone_data_to_postgres',
  start_date=datetime(2025, 1, 1),
  schedule=None,
  catchup=False,
  tags=['etl', 'postgres']
)
def load_data_pipeline():
  @task
  def load_data_to_postgres():
    file_path = '/opt/airflow/data/processed/taxi_zone_lookup.csv'
    
    print(f'Reading data from: {file_path}')
    df = pd.read_csv(file_path)
    df.columns = [col.lower().replace(' ', '_') for col in df.columns]
    
    pg_hook = PostgresHook(postgres_conn_id='taxi_zone_db')
    # conn = pg_hook.get_connection(pg_hook.postgres_conn_id)
    # db_uri = pg_hook.get_uri().replace(f'{conn.conn_type}://', f'postgresql+psycopg2://')
    # engine = create_engine(db_uri)
    engine = fix_engine_if_invalid_params(pg_hook.get_sqlalchemy_engine())
    
    df.to_sql(
      name='taxi_zones',
      con=engine,
      if_exists='replace',
      index=False
    )
    
  load_data_to_postgres()
load_data_pipeline()