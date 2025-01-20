## Homework for Wk 1
#### Question 1
Run docker with the `python:3.12.8` image in an interactive mode, use the entrypoint bash.

What's the version of `pip` in the image?

* `pip --version`
    - 24.3.1

#### Question 2
* `hostname`: `postgres`
* `port`: 5432

#### Question 3
1. 104802
- `SELECT COUNT(*) FROM green_taxis WHERE lpep_dropoff_datetime::DATE BETWEEN '2019-10-01' AND '2019-10-31' AND trip_distance <= 1;`
2. 198924
- `SELECT COUNT(*) FROM green_taxis WHERE lpep_dropoff_datetime::DATE BETWEEN '2019-10-01' AND '2019-10-31' AND trip_distance > 1 AND trip_distance <= 3;`
3. 109603
- `SELECT COUNT(*) FROM green_taxis WHERE lpep_dropoff_datetime::DATE BETWEEN '2019-10-01' AND '2019-10-31' AND trip_distance > 3 AND trip_distance <= 7;`
4. 27678
- `SELECT COUNT(*) FROM green_taxis WHERE lpep_dropoff_datetime::DATE BETWEEN '2019-10-01' AND '2019-10-31' AND trip_distance > 7 AND trip_distance <= 10;`
5. 35189
- `SELECT COUNT(*) FROM green_taxis WHERE lpep_dropoff_datetime::DATE BETWEEN '2019-10-01' AND '2019-10-31' AND trip_distance > 10;`

#### Question 4
- 2019-10-11: 95.78mi
- 2019-10-24: 90.75mi
- 2019-10-26: 91.56mi
- 2019-10-31: 515.89mi

Therefore, `2019-10-31` was the day with the longest max distance.
Query:
```
SELECT
	lpep_pickup_datetime::DATE AS pickup_date,
	MAX(trip_distance)
FROM green_taxis
WHERE 
	lpep_pickup_datetime::DATE IN ('2019-10-11', '2019-10-24', '2019-10-26', '2019-10-31')
GROUP BY 1;
```

#### Question 5
