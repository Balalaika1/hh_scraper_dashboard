import streamlit as st
import pandas as pd
from defs import hh_to_df, list_columns_dicts, spliting_columns, map_f, number_of_vacancies, average_value_salary_from_to
import plotly.express as px

citys_list = {"Москва":1,
"Санкт-Петербург":2,
"Екатеринбург":3,
"Новосибирск":4,
"Ростов-на-Дону":76}

df = pd.DataFrame()

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
    st.markdown("---")
    period = st.slider('The number of days within which the vacancy is published on the site 📆', 1, 100, 1)
    value_area = citys_list[radio_widget]
    if st.button('Refresh'):
        df = hh_to_df(title, value_area, period)
        df = spliting_columns(list_columns_dicts(df), df)
        df = spliting_columns(list_columns_dicts(df), df)
        df.to_excel('main3.xlsx')
if df.empty == False:
    tab1, tab2 = st.tabs(["📊 Analysis and visualization", "🤖 Automation"])
    with tab1:
        a = number_of_vacancies(df)
        b = average_value_salary_from_to(df)
        c1, c2, c3 = st.columns(3)
        c1.metric("Vacancies found", a[0])
        c2.metric("Vacancies where salary specified", a[1])
        c3.metric("Average salary", b)
        fig = map_f(df)
        st.plotly_chart(fig, use_container_width=True)
        with st.expander("Download table 📥"):
            st.dataframe(df)
            with open("main3.xlsx", "rb") as file:
                btn = st.download_button(
                        label="Download excel file",
                        data=file,
                        file_name="main.xlsx"
                      )
else:
    st.markdown('<h3>Select the data and click the refresh button 😉</h3>',unsafe_allow_html=True)

st.set_page_config(page_title="HH Interactive Dashboard", page_icon="📊")

