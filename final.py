import streamlit as st
import pandas as pd
import numpy as np
import sqlite3 as sq


st.title("My First Web App")
st.image('3AB54F9E-5771-4627-94FD-FAEA53432F73.webp')


conn = sq.connect('ecsel_database.db')

country=st.text_input("Select a country")

#frist table
df_grants_year=pd.read_sql('''
SELECT SUM(o.ecContribution) AS Grants,year AS Years
FROM participants o JOIN projects p ON o.projectID==p.projectID
WHERE o.country = "{}"
GROUP BY p.year
'''.format(country),conn,index_col="Years")
conn.close()
st.bar_chart(data=df_grants_year, width=0, height=0, use_container_width=True)


