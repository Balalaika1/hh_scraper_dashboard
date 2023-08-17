import streamlit as st
import pandas as pd
from defs import hh_to_df, list_columns_dicts, spliting_columns, map_f, number_of_vacancies
import plotly.express as px

citys_list = {"Москва":1,
"Санкт-Петербург":2,
"Екатеринбург":3,
"Новосибирск":4,
"Ростов-на-Дону":76}

#df = pd.DataFrame()
#------------------------------------Убрать
df = pd.read_excel('main3.xlsx')
#------------------------------------Убрать

with st.sidebar:
    st.markdown(
            '<h3><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/79/HeadHunter_logo.png/200px-HeadHunter_logo.png" height="40">&nbsp Interactive Dashboard</h3>',
            unsafe_allow_html=True,
        )
    st.markdown(
            '<h6>by <a href="https://github.com/Balalaika1">Balalaika1</a></h6>',
            unsafe_allow_html=True,
        )
    st.markdown("---")
    title = st.text_input('Сhoose a profession 👷', 'Аналитик')
    st.markdown("---")
    radio_widget = st.radio(
        label="Select a city 🏙️",
        key="visibility",
        options=citys_list.keys(),
    )
    value_area = citys_list[radio_widget]
    if st.button('Refresh'):
        df = hh_to_df(title, value_area)
        df = spliting_columns(list_columns_dicts(df), df)
        df = spliting_columns(list_columns_dicts(df), df)
        #df.to_excel('main3.xlsx')
if df.empty == False:
    a = number_of_vacancies(df)
    c1, c2, c3 = st.columns(3)
    c1.metric("Vacancies found", a[0])
    c2.metric("Vacancies where salary not specified", a[1])

    fig = map_f(df)
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df)
else:
    st.markdown('<h3>Select the data and click the refresh button 😉</h3>',unsafe_allow_html=True)

