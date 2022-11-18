# coding=utf-8
__author__ = 'neowong'

from datetime import datetime
import pytz
import time
import traceback

DEFAULT_FORMAT = "%Y-%m-%d %H:%M:%S"


def is_valid_date(time_str, format_str=DEFAULT_FORMAT):
    """
    判断是否是一个有效的日期字符串
    :param time_str:
    :param format_str
    :return:
    """
    try:
        time.strptime(time_str, format_str)
        return True
    except:
        return False


def datetime_to_string(dt, format_str=DEFAULT_FORMAT):
    """
    把datetime转成字符串
    :param dt:
    :param format_str:
    :return:
    """
    return dt.strftime(format_str)


def string_to_datetime(str_time, format_str=DEFAULT_FORMAT):
    """
    把字符串转成datetime
    :param str_time:
    :param format_str:
    :return:
    """
    return datetime.strptime(str_time, format_str)


def string_to_timestamp(str_time):
    """
    把字符串转成时间戳形式
    :param str_time:
    :return:
    """
    return time.mktime(string_to_datetime(str_time).timetuple())


def timestamp_to_string(stamp, formater=DEFAULT_FORMAT):
    """
    把时间戳转成字符串形式
    :param stamp:
    :return:
    """
    return time.strftime(formater, time.localtime(stamp))


def datetime_to_timestamp(dt):
    """
    把datetime类型转外时间戳形式
    :param dt:
    :return:
    """
    return time.mktime(dt.timetuple())


def get_cur_strtime():
    return datetime_to_string(datetime.now())


def get_max_time(str_time_list):
    ret = string_to_datetime(str_time_list[0])
    for t in str_time_list:
        temp = string_to_datetime(t)
        if temp > ret:
            ret = temp
    return ret


def format_utc_to_date(str_time):
    str_time = str_time[:str_time.find('.') + 4]
    u_format = "%Y-%m-%dT%H:%M:%S.%f"
    try:
        return datetime.strptime(str_time, u_format)
    except Exception:
        print(traceback.format_exc())
        print("format_utc_to_date:{0}".format(str_time))
        return


def utc_to_timestamp(utc_time_str, utc_format='%Y-%m-%dT%H:%M:%S.%f+08:00'):
    """
    # UTCS时间转换为时间戳
    :param utc_time_str:
    :param utc_format:
    :return: int, 时间戳
    """
    if isinstance(utc_time_str, int):
        return utc_time_str
    # 截取UTC时间的数字部分,精确到毫秒级
    n = utc_time_str.find('.') + 4
    for i in utc_time_str[utc_time_str.find('.') + 1:utc_time_str.find('.') + 4]:
        if not i.isdigit():
            n = utc_time_str.find(i)
            break
    utc_time_str = utc_time_str[:n] + "+08:00"
    local_tz = pytz.timezone('UTC')
    local_format = "%Y-%m-%d %H:%M:%S.%f"
    utc_dt = datetime.strptime(utc_time_str, utc_format)
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    time_str = local_dt.strftime(local_format)
    return int(time.mktime(time.strptime(time_str, local_format)))


def get_now_local_time() -> str:
    return datetime_to_string(datetime.now())


if __name__ == "__main__":
    cur_time = datetime.now()
    print(get_now_local_time())
    # print datetime_toTimestamp(cur_time)
    # print datetime_toString(cur_time)
