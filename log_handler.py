import re
from base import Path, Auth, JenkinsBase
import click

from dataclasses import dataclass
@dataclass
class Record:
    datetime: str
    user_id: str
    product_type: str
    mail_address: str
    phone_number: str

@click.command()
@click.option('--host')
@click.option('--job_path')
@click.option('--user')
@click.option('--pswd')
def jenkins_log_collect(host: str, job_path: str, user: str, pswd: str):
    """Get build log text & use them.
    """
    build_path = '/2351/consoleText'
    path = Path(host, job_path, build_path)
    key = Auth(user, pswd).key()
    jenkins = JenkinsBase(path, key)
    log = jenkins.get_log()
    print(log.text)
    lines = re.findall('VALUES\s\((.+)\)', log.text)

    def match_string(reg, line):
        match_object = re.search(reg, line)
        if bool(match_object):
            return match_object.group().replace(',', '').replace('"', '').replace("'", "")
        else:
            return None

    for line in lines:
        datetime = match_string(r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}', line)
        mail_address = match_string(r'[a-zA-Z0-9_.+-]+@([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.)+[a-zA-Z]{2,}', line)
        user_id = match_string(r'"(.{32})"', line)
        product_type = match_string(r'"(.{4,6})"', line)
        phone_number = match_string(r'"(\d{11})"', line)
        record = Record(datetime, mail_address, user_id, product_type, phone_number)
        print(
            record.datetime,
            record.mail_address,
            record.user_id,
            record.phone_number,
            record.product_type
            )
if __name__ == '__main__':
    jenkins_log_collect()
