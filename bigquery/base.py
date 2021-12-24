from dataclasses import dataclass
from google.cloud import bigquery

class BigqueryBase:
    def custom_query(self, query):
        client = bigquery.Client()
        return client.query(query)

if __name__ == '__main__':
    bq = BigqueryBase()
    result = bq.custom_query('SELECT * FROM `remarketing-mail.demo.mail_history` LIMIT 1000')
    print(result)
