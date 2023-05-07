import time
from typing import Callable
import requests


def request_with_retry(condition: Callable[[requests.Response], bool], wait_for_minutes: int,
                       call: Callable[[], type(requests)]):
    answer = call()

    while condition(answer) is True:
        time.sleep(wait_for_minutes)
        answer = call()

    return answer
