# pylint: disable=missing-module-docstring

import logging
import os
import subprocess
import sys

import duckdb
import streamlit as st

if "data" not in os.listdir():
    logging.error(os.listdir())
    logging.error("creating folder data")
    os.mkdir("data")

if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    subprocess.run([sys.executable, "init_db.py"], check=False)

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)


def check_users_solution(user_query: str) -> None:
    """
    Checks that user SQL query is correct by:
    1: checking the columns
    2: checking the values
    :param user_query: a string containing the query inserted by the user
    """
    result = con.execute(user_query).df()
    st.dataframe(result)
    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
    except KeyError:
        st.write("Some columns are missing")
    n_lines_difference = result.shape[0] - solution_df.shape[0]
    if n_lines_difference != 0:
        st.write(
            f"result has a {n_lines_difference} lines difference with the solution"
        )


with st.sidebar:
    themes = con.execute("SELECT DISTINCT theme FROM memory_state").df()

    theme = st.selectbox(
        "What would you like to review?",
        themes["theme"].unique(),
        index=None,
        placeholder="Select a theme...",
    )

    if theme:
        st.write(f"You selected {theme}")
        SELECT_EXERCISE_QUERY = f"SELECT * FROM memory_state WHERE theme = '{theme}'"
    else:
        SELECT_EXERCISE_QUERY = "SELECT * FROM memory_state"

    exercise = (
        con.execute(SELECT_EXERCISE_QUERY)
        .df()
        .sort_values("last_reviewed")
        .reset_index()
    )

    st.write(exercise)

    exercise_name = exercise.loc[0, "exercise_name"]
    with open(f"answers/{exercise_name}.sql", "r", encoding="utf-8") as f:
        answer = f.read()

    solution_df = con.execute(answer).df()

st.header("Entrez votre code :")
query = st.text_area(label="Votre code SQL ici :", key="user_input")


if query:
    check_users_solution(query)

tab1, tab2 = st.tabs(["Tables", "Solution"])
#
#
with tab1:

    exercise_tables = exercise.loc[0, "tables"]

    for table in exercise_tables:
        st.write(f"table : {table}")
        df_table = con.execute(f"select * from {str(table)}")
        st.dataframe(df_table)

#     st.write("table: beverages")
#     st.dataframe(beverages)
#     st.write("table: food_items")
#     st.dataframe(food_items)
#     st.write("expected")
#     st.dataframe(solution_df)
#
#
with tab2:
    st.write(answer)
