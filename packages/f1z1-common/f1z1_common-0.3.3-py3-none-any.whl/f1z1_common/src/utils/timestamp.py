# @Time     : 2021/6/3
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from enum import Enum
from functools import lru_cache
from typing import Union

from .enums import EnumUtil
from ..validator.is_validators import is_enum, is_number

TimestampTypes = Union[int, float]


class TimestampUnit(Enum):
    SECOND = 1
    MILLISECOND = 1000
    MICROSECOND = 1000000


class TimestampUtil(object):

    @classmethod
    def to_timestamp(cls, timestamp: TimestampTypes, unit: TimestampUnit = TimestampUnit.MILLISECOND) -> float:
        f = {
            TimestampUnit.SECOND: cls._to_second,
            TimestampUnit.MILLISECOND: cls._to_millisecond,
            TimestampUnit.MICROSECOND: cls._to_microsecond
        }.get(unit, cls._to_millisecond)
        return f(timestamp)

    @classmethod
    def _to_second(cls, timestamp: TimestampTypes) -> float:
        return cls._to_float(timestamp, TimestampUnit.SECOND)

    @classmethod
    def _to_millisecond(cls, timestamp: TimestampTypes) -> float:
        return cls._to_float(timestamp, TimestampUnit.MILLISECOND)

    @classmethod
    def _to_microsecond(cls, timestamp: TimestampTypes) -> float:
        return cls._to_float(timestamp, TimestampUnit.MICROSECOND)

    @classmethod
    @lru_cache()
    def _to_float(cls, number: TimestampTypes, unit: TimestampUnit) -> float:
        cls.check_timestamp(number)
        cls.check_timestamp_unit(unit)
        convert: int = EnumUtil.unenum(unit, "value")
        return float(number * convert)

    @staticmethod
    def check_timestamp(value: TimestampTypes):
        if not is_number(value):
            raise ValueError(
                f"timestamp need int or float, but got {type(value).__name__}"
            )

    @staticmethod
    def check_timestamp_unit(unit: TimestampUnit):
        if not is_enum(unit):
            raise ValueError(
                f"timestamp unit need Enum instance, but got {type(unit).__name__}"
            )
