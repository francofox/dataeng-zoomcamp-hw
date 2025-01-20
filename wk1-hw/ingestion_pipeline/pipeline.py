import pandas as pd
from sqlalchemy import create_engine
import argparse

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    dbname = params.dbname
    tblname = params.tblname
    csv = params.csv

    df_iter = pd.read_csv(csv, iterator=True, chunksize=100_000)
    df = next(df_iter)
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{dbname}")

    df.head(n=0).to_sql(name=tblname, con=engine, if_exists="replace")
    df.to_sql(name=tblname, con=engine, if_exists="append")

    while True:
        try:
            df = next(df_iter)
        except:
            break
        
        df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
        df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

        df.to_sql(name=tblname, con=engine, if_exists="append")
    print("Finished!")



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')
    # user, password, host, port, database name, table name, url of csv
    parser.add_argument('--user', help='Username for postgres')
    parser.add_argument('--password', help='Password for postgres')
    parser.add_argument('--host', help='Hostname for postgres')
    parser.add_argument('--port', help='Port for postgres')
    parser.add_argument('--dbname', help='DB name for postgres')
    parser.add_argument('--tblname', help='Table name for postgres')
    parser.add_argument('--csv', help='full path to CSV')

    args = parser.parse_args()

    main(args)