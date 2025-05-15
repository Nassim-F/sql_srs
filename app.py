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
answer_str = """
SELECT * FROM beverages
CROSS JOIN food_items
"""
duckdb.sql(answer_str)

solution_df = duckdb.sql(answer_str).df()

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


    try :
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
    except KeyError as e:
        st.write("Some columns are missing")

    n_lines_difference = result.shape[0] - solution_df.shape[0]
    if n_lines_difference != 0:
        st.write(
            f"result has a {n_lines_difference} lines difference with the solution"
        )



tab1, tab2 = st.tabs(["Tables", "Solution"])


with tab1:
    st.write("table: beverages")
    st.dataframe(beverages)
    st.write("table: food_items")
    st.dataframe(food_items)
    st.write("expected")
    st.dataframe(solution_df)


with tab2:
    st.write(answer_str)