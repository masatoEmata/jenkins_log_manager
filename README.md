# Use case
## Example of the situation assumed:  
The records that were supposed to be uploaded to the DB (BigQuery) actually failed to be uploaded, and the DB (BigQuery) did not detect any error.  
So, I want to retrieve the records from my Jenkins build log and re-upload them to BigQuery.

# Sample command
```
python command.py --jenkins_host xxx.xxx.xxx.xxx --jenkins_job_path /job/xxx/job/xxx --jenkins_user xxx --jenkins_pswd xxx --jenkins_buildnum_start xxxx --jenkins_buildnum_end xxxx --bigquery_project xxx --bigquery_dataset xxx --bigquery_table xxx
```
