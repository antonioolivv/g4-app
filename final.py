import streamlit as st
import pandas as pd
import numpy as np
import sqlite3 as sq


st.title("My First Web App")
st.image('./3AB54F9E-5771-4627-94FD-FAEA53432F73.webp')


conn = sq.connect('./ecsel_database.db')

country=input("Select a country")

#frist table
df_grants_year=pd.read_sql('''
SELECT SUM(o.ecContribution) AS Grants,year AS Years
FROM participants o JOIN projects p ON o.projectID==p.projectID
WHERE o.country = "{}"
GROUP BY p.year
'''.format(country),conn)
conn.close()
df_grants_year.head()


chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['a', 'b', 'c'])
st.write(chart_data)
option = st.selectbox('Options', ['a', 'b', 'c'])
st.bar_chart(chart_data)
