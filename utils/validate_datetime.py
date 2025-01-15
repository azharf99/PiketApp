from datetime import date, datetime
from django.core.exceptions import BadRequest
from utils.constants import WEEKDAYS, SCHEDULE_TIME_DICT

def get_day(date_string: str | date) -> str | bool:
    data = ''
    if isinstance(date_string, date):
        data = WEEKDAYS.get(date_string.weekday())
        return data
    try:
        data = WEEKDAYS.get(datetime.strptime(str(date_string), "%Y-%m-%d").weekday(), False)
    except Exception as e:
        data = "Error"
    return data
        
def parse_to_date(date_string: str):
    if isinstance(date_string, date): return date_string
    data = ''
    try:
        data = datetime.strptime(date_string, '%Y-%m-%d').date() if date_string else datetime.now().date()
    except Exception as e:
        data = datetime.now().date()
    return data

def validate_date(value: str | None):
    if value is not None:
        result = get_day(value)
        return True if result else False
    return False

def validate_time(value: str) -> bool:
    return True if SCHEDULE_TIME_DICT.get(value) else False