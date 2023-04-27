from datetime import datetime


def current_time() -> str:
    return datetime.now().getMonth()+'/'+datetime.now().getDay()+'/'+datetime.now().getYear()
