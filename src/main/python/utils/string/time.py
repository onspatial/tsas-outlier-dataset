
from datetime import datetime, timedelta

def get_next_date(input_date='get_new_date07-29T00:00:00', days=2, format_string='%Y-%m-%dT%H:%M:%S'):
    output_time = datetime.strptime(input_date, format_string) + timedelta(days=days)
    return output_time.strftime(format_string)

def get_current_date(format_string='%Y-%m-%dT%H:%M:%S'):
    return datetime.now().strftime(format_string)