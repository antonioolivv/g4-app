import streamlit as st
import pandas as pd
import numpy as np
import sqlite3 as sq


st.title("My First Web App")
st.image('./3AB54F9E-5771-4627-94FD-FAEA53432F73.webp')

chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['a', 'b', 'c'])
st.write(chart_data)
option = st.selectbox('Options', ['a', 'b', 'c'])
st.bar_chart(chart_data)
