# Import packages
import pandas as pd
import numpy as np
import math

# Use Kaggle dataset
stock_data = pd.read_csv('./GOOG.csv')

# Initialize dataframe
df = pd.DataFrame(stock_data)

# TODO: Clean data to represent 252 trading days in a year
df.dropna()
df.drop_duplicates()

# Calculate Daily returns
df['Daily Returns'] = ((pd.to_numeric(df['Adj Close'].iloc[1:]) - pd.to_numeric(df['Open'].iloc[1:]))
                        / pd.to_numeric(df['Open'].iloc[1:]))
df['Daily Returns %'] = df['Daily Returns'] * 100

# Calculate Annual Return (2024-01-02) - (2024-12-03)
annual_return = (100 * (pd.to_numeric(df["Adj Close"].iloc[-1]) - pd.to_numeric(df["Adj Close"].iloc[1])) /
                 pd.to_numeric(df["Adj Close"].iloc[1]))

# Calculate volatility, where volatility = std_dev * sqrt(trading period)
volatility = df["Daily Returns"].std() * math.sqrt(252)
