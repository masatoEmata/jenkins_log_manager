from dataclasses import dataclass
from typing import Tuple
from requests import get

@dataclass
class Path:
    host: str
    job: str
    build: str


@dataclass
class Auth:
    user: str
    pswd: str

    def key(self):
        return (self.user, self.pswd)


@dataclass
class JenkinsBase:
    path: Path
    auth: Tuple[str]

    def _generate_uri(self):
        return f'http://{self.path.host}{self.path.job}{self.path.build}'

    def get_log(self):
        uri = self._generate_uri()
        print(f'Requested URL: {uri}')
        return get(uri, auth=self.auth)

    def parse_log(self):
        pass

    def use_log(self):
        pass
