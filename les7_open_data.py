# 1) Создать приложение, которое будет из готового файла с данными «Сбербанка»
# (https://www.sberbank.com/ru/analytics/opendata) выводить результат
# по параметрам: • Тип данных • Интервал дат • Область
#
# 2) Визуализировать выводимые данные с помощью графика

import csv
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
# This import need for register date type converting
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


def visualization_pandas(name: str, aria: str, start_date: str, end_date):
    df = pd.read_csv('opendata.csv')
    df['date'] = pd.to_datetime(df['date'])
    df2 = df.loc[(df['name'] == name) &
                 (df['region'] == aria) &
                 (df['date'] > start_date) &
                 (df['date'] < end_date)]
    print(df2)
    plt.plot(df2['date'], df2['value'])
    plt.title(f'{name} \nза период от {start_date} до {end_date}\nРегион - {aria}')
    plt.ylabel('Value')
    plt.xlabel('Date')
    plt.grid(True)
    plt.show()


def visualization_csv(name: str, aria: str, start_date: str, end_date):
    format_date = '%Y-%m-%d'
    row_start_date = datetime.strptime(start_date, format_date).date()
    row_end_date = datetime.strptime(end_date, format_date).date()
    with open('opendata.csv', 'r') as f:
        reader = csv.DictReader(f)
        value = []
        date = []
        for row in reader:
            row_date = datetime.strptime(row['date'], format_date).date()
            if row['name'] == name and row['region'] == aria and row_start_date < row_date < row_end_date:
                date.append(row['date'])
                value.append(int(row['value']))
    plt.plot(date, value)
    plt.title(f'{name} \nза период от {start_date} до {end_date}\nРегион - {aria}')
    plt.ylabel('Value')
    plt.xlabel('Date')
    plt.grid(True)
    plt.show()


visualization_pandas('Средние расходы по картам', 'Москва', '2016-06-01', '2017-06-01')
visualization_csv('Средняя зарплата', 'Москва', '2017-09-01', '2018-03-01')
