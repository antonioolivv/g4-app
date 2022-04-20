import streamlit as st
import pandas as pd
st.title("My First Web App")
st.image('./header.png')
chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['a', 'b', 'c'])
st.write(chart_data)
option = st.selectbox('Options', ['a', 'b', 'c'])
st.bar_chart(chart_data)
