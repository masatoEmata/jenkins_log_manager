from .base import BigqueryBase
from dataclasses import dataclass


@dataclass
class Record:
    timestamp: str
    user_id: str
    product_type: str
    mail_address: str
    phone_number: str


@dataclass
class Register(BigqueryBase):
    project_name: str
    dataset_name: str
    table_name: str

    def insert(self, records):
        """Excute BigQuery insert API method
            Args:
                records: Sample... [('6413', '2021-12-30', ...), ('6413', '2021-12-30', ...)]
            """
        sql_values = str(records).replace('[', '').replace(']', '')  # '(...), (...), ...'
        query = f'INSERT INTO `{self.project_name}.{self.dataset_name}.{self.table_name}` VALUES {sql_values}'
        print(f'Excute insert query: {query}')
        return self.custom_query(query)


if __name__ == '__main__':
    bq = Register('remarketing-mail', 'demo', 'mail_history')
    result = bq.insert([('2021-12-24 09:58:23.688007 UTC', 'emata+2@espalhar.net', 'test_user_id_value', 'main')])
    print(result)
