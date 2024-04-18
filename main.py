import sqlite3
import streamlit as st
import pandas as pd
import random

conn = sqlite3.connect('ft_dbms.db')
c = conn.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS foodtable(rest_name TEXT)')

def add_data(rest_name):
    try:
        c.execute('INSERT INTO foodtable(rest_name) VALUES (?)', (rest_name,))  # Notice the comma
    except sqlite3.Error as e:  # Or your specific database error class
        print("Error:", e)

    conn.commit()


def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

def get_table():
    query = c.execute('SELECT * FROM foodtable')
    cols = [column[0] for column in query.description]
    results = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
    return results

st.title('Saan Kakain?')

create_table()
confirm = st.button('Generate Suggestion')
st.sidebar.subheader("Add Restaurant Choices")
restaurant = st.sidebar.text_input("Restaurant Name: ")
add_ = st.sidebar.button('Submit Restaurant?')
if add_:
    add_data(str(restaurant))

if confirm:
    df = get_table()
    dupes = df.loc[df.duplicated()]
    df.drop(dupes.index, inplace=True)
    options = list(df.rest_name)
    idx = random.randint(0, len(options)-1)
    st.success(f'Kain sa: {options[idx]}')
