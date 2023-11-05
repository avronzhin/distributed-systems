import datetime

import streamlit as st

import date_utils
import start_server_client as stats

stats.init()
if not stats.stats_server_is_available():
    st.error("Сервис статистики не доступен")
    st.stop()

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

if start_date >= end_date:
    st.error("Выбранный период некорректен. Начало периода должно быть раньше конца периода, как минимум на один день")
    st.stop()

start_date_timestamp = date_utils.get_timestamp_from_date(start_date)
end_date_timestamp = date_utils.get_timestamp_from_date(end_date)

# Получить все данные сразу, иначе 24 запроса во 2 задании очень долго
all_logs = stats.get_logs_in_period_group_by_operation_type(start_date_timestamp, end_date_timestamp)
logs_group_by_operation = dict()
for log in all_logs:
    operation_id = log["operation_type_id"]
    if operation_id in logs_group_by_operation:
        logs_group_by_operation[operation_id].append(log)
    else:
        logs = list()
        logs.append(log)
        logs_group_by_operation[operation_id] = logs

# Количество вызовов
data = {}
for operation_id in logs_group_by_operation.keys():
    operation_type = list(filter(lambda it: it["id"] == operation_id, operation_types))[0]["title"]
    data[operation_type] = len(logs_group_by_operation[operation_id])
st.subheader("Количество вызовов по типу операции")
st.bar_chart(data)


# Количество вызовов по времени
if operation is None:
    st.subheader("Количество вызовов по времени для всех типов операций")
else:
    st.subheader("Количество вызовов по времени для типа операции '{}'".format(operation))

days = list()
day = start_date
while day < end_date:
    days.append(day)
    day = day + datetime.timedelta(days=1)

interval_timestamp = interval * 60 * 60
days_timestamps = list()
for day in days:
    next_day = day + datetime.timedelta(days=1)
    next_day_timestamp = date_utils.get_timestamp_from_date(next_day)
    day_timestamp = date_utils.get_timestamp_from_date(day)
    day_timestamps = list()
    while day_timestamp < next_day_timestamp:
        day_timestamps.append(day_timestamp)
        day_timestamp = day_timestamp + interval_timestamp
    days_timestamps.append(day_timestamps)

for day_timestamps in days_timestamps:
    day_timestamp = day_timestamps[0]
    day_date = date_utils.get_date_from_timestamp(day_timestamp).date()
    st.subheader(day_date)
    data = {}
    for timestamp in day_timestamps:
        next_timestamp = timestamp + interval_timestamp
        # TODO из всех логов достать те который в этих интервалах
        #count = stats.get_count_in_period_by_operation_type(timestamp, next_timestamp, operation_types[1]["title"])
        # date = date_utils.get_date_from_timestamp(timestamp)
        # data[str(date)] = count
    # print(data)
    # st.bar_chart(data)
# гистограмму по количеству вызова для типов операций на сутки (горизонтальная ось гистограммы – время 00:00-24:00 с заданными интервалом «slider» группировки, вертикальная ось – количество вызовов). Если тип операции «text_input» задан, то гистограмма строится для заданного типа операции, иначе – для всех.


# круговую диаграмму по количеству вызовов типа операции (размер сектора типа пропорционален количеству вызовов типа операции).

# labels = ["a", "b", "c", "d"]
# sizes = [15, 30, 45, 10]
#
# fig, ax = plt.subplots()
# ax.pie(sizes, labels=labels)
# st.pyplot(fig)

# построить круговую диаграмму по времени вызовов типа операции (размер сектора типа пропорционален времени выполнения типа операции).
