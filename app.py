import streamlit as st
import pandas as pd
import duckdb

st.write("""
# SQL SRS
Spaced Repetitin System SQL practice
""")
with st.sidebar:
    option = st.selectbox(
        "What would you like to review?",
        ("Joins", "GroupBy", "Windows Functions"),
        index=None,
        placeholder="Select a theme...",
    )

    st.write("You selected:", option)

data = {"a" : [1, 2, 3], "b" : [4, 5, 6]}
df = pd.DataFrame(data)

tab1, tab2 = st.tabs(["test_input", "test_v2"])


with tab1:
    sql_query = st.text_area(label="entrez votre input")
    result = duckdb.query(sql_query).df()
    st.write(f"Vous avez entré la requête suivante : {sql_query}")
    st.dataframe(result)
