import json

from cachetools import TTLCache

from entities.History_Search_Model import History_app, HistoryRecord
from services.Youtube_Analysis_Services import PysparkModule

desired_cache_size_bytes = 150 * 1024 * 1024  # 1 MB = 1024 * 1024 bytes

# The average size of each cached item is around 1 MB
average_item_size_bytes = 1 * 1024 * 1024

# Calculate the maxsize parameter
maxsize = desired_cache_size_bytes // average_item_size_bytes

cache = TTLCache(maxsize=maxsize, ttl=3600)

history_cache = TTLCache(maxsize=maxsize, ttl=300)


def generate_report_data(channel_name):
    pyspark_module = PysparkModule(channel_name)
    channel_id = pyspark_module.get_channel_id()
    if channel_id is not None:
        transformed_data = pyspark_module.collect_data()
        if transformed_data is not None:
            return transformed_data
    return None


def get_report_data(channel_name):
    key = channel_name
    cached_valid = False
    if key not in cache:
        cache[key] = generate_report_data(channel_name)
        cached_valid = False
    else:
        cached_valid = True
    return cache[key], cached_valid


def generate_report_history_data(username):
    with History_app.app_context():
        history_records = HistoryRecord.query.filter_by(username=username).all()
    if history_records:
        history_data = []
        for record in history_records:
            data_dict = json.loads(record.data)
            history_data.append(
                {"channel_id": record.channel_id, "channel_name": record.channel_name, "data": data_dict,
                 "date_created": record.date_created})
        return history_data
    return None


def get_report_history_data(username):
    key = username
    cached_valid = False
    if key not in history_cache:
        history_cache[key] = generate_report_history_data(username)
        cached_valid = False
    else:
        cached_valid = True
    return history_cache[key], cached_valid

#
# if __name__ == "__main__":
#     username = "minhlenguyen023@gmail.com"
#     data, valid = get_report_history_data(username)
#     print(type(data[0]["data"]))
#     keys_list = data[0]["date_created"]
#     print(type(data[0]["date_created"]))
#     print(keys_list)