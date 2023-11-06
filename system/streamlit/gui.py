import datetime

import streamlit as st
from matplotlib import pyplot as plt

import date_utils
import logs_utils
import start_server_client as stats

stats.init()
if not stats.stats_server_is_available():
    st.error("Сервис статистики не доступен")
    st.stop()

# UI
operation_types = stats.get_operation_types()
st.sidebar.header("Параметры")
st.sidebar.subheader('Период анализа')
today = datetime.datetime.today()
tomorrow = today + datetime.timedelta(days=1)
start_date = st.sidebar.date_input('Начало периода', max_value=today, value=today)
end_date = st.sidebar.date_input('Конец периода (невключительно)', max_value=tomorrow, value=tomorrow)
interval = st.sidebar.slider('Интервал анализа данных, часы', 1, 4, 24)
options = list(map(lambda it: it["title"], operation_types))
operation = st.sidebar.selectbox('Тип операции', options=options, index=None, on_change=None)
st.write("## Аналитика работы веб-сервиса")

# Валидация
if start_date >= end_date:
    st.error("Выбранный период некорректен. Начало периода должно быть раньше конца периода, как минимум на один день")
    st.stop()

# Подготовка входный данных
operation_type_selected = operation is not None
start_date_timestamp = date_utils.get_timestamp_from_date(start_date)
end_date_timestamp = date_utils.get_timestamp_from_date(end_date)

# Загрузка и обработка данных статистики
all_logs = stats.get_logs_in_period_group_by_operation_type(start_date_timestamp, end_date_timestamp)
logs_group_by_operation = logs_utils.group_log_by_operation(all_logs)
log_count_by_operation = logs_utils.get_log_count_by_operation(logs_group_by_operation)
days = date_utils.split_by_days(start_date, end_date)
log_count_by_day_splitting_by_interval = dict()
# TODO вынести в функцию
for day in days:
    day_timestamps, interval_timestamp = date_utils.split_day_by_interval(day, interval)
    timestamps_log_count = []
    for current_timestamp in day_timestamps:
        next_timestamp = current_timestamp + interval_timestamp
        logs = all_logs
        if operation_type_selected:
            operation_type_id = logs_utils.get_operation_type_id_by_title(operation_types, operation)
            if operation_type_id in logs_group_by_operation:
                logs = logs_group_by_operation[operation_type_id]
            else:
                logs = []
        current_timestamp_log_count = logs_utils.get_log_count_in_period(logs, current_timestamp, next_timestamp)
        timestamps_log_count.append({"timestamp": current_timestamp, "count": current_timestamp_log_count})
    log_count_by_day_splitting_by_interval[day] = timestamps_log_count
avg_duration_by_operation = logs_utils.get_avg_duration_by_operation(logs_group_by_operation)

# Подготовка к отрисовке
log_count_by_operation_title = dict()
for key in log_count_by_operation.keys():
    title = logs_utils.get_operation_type_title_by_id(operation_types, key)
    log_count_by_operation_title[title] = log_count_by_operation[key]
avg_duration_by_operation_title = dict()
for key in avg_duration_by_operation.keys():
    title = logs_utils.get_operation_type_title_by_id(operation_types, key)
    avg_duration_by_operation_title[title] = avg_duration_by_operation[key]


# Отрисовка
st.subheader("Количество вызовов по типу операции")
st.bar_chart(log_count_by_operation_title)

if operation_type_selected:
    st.subheader("Количество вызовов по времени для типа операции '{}'".format(operation))
else:
    st.subheader("Количество вызовов по времени для всех типов операций")

for day in log_count_by_day_splitting_by_interval.keys():
    st.subheader(day)
    # TODO Вывести красиво
    log_count_by_timestamp = log_count_by_day_splitting_by_interval[day]
    data = list(map(lambda it: {datetime.datetime.fromtimestamp(it["timestamp"]).hour: it["count"]}, log_count_by_timestamp))
    st.bar_chart(data)

fig, ax = plt.subplots()
ax.pie(log_count_by_operation_title.values(), labels=log_count_by_operation_title.keys())
st.subheader("Количество вызовов по типу операции")
st.pyplot(fig)

st.subheader("Среднее время выполнения операции")
fig, ax = plt.subplots()
ax.pie(avg_duration_by_operation_title.values(), labels=avg_duration_by_operation_title.keys())
st.pyplot(fig)
