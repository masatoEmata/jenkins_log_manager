from google.cloud import bigquery

class BigqueryBase:
    def custom_query(self, query):
        client = bigquery.Client()
        return client.query(query)

if __name__ == '__main__':
    bq = BigqueryBase()
    result = bq.custom_query('SELECT * FROM `my-project-xxx.my_dataset_xxx.my_table` LIMIT 1000')
    print(result)
