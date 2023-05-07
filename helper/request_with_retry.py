import time
from typing import Callable, Optional
import requests


def request_with_retry(condition: Callable[[requests.Response], bool], wait_for_seconds: int,
                       call: Callable[[], type(requests)], retries: int):
    """
    :param condition: As long as return value is True, the loop will repeat
    :param wait_for_seconds: Amount of seconds passing between two calls.
    :param call: A lambda function containing the call itself.
    :param retries: Amount of possible Retries. Must be set since we dont want infinite loops
    :return: the answer object. It can still meet the condition since the tried calls can max out retries
    """

    answer = call()
    tried_calls = 0

    while condition(answer) is True and tried_calls < retries:
        print("Condition of retry met. (Call", str(tried_calls + 1), "of", str(retries) + ")")
        time.sleep(wait_for_seconds)
        answer = call()
        tried_calls += 1

    return answer
