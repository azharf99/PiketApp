from datetime import datetime
from django.core.exceptions import BadRequest
from utils.constants import WEEKDAYS, SCHEDULE_TIME_DICT

def get_day(date: str) -> str | bool:
    try:
        data = WEEKDAYS.get(datetime.strptime(str(date), "%Y-%m-%d").weekday(), False)
        return data
    except Exception as e:
        print(f"Data tidak valid! Error:{e}")
        return False
        
def parse_to_date(date: str):
    try:
        data = datetime.strptime(str(date), "%Y-%m-%d").date()
        return data
    except Exception as e:
        print(f"Data tidak valid! Error:{e}")
        return BadRequest("Data tidak Valid!")

def validate_date(value: str | None):
    if value is not None:
        result = get_day(value)
        return True if result else False
    return False

def validate_time(value: str) -> bool:
    return True if SCHEDULE_TIME_DICT.get(value) else False