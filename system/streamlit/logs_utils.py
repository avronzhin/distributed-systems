import date_utils


def group_log_by_operation(all_logs: list):
    logs_group_by_operation = dict()
    for log in all_logs:
        operation_id = log["operation_type_id"]
        if operation_id in logs_group_by_operation:
            logs_group_by_operation[operation_id].append(log)
        else:
            logs = list()
            logs.append(log)
            logs_group_by_operation[operation_id] = logs
    return logs_group_by_operation


def extract_log_count_by_operation(logs_group_by_operation: dict):
    log_count_by_operation = dict()
    for operation_id in logs_group_by_operation.keys():
        log_count_by_operation[operation_id] = len(logs_group_by_operation[operation_id])
    return log_count_by_operation


def extract_operation_type_id_by_title(operation_types: list, title: str):
    return list(filter(lambda it: it["title"] == title, operation_types))[0]["id"]


def extract_operation_type_title_by_id(operation_types: list, operation_id: int):
    return list(filter(lambda it: it["id"] == operation_id, operation_types))[0]["title"]


def get_log_count_in_period(logs, current_timestamp, next_timestamp):
    return len(list(filter(lambda it: current_timestamp <= it["created"] < next_timestamp, logs)))


def extract_avg_duration_by_operation(logs_group_by_operation: dict):
    avg_duration_by_operation = dict()
    for operation_id in logs_group_by_operation.keys():
        logs = logs_group_by_operation[operation_id]
        avg_duration_by_operation[operation_id] = average(list(map(lambda it: it["duration"], logs)))
    return avg_duration_by_operation


def average(source_list: list):
    return sum(source_list) / len(source_list)


def get_log_count_by_day_splitting_by_interval(days: list, interval: int, logs: list):
    log_count_by_day_splitting_by_interval = dict()
    for day in days:
        day_timestamps, interval_timestamp = date_utils.split_day_by_interval(day, interval)
        timestamps_log_count = []
        for current_timestamp in day_timestamps:
            next_timestamp = current_timestamp + interval_timestamp
            current_timestamp_log_count = get_log_count_in_period(logs, current_timestamp, next_timestamp)
            timestamps_log_count.append({"timestamp": current_timestamp, "count": current_timestamp_log_count})
        log_count_by_day_splitting_by_interval[day] = timestamps_log_count
    return log_count_by_day_splitting_by_interval


def extract_logs_for_operation_by_title(operation_types: list, operation: str, logs_group_by_operation: dict):
    operation_type_id = extract_operation_type_id_by_title(operation_types, operation)
    if operation_type_id in logs_group_by_operation:
        return logs_group_by_operation[operation_type_id]
    else:
        return []
