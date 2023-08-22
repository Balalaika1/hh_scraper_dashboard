import requests
import pandas as pd
import plotly.express as px
import json
import streamlit as st


def hh_to_df(text, area, period):
    df_main = pd.DataFrame()
    frames = []
    for i in range(0, 21):
        print(i, 21)
        url = 'https://api.hh.ru/vacancies'
        params = {'page': i,
                  'per_page':100,
                  'text':f'!{text}', # Если необходимо найти слово или словосочетание именно в той форме, которая указана в поисковом запросе, поставьте перед ним восклицательный знак. (https://hh.ru/article/1175)
                  'area': area,
                  'period':period}

        html = requests.get(url, params = params)
        if html.status_code == 200:
            data = html.text

            data_json = json.loads(data)
            if data_json['items'] != []:
                names = data_json['items'][0].keys()
                data = data_json['items'][0]
                df = pd.DataFrame(data_json['items'])
                frames.append(df)
    result = pd.concat(frames)
    return result


def list_columns_dicts(df):
    # Получаем список названий столбцов в DataFrame
    columns_list = df.columns
    
    # Создаем пустой список для хранения названий столбцов с данными в виде словарей
    d_list = []
    
    # Проходимся по каждому столбцу из списка
    for column in columns_list:
        # Удаляем строки с отсутствующими (NaN) значениями из столбца
        series_no_nan = df[column].dropna()
        
        # Проверяем, что столбец не пустой после удаления NaN значений
        if not series_no_nan.empty:
            # Проверяем, является ли первое значение в столбце словарем
            if type(series_no_nan.iloc[0]) == dict:
                # Добавляем название столбца в список, если условие выполняется
                d_list.append(column)


       # Получаем список названий столбцов в DataFrame
    columns_list = df.columns
    
    # Создаем пустой список для хранения названий столбцов с данными в виде словарей
    d_list2 = []
    
    # Проходимся по каждому столбцу из списка
    for column in columns_list:
        # Удаляем строки с отсутствующими (NaN) значениями из столбца
        series_no_nan = df[column].dropna()
        
        # Проверяем, что столбец не пустой после удаления NaN значений
        if not series_no_nan.empty:
            # Проверяем, является ли первое значение в столбце словарем
            if type(series_no_nan.iloc[0]) == list:
                # Добавляем название столбца в список, если условие выполняется
                d_list2.append(column)
    
    # Возвращаем список названий столбцов, соответствующих условиям
    d_list_result = d_list + d_list2
    return d_list_result

def spliting_columns(name_lists_list, df2):
    # Проходимся по каждому имени столбца из переданного списка
    for name in name_lists_list:
        try:
            # Создаем новый столбец, который содержит информацию о том, равно ли значение None
            df2[f'{name}_None'] = df2[name].apply(lambda x: x is None)
            
            # Получаем список уникальных ключей из словарей в столбце и разбиваем его на отдельные строки
            keys_list = df2[name].apply(lambda x: x.keys() if isinstance(x, dict) else [])
            keys_list = keys_list.explode().unique()
            # Проходимся по каждому уникальному ключу и создаем новый столбец с соответствующим значением
            for i in keys_list:
                df2[f'{name}_{i}'] = df2[name].apply(lambda x: x.get(i) if isinstance(x, dict) and x is not None else None)
            
            # Удаляем исходный столбец после его разделения
            del df2[name]
        except:
            continue
    
    # Возвращаем DataFrame с разделенными столбцами
    return df2

@st.cache_data
def map_f(df1):
    df = df1
    df = df.dropna(subset=['salary_from'])
    fig = px.scatter_mapbox(df, lat='address_lat', lon='address_lng',size = 'salary_from', size_max=10, color='salary_currency')
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


def number_of_vacancies(df):
    false_count = int(df['salary_None'].value_counts()[True])
    b=int(len(df))
    list_vacancies = [b, false_count]
    return list_vacancies

def average_value_salary_from_to(df):
    df = df[df['salary_currency'] == 'RUR']
    average_value1 = df['salary_from'].mean()
    average_value2 = df['salary_to'].mean()
    average_value = int((average_value1+average_value2)//2)
    return average_value
