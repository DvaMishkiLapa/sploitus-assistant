import shlex
from collections import ChainMap
from datetime import datetime
from json import dumps, loads
from os import getenv
from subprocess import CalledProcessError, check_output
from threading import Semaphore, Thread
from typing import Any, Dict, List

from pytz import timezone

headers = {
    # 'authority': 'sploitus.com',
    # 'accept': 'application/json',
    # 'accept-language': 'en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7',
    'content-type': 'application/json',
    # 'dnt': 1,
    # 'origin': 'https://sploitus.com',
    # 'referer': 'https://sploitus.com/?query=Moodle',
    # 'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    # 'sec-ch-ua-mobile': '?0',
    # 'sec-ch-ua-platform': '"Windows"',
    # 'sec-fetch-dest': 'empty',
    # 'sec-fetch-mode': 'cors',
    # 'sec-fetch-site': 'same-origin',
    # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
}


class SploitusAssistant:
    def __init__(
            self,
            targets: List[str],
            headers: Dict[str, Any],
            targets_type: str = 'exploits',
            sort: str = 'default',
            title: bool = False,
            offset: int = 0,
            sploitus_url: str = 'https://sploitus.com',
            semaphore: int = 4
    ) -> None:
        self.tz = timezone(getenv('TZ', 'UTC'))
        self.targets = targets
        self.headers_dict = headers
        self.type = targets_type
        self.sort = sort
        self.title = title
        self.offset = offset
        self.sploitus_url = sploitus_url
        self.semaphore = semaphore
        self.result = self.__scan()

    def __run_curl_sploitus(self, target: str, output: list) -> None:
        self.headers_dict.update({'referer': f'{self.sploitus_url}/?query={target}'})
        headers_for_curl = ' '.join([f"-H '{k}: {v}'" for k, v in self.headers_dict.items()])
        cmd = "curl -s '{search_url}/search' {headers} --data-raw '{data}' --compressed".format(
            search_url=self.sploitus_url,
            headers=headers_for_curl,
            data=dumps(
                {
                    'type': self.type,
                    'sort': self.sort,
                    'query': target,
                    'title': self.title,
                    'offset': self.offset
                }
            )
        )
        status = 'error'
        try:
            data = loads(check_output(shlex.split(cmd)).decode())
            status = 'done'
        except CalledProcessError as exc:
            data = exc.output
        except Exception as e:
            data = str(e)
        output.append(
            {
                target: {
                    'status': status,
                    'data': data
                }
            }
        )

    def __dispatch(self, sem, argv, **kw):
        with sem:
            self.__run_curl_sploitus(argv, **kw)

    def __scan(self) -> Dict[str, dict]:
        sem = Semaphore(self.semaphore)
        threads = []
        output = []
        now_datatime = datetime.now(self.tz)
        for t in self.targets:
            T = Thread(target=self.__dispatch, args=(sem, t), kwargs={'output': output})
            T.start()
            threads.append(T)
        for T in threads:
            T.join()
        finish_time = datetime.now(self.tz)
        return {
            'targets_info': dict(ChainMap(*output)),
            'time': {
                'start_dt': now_datatime,
                'finish_dt': finish_time,
            }
        }


if __name__ == "__main__":
    result_domain = SploitusAssistant(
        targets=[
            'Moodle',
            'Gitlab',
            'Minio',
            'Forefront',
            'Fortinet',
            'Mysql',
            'Mongo',
            'Chrome',
            'Android',
            'Fortios',
            'Nginx',
            'Apache'
        ],
        headers=headers,
        targets_type='exploits',
        sort='default',
        title=False,
        offset=0,
        semaphore=8
    )
    out = dumps(result_domain.result, indent=2, default=str)
    # print(out)
    with open("output.json", "w") as outfile:
        outfile.write(out)
