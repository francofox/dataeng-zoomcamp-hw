## Homework Answers - Module 3
### Setup
```sql
CREATE OR REPlACE EXTERNAL TABLE `de-course-448103.demo_dataset_de_course_448103.yellow_2024_parquet`
OPTIONS (
    format = 'PARQUET',
    uris = ['gs://demo-bucket-de-course-448103/yellow*.parquet']
);

CREATE OR REPLACE TABLE `de-course-448103.demo_dataset_de_course_448103.yellow_2024` AS
SELECT * FROM de-course-448103.demo_dataset_de_course_448103.yellow_2024_parquet;
```

### Question 1
This is visible at the bottom of the BigQuery "Preview" tab, but if I were to write a SQL query to find this, it would be:
```sql
SELECT COUNT(*) 
FROM de-course-448103.demo_dataset_de_course_448103.yellow_2024;
```

**answer: 20_332_093**

### Question 2
Query:
```sql
SELECT COUNT(DISTINCT PULocationID) FROM de-course-448103.demo_dataset_de_course_448103.yellow_2024;
-- The above will process 155.12MB when run; this is the materialized table
SELECT COUNT(DISTINCT PULocationID) FROM de-course-448103.demo_dataset_de_course_448103.yellow_2024_parquet;
-- The above will process 0B when run; this is the external table
```

**answer: 0B for the external table, 155.12MB for the materialized table**

### Question 3
Query:
```sql
SELECT PULocationID 
FROM de-course-448103.demo_dataset_de_course_448103.yellow_2024;
-- 155.12MB
SELECT PULocationID, DOLocationID 
FROM de-course-448103.demo_dataset_de_course_448103.yellow_2024;
-- 310.24MB, i.e. two times the column's size
```

The reason for this is that BigQuery is a columnar database and it only scans the specific columns requested in the query. Querying two columns requires reading more data than just one column. **Thus, #1 is the answer.**

### Question 4
Query:
```sql
SELECT COUNT(*) 
FROM de-course-448103.demo_dataset_de_course_448103.yellow_2024 
WHERE fare_amount = 0;
```
Result:

| Row | f0_ |
| - | - |
| 1 | 8333 |

### Question 5
**Answer: Partition by `tpep_dropoff_datetime` and cluster by `VendorID`**

Query:
```sql
CREATE OR REPLACE TABLE `de-course-448103.demo_dataset_de_course_448103.yellow_2024_part_tpepdr`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT * FROM de-course-448103.demo_dataset_de_course_448103.yellow_2024;
```

### Question 6
```sql
SELECT DISTINCT VendorID 
FROM de-course-448103.demo_dataset_de_course_448103.yellow_2024 
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15';
-- above is unpartitioned/unclustered table - 310.24MB to process
SELECT DISTINCT VendorID 
FROM de-course-448103.demo_dataset_de_course_448103.yellow_2024_part_tpepdr 
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15';
-- above is partitioned/clustered table - 26.84MB to process
```

**Answer: 310.24MB for non-partitioned table, 26.84MB for partitioned-and-clustered table.**

### Question 7
Question: Where is the data stored in the external table previously created?

**Answer: GCP Bucket**

### Question 8
It is best practice in BigQuery to always cluster your data:

**Answer: false - there is little to no effect to cluster tables <1GB in size**

### Question 9
```sql
SELECT COUNT(*) 
FROM de-course-448103.demo_dataset_de_course_448103.yellow_2024';
```
It estimates 0B to be read, which is because this information is stored in the metadata of the table in `INFORMATION_SCHEMA.TABLE_STORAGE`, so it costs nothing to access as there is no actual counting of rows. 