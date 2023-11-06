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


def get_log_count_by_operation(logs_group_by_operation: dict):
    log_count_by_operation = dict()
    for operation_id in logs_group_by_operation.keys():
        log_count_by_operation[operation_id] = len(logs_group_by_operation[operation_id])
    return log_count_by_operation


def get_operation_type_id_by_title(operation_types: list, title: str):
    return list(filter(lambda it: it["title"] == title, operation_types))[0]["id"]


def get_operation_type_title_by_id(operation_types: list, operation_id: int):
    return list(filter(lambda it: it["id"] == operation_id, operation_types))[0]["title"]


def get_log_count_in_period(logs, current_timestamp, next_timestamp):
    return len(list(filter(lambda it: current_timestamp <= it["created"] < next_timestamp, logs)))


def get_avg_duration_by_operation(logs_group_by_operation: dict):
    avg_duration_by_operation = dict()
    for operation_id in logs_group_by_operation.keys():
        logs = logs_group_by_operation[operation_id]
        avg_duration_by_operation[operation_id] = average(list(map(lambda it: it["duration"], logs)))
    return avg_duration_by_operation


def average(source_list: list):
    return sum(source_list) / len(source_list)
