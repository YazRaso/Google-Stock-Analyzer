# Import packages
import pandas as pd
import numpy as np
import streamlit as st

# Use Kaggle dataset
stock_data = pd.read_csv("./GOOG.csv")

# Initialize dataframe
df = pd.DataFrame(stock_data)

# Clean data
df.dropna()
df.drop_duplicates()

df['price change %'] = ((pd.to_numeric(df['Adj Close'].iloc[1:]) - pd.to_numeric(df['Open'].iloc[1:]))
                        / pd.to_numeric(df['Open'].iloc[1:])) * 100

# Creating UI using streamlit
st.write("Hello World!")