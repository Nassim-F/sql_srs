# pylint: disable=missing-module-docstring
import io
import random

import duckdb
import pandas as pd
import numpy as np

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
        "group_by",
        "group_by",
        "group_by",
        "group_by",
    ],
    "exercise_name": [
        "beverages_and_food",
        "sizes_and_trademarks",
        "hours_and_quarters",
        "employees",
        "sales",
        "meetings_durations_self_join",
        "real_estate_sales",
        "mean_price_per_city",
        "panier_moyen_client",
        "mean_sales",
    ],
    "tables": [
        ["beverages", "food_items"],
        ["sizes", "trademarks"],
        ["hours", "quarters"],
        ["employees"],
        ["sales"],
        ["meetings_durations"],
        ["ventes_immo"],
        ["appt_nord"],
        ["ventes"],
        ["ventes"],
    ],
    "last_reviewed": [
        "1980-01-01",
        "1970-01-01",
        "1970-01-01",
        "1970-01-01",
        "1970-01-01",
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

# ----------------------------
#       FULL OUTER JOIN
# ----------------------------

customers_data = {
    'customer_id': [11, 12, 13, 14, 15],
    'customer_name': ["Zeinaba", "Tancrède", "Israel", "Kaouter", "Alan"]
}
df_customers = pd.DataFrame(customers_data)

stores_data = {
    'store_id': [1, 2, 3, 4],
    'customer_id': [11, 12, 13, 15]
}
df_stores = pd.DataFrame(stores_data)

store_products_data = {
    'store_id': [1, 1, 1, 2, 2, 3, 4],
    'product_id': [101, 103, 105, 101, 103, 104, 105],
}
df_store_products = pd.DataFrame(store_products_data)

p_names = ["Cherry coke", "Laptop", "Ipad", "Livre",]
products_data = {
    'product_id': [100, 101, 103, 104],
    'product_name': p_names,
    'product_price': [3, 800, 400, 30]
}
df_products = pd.DataFrame(products_data)







dates = [f"2023-08-{str(x).zfill(2)}" for x in range(7, 21)]

ventes_immo = pd.DataFrame([
    [0, "vieux_lille", 460000],
    [1, "vieux_lille", 430000],
    [2, "vieux_lille", 450000],
    [3, np.nan, 470000],
    [4, "vieux_lille", 440000],
    [10, "gambetta", 336000],
    [11, np.nan, 333000],
    [12, "gambetta", 335000],
    [13, "gambetta", 337000],
    [14, "gambetta", 334000],
    [20, "centre", 356000],
    [21, "centre", 353000],
    [22, np.nan, 355000],
    [23, "centre", 357000],
    [24, "centre", 354000],
    [30, "wazemmes", 260000],
    [31, np.nan, 230000],
    [32, "wazemmes", 250000],
    [33, "wazemmes", 270000],
    [34, "wazemmes", 240000],
]
)

ventes_immo.columns = ["flat_id",
                       "neighborhood",
                       "price"]

con.execute(
    "CREATE TABLE IF NOT EXISTS ventes_immo AS SELECT * FROM ventes_immo"
)


# ------------

appt_nord = pd.read_csv("data/appartements_nord_pdc.csv", sep=",")

con.execute(
    "CREATE TABLE IF NOT EXISTS appt_nord AS SELECT * FROM appt_nord"
)

# -------------- GROUP BY, CTE, HAVING exercise

clients = ["Oussama", "Julie", "Chris", "Tom", "Jean-Nicolas", "Aline", "Ben", "Toufik", "Sylvie", "David"]
ventes = [110, 49, 65, 23, 24, 3.99, 29, 48.77, 44, 10, 60, 12, 62, 19, 75] * 2

ventes = pd.DataFrame(ventes)
ventes.columns = ["montant"]
ventes["client"] = clients * 3


con.execute(
    "CREATE TABLE IF NOT EXISTS ventes AS SELECT * FROM ventes"
)


con.close()
