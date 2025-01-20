import pandas as pd
from sqlalchemy import create_engine
engine = create_engine("postgresql://root:root@localhost:5432/taxis")
df_iter = pd.read_csv("./green.csv", iterator=True, chunksize=100000)
df = next(df_iter)
print(pd.io.sql.get_schema(df, con=engine, name="green_taxis"))
# check for the correct types 
# with this I see that the lpep_pickup_datetime and lpep_dropoff_datetime are TEXT when they need to be DATETIME
"""
CREATE TABLE green_taxis (
        "VendorID" BIGINT,
        lpep_pickup_datetime TEXT,
        lpep_dropoff_datetime TEXT,
        store_and_fwd_flag TEXT,
        "RatecodeID" BIGINT,
        "PULocationID" BIGINT,
        "DOLocationID" BIGINT,
        passenger_count BIGINT,
        trip_distance FLOAT(53),
        fare_amount FLOAT(53),
        extra FLOAT(53),
        mta_tax FLOAT(53),
        tip_amount FLOAT(53),
        tolls_amount FLOAT(53),
        ehail_fee FLOAT(53),
        improvement_surcharge FLOAT(53),
        total_amount FLOAT(53),
        payment_type BIGINT,
        trip_type FLOAT(53),
        congestion_surcharge FLOAT(53)
)
"""
# need to do the same for the other csv we will import:
zones = pd.read_csv("./zones.csv")
print(pd.io.sql.get_schema(zones, con=engine, name="zones"))
"""
CREATE TABLE zones (
        "LocationID" BIGINT,
        "Borough" TEXT,
        "Zone" TEXT,
        service_zone TEXT
)
"""
# noting this down so that I can join these on green_taxis.PULocationID = zones.LocationID and green_taxis.DOLocationID = zones.LocationID
