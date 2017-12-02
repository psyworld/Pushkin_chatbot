import datetime

def get_range(callback_data):
    date_ts = int(callback_data["date_ts"]) # timestamp Дня, на который нужны события
    offset = int(callback_data["offset"])
    category = callback_data["category"]
    start_ts = date_ts # начало дня
    end_tes = date_ts + 24*60*60  # конец дня
    return start_ts, end_tes
