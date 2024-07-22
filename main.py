import pandas as pd
import streamlit as st
import altair as alt
import numpy as np

st.set_page_config(
    page_title="Dashboard for movies dataset",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Define your custom CSS styles
custom_css = """
<style>
    .main .block-container {{
        padding-top: 1rem;
    }}
    .css-1d391kg {{
        background-color: #F0F2F6;
    }}
    .stButton > button {{
        color: white;
        background-color: #F63366;
    }}
</style>
"""

# Apply custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

st.title("Interactive Movie Dashboard")

with st.expander("About this app"):
    st.markdown("What can this app do")
    st.info("This app shows the use of pandas for data wrangling")
    st.markdown("How to use this app")
    st.info("To engage with the app,  \n 1) Select the Genres \n 2) Select the years range of the movies \n ")

st.subheader("Which Movie Genre performs ($) best at the box office")

df = pd.read_csv("venv/movies_genres_summary.csv")
df.year = df.year.astype('int')

genres_list = df.genre.unique()
genres_selection = st.multiselect('Select Genres', genres_list, ["Action", "Biography"])

year_list = df.year.unique()
year_selection = st.slider('Select year', 1986, 2023, (2000, 2016))
year_selection_list = list(np.arange(year_selection[0], year_selection[1] + 1))

df_selection = df[df.genre.isin(genres_selection) & df["year"].isin(year_selection_list)]
reshaped_df = df_selection.pivot_table(index="year", columns="genre", values="gross", aggfunc="sum", fill_value=0)
reshaped_df = reshaped_df.sort_values(by="year", ascending=False)

df_editor = st.data_editor(
    reshaped_df,
    height=212,
    use_container_width=True,
    column_config={"year": st.column_config.TextColumn("Year")},
    num_rows="dynamic",
)

df_chart = pd.melt(df_editor.reset_index(), id_vars="year", var_name="genre", value_name="gross")

chart = alt.Chart(df_chart).mark_line().encode(
    x=alt.X("year:N", title="Year"),
    y=alt.Y("gross:Q", title="Gross earnings ($)"),
    color="genre:N",
).properties(height=320)
st.altair_chart(chart, use_container_width=True)

df_selection = df[df.genre.isin(genres_selection)]
genre_totals = df_selection.groupby('genre')['gross'].sum().reset_index()

# Pie Chart
pie_chart = alt.Chart(genre_totals).mark_arc().encode(
    theta=alt.Theta('gross:Q', stack=True, title='Gross earnings ($)'),
    color=alt.Color('genre:N', title='Genre'),
    tooltip=['genre', 'gross']
).properties(height=320, width=600)

st.altair_chart(pie_chart, use_container_width=True)

