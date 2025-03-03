# Homework Answers for Module 4
Prep queries creating views of data conforming to the data we are using:
```sql
CREATE OR REPLACE VIEW `proj.dataset.green_tripdata_2019-2020`
OPTIONS (
    friendly_name="green-2019-2020",
    description="View of green trip data from only 2019 to 2020"
)
AS SELECT * FROM proj.dataset.green_tripdata WHERE filename LIKE '%2019%' OR filename LIKE '%2020%';

CREATE OR REPLACE VIEW `proj.dataset.yellow_tripdata_2019-2020`
OPTIONS (
    friendly_name="yellow-2019-2020",
    description="View of yellow trip data from only 2019 to 2020"
)
AS SELECT * FROM proj.dataset.yellow_tripdata WHERE filename LIKE '%2019%' OR filename LIKE '%2020%'
```

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
1. 
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
        ELSE 100 * ((quarterly_revenue - LAG(quarterly_revenue, 4) OVER (ORDER BY trunc_quarter))/ LAG(quarterly_revenue, 4) OVER (ORDER BY trunc_quarter)) 
    END AS yoy_q_rev_growth
FROM revs
ORDER BY 1, 2 ASC
```