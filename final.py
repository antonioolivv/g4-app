import streamlit as st
import pandas as pd
import numpy as np
import sqlite3 as sq


st.title("My First Web App")
st.image('3AB54F9E-5771-4627-94FD-FAEA53432F73.webp')


conn = sq.connect('ecsel_database.db')

acronym=st.text_input("Select a country")

country_acronyms = {'BE':'Belgium' , 'Bulgaria': 'BG', 'Czechia': 'CZ', 'Denmark': 'DK', 'Germany':
'DE', 'Estonia': 'EE', 'Ireland': 'IE','Greece': 'EL', 'Spain': 'ES', 'France': 'FR', 'Croatia':
'HR', 'Italy': 'IT', 'Cyprus': 'CY', 'Latvia': 'LV', 'Lithuania': 'LT','Luxembourg': 'LU',
'Hungary': 'HU', 'Malta': 'MT', 'Netherlands': 'NL', 'Austria': 'AT', 'Poland': 'PL', 'Portugal':
'PT','Romania': 'RO', 'Slovenia': 'SI', 'Slovakia': 'SK', 'Finland': 'FI', 'Sweden': 'SE'}

country=country_acronyms[acronym]

#frist table
df_grants_year=pd.read_sql('''
SELECT SUM(o.ecContribution) AS Grants,year AS Years
FROM participants o JOIN projects p ON o.projectID==p.projectID
WHERE o.country = "{}"
GROUP BY p.year
'''.format(country),conn,index_col="Years")
conn.close()
st.title(f"Participants in {country}")
st.bar_chart(data=df_grants_year, width=0, height=0, use_container_width=True)


#Second table

conn = sq.connect('ecsel_database.db')
df_grants_year=pd.read_sql('''
SELECT COUNT(o.projectID) AS ProjectCount,SUM(o.ecContribution)AS Contribution,year AS Years,name AS OrganizationName,shortName AS ShortName,organizationURL AS URL,activityType as ActivityType
FROM participants o JOIN projects p ON o.projectID==p.projectID
WHERE o.country = "{}" 
GROUP BY o.projectAcronym
ORDER BY Contribution DESC
'''.format(country),conn,index_col="Years")

conn.close()
st.table(df_grants_year)


