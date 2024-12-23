import streamlit as st
import main
# Creating UI using streamlit
st.write("Hello World!")
choice = st.selectbox("Quarterly performance", ("Q1", "Q2", "Q3", "Q4"))