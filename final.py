#the required libraries where imported
import streamlit as st
import pandas as pd
import numpy as np
import sqlite3 as sq


st.image('image.webp')
st.title("Partner search tool")

#FR-2.13 - Connection to the database
conn = sq.connect('ecsel_database.db')
#FR-2.14 - Dropdown selector with the different countries
selection = st.selectbox("Select country",['Belgium' , 'Bulgaria', 'Czechia', 'Denmark', 'Germany', 'Estonia', 'Ireland','Greece', 'Spain', 'France', 'Croatia', 'Italy', 'Cyprus', 'Latvia', 'Lithuania','Luxembourg',
'Hungary', 'Malta', 'Netherlands', 'Austria', 'Poland', 'Portugal','Romania', 'Slovenia', 'Slovakia', 'Finland', 'Sweden'])
# List of country names and country acronyms for the selection
country_acronyms = {'Belgium':'BE' , 'Bulgaria': 'BG', 'Czechia': 'CZ', 'Denmark': 'DK', 'Germany':
'DE', 'Estonia': 'EE', 'Ireland': 'IE','Greece': 'EL', 'Spain': 'ES', 'France': 'FR', 'Croatia':
'HR', 'Italy': 'IT', 'Cyprus': 'CY', 'Latvia': 'LV', 'Lithuania': 'LT','Luxembourg': 'LU',
'Hungary': 'HU', 'Malta': 'MT', 'Netherlands': 'NL', 'Austria': 'AT', 'Poland': 'PL', 'Portugal':
'PT','Romania': 'RO', 'Slovenia': 'SI', 'Slovakia': 'SK', 'Finland': 'FI', 'Sweden': 'SE'}
# FR-2.15 - The system gets the country acronym from the given country_acronyms dictionary
# The acronym selected is match with the country name which is stored on "country"
country = country_acronyms[selection]

# ---------------------------------------
# Yearly EC contributions bar chart
# QUESTION - should we open and close the connection with the database each time?
# The system connected to the database through a SQL querie generates a new dataframe of grants per year for the selected country
df_grants_year = pd.read_sql('''
SELECT SUM(o.ecContribution) AS Grants,year AS Years
FROM participants o JOIN projects p ON o.projectID==p.projectID
WHERE o.country = "{}"
GROUP BY p.year
'''.format(country),conn,index_col="Years")
#The index_col is set to years to have the right x-axis
# The connection is closed with the database
conn.close()
st.title(f"Yearly EC contribution in {selection}")
# A bar chart is generated from the selection
st.bar_chart(data=df_grants_year, width=0, height=0, use_container_width=True)

# ---------------------------------------
#Participants table
st.title(f"Participants in {selection}")
# Connection to the database
conn = sq.connect('ecsel_database.db')
#FR-2.16 - The system connected to the database through a SQL querie generates a new dataframe of participants of the selected country
#FR-2.17 - The genereated dataset is displayed in descending order by received grants, contribution
df_participants=pd.read_sql('''
SELECT COUNT(o.projectID) AS ProjectCount,SUM(o.ecContribution)AS Contribution,year AS Years,name AS OrganizationName,shortName AS ShortName,organizationURL AS URL,activityType as ActivityType
FROM participants o JOIN projects p ON o.projectID==p.projectID
WHERE o.country = "{}" 
GROUP BY o.projectAcronym
ORDER BY Contribution DESC
'''.format(country),conn,index_col="Years")
# The connection is closed
conn.close()
st.dataframe(df_participants)
#FR2.21 - Definition of a function to make more accesible the downlooad function in Streamlit
def convert_df(data): 
 return df_participants.to_csv().encode('utf-8') 
st.download_button(label=f"Download {selection} Participants",data=convert_df(df_participants), file_name=f'participants{selection}.csv', mime='text/csv',)

# ---------------------------------------
#Project coordinators table
st.title(f"Project coordinators in {selection}")
conn = sq.connect('ecsel_database.db')

df_coordinators=pd.read_sql('''
SELECT COUNT(o.projectID) AS ProjectCount,SUM(o.ecContribution)AS Contribution,year AS Years,name AS OrganizationName,shortName AS ShortName,organizationURL AS URL,activityType as ActivityType
FROM participants o JOIN projects p ON o.projectID==p.projectID
WHERE o.country = "{}" AND o.Role="coordinator"
GROUP BY o.projectAcronym
ORDER BY ShortName ASC
'''.format(country),conn,index_col="Years")

conn.close()
st.dataframe(df_coordinators)
#FR2.21 - Another button to make easy the process of downloading the data as CSV file
st.download_button(label=f"Download {selection} Coordinators",data=convert_df(df_coordinators), file_name=f'coordinators{selection}.csv', mime='text/csv',)

