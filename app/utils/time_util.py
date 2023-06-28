import calendar
import time
from datetime import datetime


def timestamp_to_datetime(timestamp) -> datetime:
    """将时间戳转换为datetime对象"""
    return datetime.fromtimestamp(timestamp)


def datetime_to_timestamp(datetime) -> int:
    """将datetime对象转换为时间戳"""
    return datetime.timestamp()


def datetime_to_str(datetime, format="%Y-%m-%d %H:%M:%S") -> str:
    """将datetime对象转换为字符串"""
    return datetime.strftime(format)


def str_to_datetime(string, format="%Y-%m-%d %H:%M:%S") -> datetime:
    """将字符串转换为datetime对象"""
    return datetime.strptime(string, format)


def strutc_to_datetime(t: time.struct_time) -> datetime:
    """将时间元组转换为datetime对象"""
    return datetime.utcfromtimestamp(calendar.timegm(t))
