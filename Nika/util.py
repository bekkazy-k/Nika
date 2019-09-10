from datetime import datetime
import json


def get_datetime_str_from_timestamp(timestamp):
    dt_object = datetime.fromtimestamp(timestamp)
    return dt_object.strftime("%Y-%m-%dT%H:%M:%S")


def get_datetime_str_from_now():
    now = datetime.now()
    return now.strftime("%Y-%m-%dT%H:%M:%S")


def get_datetime_str_from_str(str_val):
    return datetime.strptime(str_val, '%Y-%m-%d %H:%M:%S').strftime("%Y-%m-%dT%H:%M:%S")


def get_date_from_str(str_val):
    return datetime.strptime(str_val, '%Y-%m-%d %H:%M:%S')


def get_timestamp_from_date(date_val):
    return datetime.timestamp(date_val)


def nvl(val, rpl=""):
    if val:
        return val
    else:
        return rpl


def escape(str_val):
    return str_val.replace("\'", "").replace("\"", "")


def marshall(message):
    message = json.loads(message)
    return message


def unmarshall(message):
    msg = json.dumps(message)
    return msg



