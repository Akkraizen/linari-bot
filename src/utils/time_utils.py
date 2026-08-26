import re
from datetime import timedelta

def parse_time_string(time_str: str) -> timedelta | None:
    if not isinstance(time_str, str):
        return None

    time_str = time_str.lower().replace(" ", "")
    if not time_str:
        return None

    pattern = r"(\d+)([дчмсdhms])"
    matches = re.findall(pattern, time_str)
    
    if not matches:
        return None

    remaining = re.sub(pattern, "", time_str)
    if remaining:
        return None

    total_delta = timedelta()
    for value, unit in matches:
        val = int(value)
        if unit in ('д', 'd'):
            total_delta += timedelta(days=val)
        elif unit in ('ч', 'h'):
            total_delta += timedelta(hours=val)
        elif unit in ('м', 'm'):
            total_delta += timedelta(minutes=val)
        elif unit in ('с', 's'):
            total_delta += timedelta(seconds=val)
    
    return total_delta
