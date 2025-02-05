## Homework for Wk 2
### Assignment
- See `flow.yml` for Kestra flow, I executed a backfill over 01 Jan 2021 - 06 July 2021 for both green and yellow in order to bring in the data for 2021 (which extends into July 2021)

### Question 1
As the flow purges the current execution files after moving the data over into GCS and processing the data in BigQuery, the data for the size of the file was not available in the Kestra logs. However, inside the Google Cloud Storage bucket the uncompressed size is available for the `yellow_tripdata_2020-12.csv` file:
- **128.3MB**

### Question 2
* `file: "{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv"`
* ergo: 
    - `"{{render(vars.file)}}" = "green_tripdata_2020-04.csv"`

### Question 3
Query run in BigQuery:
```sql
SELECT COUNT(*) FROM \`projectid.datasetname.yellow_tripdata\` WHERE filename LIKE "%2020%";
```

Results:
| Row | f0_ |
| - | - |
| 1 | 24648499 |

### Question 4
Query run in BigQuery:
```sql
SELECT COUNT(*) FROM \`projectid.datasetname.green_tripdata\` WHERE filename LIKE "%2020%";
```

Results:
| Row | f0_ |
| - | - |
| 1 | 1734051 |

### Question 5
Query run in BigQuery:
```sql
SELECT COUNT(*) FROM `projectid.datasetname.yellow_tripdata` WHERE filename LIKE "%2021-03%";
```
Results:
| Row | f0_ |
| - | - |
| 1 | 1925152 |

### Question 6
Inside of the "`triggers:`" section of the Kestra flow:
```yaml
triggers:
    - id: scheduled_trigger
      type: io.kestra.plugin.core.trigger.Schedule
      cron: "0 9 1 * *" # or whatever the crontab expression is for your desired scheduling
      timezone: America/New_York
```

Therefore: 
- Add a `timezone` property set to `America/New_York` in the Schedule trigger configuration