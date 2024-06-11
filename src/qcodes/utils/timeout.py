import time
from typing import Optional


class Timeout:
    """A simple class to use with methods or loops that can time out

    Args:
        timeout_s: The number of seconds to wait before timeout
        raise_timeout: Whether or not to raise TimeOutError when the time duration lapses
        timeout_err_msg: The message to send when raising the TimeOutError

    Call returns:
        bool: True if the timeout duration has elapsed, else False

    Raises:
        TimeOutError
    """

    def __init__(
        self,
        timeout_s: float,
        raise_timeout: bool = True,
        timeout_err_msg: Optional[str] = None,
    ):
        self._start_time: float = time.perf_counter()
        self._timeout_s = timeout_s
        self.timeout_err_msg = timeout_err_msg
        self.raise_timeout = raise_timeout

    def __call__(self) -> bool:
        if time.perf_counter() < self._start_time + self._timeout_s:
            return False
        if self.raise_timeout:
            raise TimeoutError(self.timeout_err_msg)
        return True

    def reset(self) -> None:
        self._start_time = time.perf_counter()
