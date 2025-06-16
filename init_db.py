# pylint: disable=missing-module-docstring
import io
import random

import duckdb
import pandas as pd

random.seed(42)

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

# ----------------------------
#       EXERCISES LIST
# ----------------------------

data = {
    "theme": [
        "cross_joins",
        "cross_joins",
        "cross_joins",
        "self_join",
        "self_join",
        "self_join",
    ],
    "exercise_name": [
        "beverages_and_food",
        "sizes_and_trademarks",
        "hours_and_quarters",
        "employees",
        "sales",
        "meetings_durations_self_join",
    ],
    "tables": [
        ["beverages", "food_items"],
        ["sizes", "trademarks"],
        ["hours", "quarters"],
        ["employees"],
        ["sales"],
        ["meetings_durations"],
    ],
    "last_reviewed": [
        "1980-01-01",
        "1970-01-01",
        "1970-01-01",
        "1970-01-01",
        "1970-01-01",
        "1970-01-01",
    ],
}
memory_state_df = pd.DataFrame(data)
con.execute("CREATE TABLE IF NOT EXISTS memory_state AS SELECT * FROM memory_state_df")

# ----------------------------
#       CROSS JOIN
# ----------------------------

CSV = """
beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""

beverages = pd.read_csv(io.StringIO(CSV))
con.execute("CREATE TABLE IF NOT EXISTS beverages AS SELECT * FROM beverages")

CSV2 = """
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
"""

food_items = pd.read_csv(io.StringIO(CSV2))
con.execute("CREATE TABLE IF NOT EXISTS food_items AS SELECT * FROM food_items")

CSV3 = """
size
XS
M
L
XL
"""

sizes = pd.read_csv(io.StringIO(CSV3))
con.execute("CREATE TABLE IF NOT EXISTS sizes AS SELECT * FROM sizes")

CSV4 = """
trademark
Nike
Asphalte
Abercrombie
Lewis
"""

trademarks = pd.read_csv(io.StringIO(CSV4))
con.execute("CREATE TABLE IF NOT EXISTS trademarks AS SELECT * FROM trademarks")


CSV5 = """
hour
08
09
10
11
12
"""

hours = pd.read_csv(io.StringIO(CSV5))
con.execute("CREATE TABLE IF NOT EXISTS hours AS SELECT * FROM hours")

CSV6 = """
quarter
00
15
30
45
"""

quarters = pd.read_csv(io.StringIO(CSV5))
con.execute("CREATE TABLE IF NOT EXISTS quarters AS SELECT * FROM quarters")

# -------------------------- EMPLOYEES SELF JOIN

employees_data = {
    "employee_id": [11, 12, 13, 14, 15],
    "employee_name": ["Sophie", "Sylvie", "Daniel", "Kaouter", "David"],
    "manager_id": [13, None, 12, 13, 11],
}

employees = pd.DataFrame(employees_data)
con.execute("CREATE TABLE IF NOT EXISTS employees AS SELECT * FROM employees")

# -------------------------- SALES SELF JOIN

sales_data = {
    "order_id": list(range(1110, 1198)),
    "customer_id": random.choices([11, 12, 13, 14, 15, 11, 12, 13, 14], k=88),
}

sales = pd.DataFrame(sales_data)
sales["date"] = [d // 3 + 1 for d in range(1, 89)]
con.execute("CREATE TABLE IF NOT EXISTS sales AS SELECT * FROM sales")

# -------------------------- MEETINGS DURATION SELF JOIN

person_names = ["Benjamin", "Florian", "Tarik", "Bob", "Sirine", "Alice"]

meetings_data = []
for meeting_id in range(150):
    persons_in_meet = random.sample(person_names, random.randint(1, 5))
    for person_name in persons_in_meet:
        meetings_data.append((meeting_id, person_name))


meetings_df = pd.DataFrame(meetings_data, columns=["meeting_id", "person_name"])

meeting_durations = []
for meeting_id in meetings_df["meeting_id"].unique():
    duration = random.randint(10, 60)  # You can adjust the range as needed
    meeting_durations.append((meeting_id, duration))

durations_df = pd.DataFrame(
    meeting_durations, columns=["meeting_id", "duration_minutes"]
)

average_duration = durations_df["duration_minutes"].mean()
meetings_with_flo = meetings_df[meetings_df["person_name"] == "Florian"][
    "meeting_id"
].unique()
# meetings_with_ben = meetings_df[meetings_df["person_name"] == "Benjamin"]["meeting_id"].unique()
# s=set(meetings_with_ben) & set(meetings_with_flo)
for _, row in durations_df.iterrows():
    if row["meeting_id"] in meetings_with_flo:
        row["duration_minutes"] += random.randint(
            50, 55
        )  # Add extra minutes to meet the condition

meetings_durations = meetings_df.merge(durations_df, on="meeting_id")

con.execute(
    "CREATE TABLE IF NOT EXISTS meetings_durations AS SELECT * FROM meetings_durations"
)


con.close()
