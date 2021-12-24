import re
from jenkins.base import Path, Auth, JenkinsBase
from bigquery.regist_logs import Record, Register
import click

@click.command()
@click.option('--host')
@click.option('--job_path')
@click.option('--user')
@click.option('--pswd')
def command(host: str, job_path: str, user: str, pswd: str):
    def insert_jenkins_build_log(build_num):
        def jenkins_log_collect(host: str, job_path: str, user: str, pswd: str):
            """Get build log text & use them.
            """
            build_path = f'/{build_num}/consoleText'
            path = Path(host, job_path, build_path)
            key = Auth(user, pswd).key()
            jenkins = JenkinsBase(path, key)
            log = jenkins.get_log()
            lines = re.findall('VALUES\s\((.+)\)', log.text)

            def match_string(reg, line):
                match_object = re.search(reg, line)
                if bool(match_object):
                    return match_object.group().replace(',', '').replace('"', '').replace("'", "")
                else:
                    return 'None'

            records = []
            for line in lines:
                timestamp = match_string(r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}', line)
                mail_address = match_string(r'[a-zA-Z0-9_.+-]+@([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.)+[a-zA-Z]{2,}', line)
                user_id = match_string(r'"(.{32})"', line)
                product_type = match_string(r'"(.{4,6})"', line)
                phone_number = match_string(r'"(\d{11})"', line)
                record = Record(timestamp, mail_address, user_id, product_type, phone_number)
                records.append(record)
            print(f'Created records: {records}')
            return records

        def create_sql_rows(records):
            sql_rows = []
            for r in records:
                sql_row = (r.timestamp, r.mail_address, r.user_id, r.product_type, r.phone_number)
                sql_rows.append(sql_row)
            return sql_rows

        records = jenkins_log_collect(host, job_path, user, pswd)
        sql_rows = create_sql_rows(records)
        print(f'SQL rows: {sql_rows}')
        history_register = Register(project_name='remarketing-mail', dataset_name='demo', table_name='history_restore')
        history_register.insert(sql_rows)

    for i in range(2425, 2430):
        insert_jenkins_build_log(i)

if __name__ == '__main__':
    command()
