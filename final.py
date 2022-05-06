import streamlit as st
import pandas as pd
import numpy as np
import sqlite3 as sq


st.title("My First Web App")
st.image('3AB54F9E-5771-4627-94FD-FAEA53432F73.webp')


conn = sq.connect('ecsel_database.db')

selection=st.selectbox("Select country",['Belgium' , 'Bulgaria', 'Czechia', 'Denmark', 'Germany', 'Estonia', 'Ireland','Greece', 'Spain', 'France', 'Croatia', 'Italy', 'Cyprus', 'Latvia', 'Lithuania','Luxembourg',
'Hungary', 'Malta', 'Netherlands', 'Austria', 'Poland', 'Portugal','Romania', 'Slovenia', 'Slovakia', 'Finland', 'Sweden'])

country_acronyms = {'Belgium':'BE' , 'Bulgaria': 'BG', 'Czechia': 'CZ', 'Denmark': 'DK', 'Germany':
'DE', 'Estonia': 'EE', 'Ireland': 'IE','Greece': 'EL', 'Spain': 'ES', 'France': 'FR', 'Croatia':
'HR', 'Italy': 'IT', 'Cyprus': 'CY', 'Latvia': 'LV', 'Lithuania': 'LT','Luxembourg': 'LU',
'Hungary': 'HU', 'Malta': 'MT', 'Netherlands': 'NL', 'Austria': 'AT', 'Poland': 'PL', 'Portugal':
'PT','Romania': 'RO', 'Slovenia': 'SI', 'Slovakia': 'SK', 'Finland': 'FI', 'Sweden': 'SE'}

country=country_acronyms[selection]

#frist table
df_grants_year=pd.read_sql('''
SELECT SUM(o.ecContribution) AS Grants,year AS Years
FROM participants o JOIN projects p ON o.projectID==p.projectID
WHERE o.country = "{}"
GROUP BY p.year
'''.format(country),conn,index_col="Years")
conn.close()
st.title(f"Yearly EC contribution in {selection}")
st.bar_chart(data=df_grants_year, width=0, height=0, use_container_width=True)


#Second table

st.title(f"Participants in {selection}")

conn = sq.connect('ecsel_database.db')
df_grants_year=pd.read_sql('''
SELECT COUNT(o.projectID) AS ProjectCount,SUM(o.ecContribution)AS Contribution,year AS Years,name AS OrganizationName,shortName AS ShortName,organizationURL AS URL,activityType as ActivityType
FROM participants o JOIN projects p ON o.projectID==p.projectID
WHERE o.country = "{}" 
GROUP BY o.projectAcronym
ORDER BY Contribution DESC
'''.format(country),conn,index_col="Years")

conn.close()
st.dataframe(df_grants_year)

#Third table

st.title(f"Project coordinators in {selection}")
conn = sq.connect('ecsel_database.db')

df_grants_year=pd.read_sql('''
SELECT COUNT(o.projectID) AS ProjectCount,SUM(o.ecContribution)AS Contribution,year AS Years,name AS OrganizationName,shortName AS ShortName,organizationURL AS URL,activityType as ActivityType
FROM participants o JOIN projects p ON o.projectID==p.projectID
WHERE o.country = "{}" AND o.Role="coordinator"
GROUP BY o.projectAcronym
ORDER BY ShortName ASC
'''.format(country),conn,index_col="Years")

conn.close()
df_grants_year.head()

