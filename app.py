import streamlit as st
import pandas as pd
import duckdb
import io

csv = '''
beverage,price
orange juice,2.5
Expresso,2
Tea,3
'''

beverages = pd.read_csv(io.StringIO(csv))

csv2 = '''
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
'''

food_items = pd.read_csv(io.StringIO(csv2))

# checks
answer = """
SELECT * FROM beverages
CROSS JOIN food_items
"""
duckdb.sql(answer)

solution = duckdb.sql(answer).df()

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


st.header("Entrez votre code :")
query = st.text_area(label="Votre code SQL ici :", key="user_input")

if query:
    result = duckdb.sql(query).df()
    st.dataframe(result)


tab1, tab2 = st.tabs(["Tables", "Solution"])


with tab1:
    st.write("table: beverages")
    st.dataframe(beverages)
    st.write("table: food_items")
    st.dataframe(food_items)
    st.write("expected")
    st.dataframe(solution)


with tab2:
    st.write(answer)