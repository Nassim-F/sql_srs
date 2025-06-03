# pylint: disable=missing-module-docstring
import ast

import duckdb
import streamlit as st


con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

with st.sidebar:
    themes = con.execute("SELECT theme FROM memory_state").df()

    theme = st.selectbox(
        "What would you like to review?",
        (t for t in themes.theme.tolist()),
        index=None,
        placeholder="Select a theme...",
    )

    exercise = con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}' ").df()
    st.write("You selected:", theme)

    st.write(exercise)

    exercise_name = exercise.loc[0, "exercise_name"]
    with open(f"answers/{exercise_name}.sql", "r", encoding="utf-8") as f:
        answer = f.read()

    solution_df = con.execute(answer).df()

st.header("Entrez votre code :")
query = st.text_area(label="Votre code SQL ici :", key="user_input")

if query:
    result = con.execute(query).df()
    st.dataframe(result)

    try:
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
#
#
with tab1:

    exercise_tables = ast.literal_eval(exercise.loc[0, "tables"])

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
