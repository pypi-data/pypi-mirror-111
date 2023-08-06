import glob
import time
import schedule as _schedule
from typing import Dict, Optional, Callable, Any

'''
You've got the Urge to write some code.
So go ahead.
'''


class NoobError(Exception):
    '''Everybody Makes a Mistake'''

    pass


class TimeUnitError(NoobError):
    '''Typo Invalid and Empty'''

    pass


class DumbEmptyError(NoobError):
    pass


class CarelessFunctionError(NoobError):
    '''Ugh'''

    pass


class InvalidUrlError(NoobError):
    pass


class Action:

    # def __init__(self) -> None:
    #     self.on_success = None
    #     self.on_failed = None;

    on_success: Optional[Callable] = None
    on_failed: Optional[Callable] = None

    @staticmethod
    def convert_time(time: Dict[int, str]) -> int:
        if not time:
            raise DumbEmptyError(
                'Put time value and unit in pairs , or just use seconds'
            )

        val, unit = list(time.items())[0]

        if unit == 'seconds':
            return val
        elif unit == 'minutes':
            return round(val / 60)
        elif unit == 'hours':
            return round(val / 360)
        else:
            raise TimeUnitError(
                f'{unit} is not a valid unit, try to use "seconds minutes and hour..."'
            )

    @staticmethod
    def glob_file(pattern):
        pattern_list = glob.glob(pattern)
        return pattern_list

    @staticmethod
    def _callable_check(func: Callable):
        if not isinstance(func, Callable):
            raise CarelessFunctionError('Pass a function ,not call a function inside')

    def every(self, freq) -> None:
        # shoud be in convert_time ?
        if isinstance(freq, dict):
            freq = Action.convert_time(freq)

        _schedule.every(freq).seconds.do(self.once)

    def when(self, time: str):
        _schedule.every().day.at(time).do(self.once)

    def _now(self):
        raise NotImplementedError()

    def once(self, *args) -> Any:
        try:
            # if get result then pass to callback
            res = self._now()
            if self.on_success is not None:
                self.on_success(res)
            return res
        except Exception as e:
            if self.on_failed is not None:
                self.on_failed(e)

    def success(self, func: Callable):
        Action._callable_check(func)
        self.on_success = func
        return self

    def failed(self, func: Callable):
        Action._callable_check(func)
        self.on_failed = func
        return self


def start(interval: int = 0) -> None:

    while True:
        time.sleep(interval)
        _schedule.run_pending()
