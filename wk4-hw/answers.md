# Homework Answers for Module 4

### Question 1
```sql
select *
from {{ source('raw_nyc_tripdata', 'ext_green_taxi' )}}
```
resolves to
```sql
select *
from myproject.my_nyc_tripdata.ext_green_taxi
```

### Question 2
In order to allow for overriding the default production time length of 30 days by command line arguments in 1st priority and environment variables in 2nd priority, you would add in a variable and replace the '30' in the SQL query with `{{ var("days_back", env_var("DAYS_BACK", "30"))}}` since the second argument of `var` provides a default value in the case of a null variable, and for the default value we want it to defer to the environment variables using `env_var`, which also has an optional second argument providing a default in case of null (and our ultimate default of 30 is encapsulated in quotes since the Jinja is only replacing a string and doesn't care about type). 

Therefore, the answer is "Update the `WHERE` clause to `pickup_datetime >= CURRENT_DATE - INTERVAL '{{ var("days_back", env_var("DAYS_BACK", "30"))}}' DAY`

### Question 3
* `dbt run --select models/staging/+

### Question 4
True statements:
* Setting a value for `DBT_BIGQUERY_TARGET_DATASET` is mandatory, otherwise it will fail to compile.
* X
* When using `core`, it materializes in the dataset defined in `DBT_BIGQUERY_TARGET_DATASET`.
* When using `stg`, it materializes in the dataset defined in `DBT_BIGQUERY_STAGING_DATASET`, or defaults to `DBT_BIGQUERY_TARGET_DATASET`.
* When using `staging`, it materializes in the dataset defined in `DBT_BIGQUERY_STAGING_DATASET`, or defaults to `DBT_BIGQUERY_TARGET_DATASET`.

### Question 5
```sql
-- fct_taxi_trips_quarterly_revenue.sql
WITH quarterly AS
(
    SELECT 
        service_type,
        pickup_datetime,
        DATE_TRUNC(pickup_datetime, QUARTER) AS trunc_quarter,
        -- EXTRACT(YEAR FROM pickup_datetime) || '-Q' || EXTRACT(QUARTER FROM pickup_datetime) AS year_quarter,
        total_amount
    FROM {{ ref('fact_trips') }}
    WHERE EXTRACT(YEAR FROM pickup_datetime) BETWEEN 2019 AND 2020
), 
revs AS
(
    SELECT
        service_type,
        trunc_quarter,
        SUM(total_amount) AS quarterly_revenue
    FROM quarterly
    GROUP BY 1, 2
)

SELECT
    service_type,
    trunc_quarter,
    quarterly_revenue,
    CASE WHEN 
        EXTRACT(YEAR FROM trunc_quarter) <> 2020 THEN NULL 
        ELSE 100 * ((quarterly_revenue - LAG(quarterly_revenue, 4) OVER (PARTITION BY service_type ORDER BY trunc_quarter)) / LAG(quarterly_revenue, 4) OVER (PARTITION BY service_type ORDER BY trunc_quarter)) 
    END AS yoy_q_rev_growth
FROM revs
ORDER BY 1, 2 ASC
```

**Results**:
- Green: {best: 2020/Q1, worst: 2020/Q2}
- Yellow: {best: 2020/Q1, worst: 2020/Q2}

### Question 6
```sql
-- fct_taxi_trips_monthly_fare_p95.sql
WITH valid AS 
(
    SELECT 
        service_type,
        pickup_datetime,
        fare_amount,
        EXTRACT(YEAR FROM pickup_datetime) || '-' || EXTRACT(MONTH FROM pickup_datetime) AS pickup_month
    FROM {{ ref('fact_trips') }}
    WHERE 
        fare_amount > 0 AND
        trip_distance > 0 AND
        payment_type_description in ('Cash', 'Credit card') AND
        EXTRACT(YEAR FROM pickup_datetime) BETWEEN 2019 AND 2020
)

SELECT
    DISTINCT pickup_month,
    service_type,
    PERCENTILE_CONT(fare_amount, .97) OVER (PARTITION BY service_type, pickup_month) AS p97,
    PERCENTILE_CONT(fare_amount, .95) OVER (PARTITION BY service_type, pickup_month) AS p95,
    PERCENTILE_CONT(fare_amount, .9) OVER (PARTITION BY service_type, pickup_month) AS p90
FROM valid
ORDER BY 1, 2
```
- Green: {p97: 55.023, p95: 45.5, p90: 27.0}
- Yellow: {p97: 32.5, p95: 26.0, p90: 19.0}

These numbers are very slightly off from the choices given, and I tried a couple other ways and got the same result, so I don't see where my error would be, and will choose the closest result. 
### Question 7
```sql
-- models/staging/stg_fhv_tripdata.sql
{{
    config(
        materialized='table'
    )
}}

with 
source as (

    select * from {{ source('staging', 'fhv_tripdata') }}

),

renamed as (

    select
        {{ dbt_utils.generate_surrogate_key(["dispatching_base_num", "dropoff_datetime", "pickup_datetime"])}} as tripid,
        {{ dbt.safe_cast("dispatching_base_num", api.Column.translate_type("string")) }} as dispatching_base_num,
        cast(pickup_datetime as timestamp) as pickup_time,
        cast(dropoff_datetime as timestamp) as dropoff_time,
        {{ dbt.safe_cast("pulocationid", api.Column.translate_type("integer")) }} as pickup_locationid,
        {{ dbt.safe_cast("dolocationid", api.Column.translate_type("integer")) }} as dropoff_locationid,
        {{ dbt.safe_cast("sr_flag", api.Column.translate_type("integer")) }} as sr_flag,
        {{ dbt.safe_cast("affiliated_base_number", api.Column.translate_type("string")) }} as affiliated_base_number

    from source
    where dispatching_base_num is not null

)

select * from renamed

-- dim_fhv_trips.sql
with trips as (
    select * from {{ ref('stg_fhv_tripdata')}}
),
zones as (
    select * from {{ ref('dim_zones')}}
)

select 
    trips.tripid,
    trips.dispatching_base_num,
    trips.pickup_time,
    trips.dropoff_time,
    extract(year from trips.pickup_time) as pickup_year,
    extract(month from trips.pickup_time) as pickup_month,
    extract(quarter from trips.pickup_time) as pickup_quarter,
    trips.pickup_locationid,
    pickup_zone.borough as pickup_borough,
    pickup_zone.zone as pickup_zone,
    trips.dropoff_locationid,
    dropoff_zone.borough as dropoff_borough,
    dropoff_zone.zone as dropoff_zone,
    trips.sr_flag,
    trips.affiliated_base_number
from trips
inner join zones as pickup_zone on pickup_zone.locationid = trips.pickup_locationid
inner join zones as dropoff_zone on dropoff_zone.locationid = trips.dropoff_locationid

-- fct_fhv_monthly_zone_traveltime_p90.sql
with trips_duration as (
    select 
        *,
        case when pickup_month < 10 
            then pickup_year || '-0' || pickup_month
            else pickup_year || '-' || pickup_month
        end as year_month,
        timestamp_diff(dropoff_time, pickup_time, minute) as trip_duration, -- in minutes
    from {{ ref("dim_fhv_trips") }}
)

select 
    distinct year_month,
    pickup_zone,
    dropoff_zone,
    percentile_cont(trip_duration, 0.9) over (partition by pickup_year, pickup_month, pickup_locationid, dropoff_locationid) as p90
from trips_duration

-- query to find dropoff locations with the second longest p90 trip_duration with pickup location in ("Newark Airport", "SoHo", "Yorkville East") in Nov 2019 which 
with initialcte as 
(   
    select
        pickup_zone,
        dropoff_zone,
        p90,
        row_number() over (partition by pickup_zone order by p90 desc) as ranking
    from {{ ref("fct_fhv_monthly_zone_traveltime_p90") }}
    where 
        pickup_zone in ("Newark Airport", "SoHo", "Yorkville East") and 
        year_month = '2019-11'
)
select
    pickup_zone,
    dropoff_zone,
    p90
from initialcte
where ranking <= 2
```
| pickup_zone | dropoff_zone | p90 |
| - | - | - |
| SoHo | Chinatown | 324 |
| Yorkville East | Garment District | 230 |
| Newark Airport | Williamsburg (South Side) | 135.9 |

