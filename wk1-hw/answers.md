## Homework for Wk 1
### Question 1
Run docker with the `python:3.12.8` image in an interactive mode, use the entrypoint bash.

What's the version of `pip` in the image?

* `pip --version`
    - 24.3.1

### Question 2
* `hostname`: `postgres`
* `port`: 5432

### Question 3
1. **104802**
```sql
SELECT COUNT(*) 
FROM green_taxis 
WHERE 
	lpep_dropoff_datetime::DATE BETWEEN '2019-10-01' AND '2019-10-31' 
	AND trip_distance <= 1;
```
2. **198924**
```sql
SELECT COUNT(*)
FROM green_taxis 
WHERE  
	lpep_dropoff_datetime::DATE BETWEEN '2019-10-01' AND '2019-10-31' 
	AND trip_distance > 1 
	AND trip_distance <= 3;
```
3. **109603**
```sql
SELECT COUNT(*) 
FROM green_taxis 
WHERE 
	lpep_dropoff_datetime::DATE BETWEEN '2019-10-01' AND '2019-10-31' 
	AND trip_distance > 3 
	AND trip_distance <= 7;
```
4. **27678**
```sql
SELECT COUNT(*) 
FROM green_taxis 
WHERE 
	lpep_dropoff_datetime::DATE BETWEEN '2019-10-01' AND '2019-10-31' 
	AND trip_distance > 7 
	AND trip_distance <= 10;
```
5. **35189**
```sql
SELECT COUNT(*) 
FROM green_taxis 
WHERE 
	lpep_dropoff_datetime::DATE BETWEEN '2019-10-01' AND '2019-10-31' 
	AND trip_distance > 10;
```

### Question 4
- 2019-10-11: 95.78mi
- 2019-10-24: 90.75mi
- 2019-10-26: 91.56mi
- 2019-10-31: 515.89mi

Therefore, `2019-10-31` was the day with the longest max distance.
Query:
```sql
SELECT
	lpep_pickup_datetime::DATE AS pickup_date,
	MAX(trip_distance)
FROM green_taxis
WHERE 
	lpep_pickup_datetime::DATE IN ('2019-10-11', '2019-10-24', '2019-10-26', '2019-10-31')
GROUP BY 1;
```

### Question 5
- East Harlem North, East Harlem South, Morningside Heights

Query:
```sql
SELECT
	pickup_zones."Zone",
	SUM(green_taxis."total_amount")
FROM green_taxis
LEFT JOIN zones pickup_zones ON pickup_zones."LocationID" = green_taxis."PULocationID"
WHERE green_taxis."lpep_pickup_datetime"::DATE = '2019-10-18'
GROUP BY 1
HAVING SUM(green_taxis."total_amount") > 13000;
```

### Question 6
- **JFK Airport**

Query:
```sql
SELECT
	dropoff_zones."Zone",
	MAX(green_taxis."tip_amount")
FROM green_taxis
LEFT JOIN zones pickup_zones ON pickup_zones."LocationID" = green_taxis."PULocationID"
LEFT JOIN zones dropoff_zones ON dropoff_zones."LocationID" = green_taxis."DOLocationID"
WHERE 
	green_taxis."lpep_pickup_datetime"::DATE BETWEEN '2019-10-01' AND '2019-10-31'
	AND pickup_zones."Zone" = 'East Harlem North'
GROUP BY 1
ORDER BY 2 DESC;
```

### Question 7
- `terraform init`, `terraform apply -auto-approve`, `terraform destroy`