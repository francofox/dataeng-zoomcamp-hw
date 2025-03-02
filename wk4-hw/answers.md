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
