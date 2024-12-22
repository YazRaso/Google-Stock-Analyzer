# Import packages
import pandas as pd
import numpy as np
import math

from scipy.ndimage import maximum

# Use Kaggle dataset
stock_data = pd.read_csv('./GOOG.csv')

# Initialize dataframe
df = pd.DataFrame(stock_data)
df = df.drop_duplicates()

# Calculate Daily returns
df['Daily Returns'] = ((pd.to_numeric(df['Adj Close'].iloc[1:]) - pd.to_numeric(df['Open'].iloc[1:]))
                        / pd.to_numeric(df['Open'].iloc[1:]))
df['Daily Returns %'] = df['Daily Returns'] * 100

# Calculate Annual Return (2024-01-02) - (2024-12-03)
annual_return = (100 * (pd.to_numeric(df["Adj Close"].iloc[-1]) - pd.to_numeric(df["Adj Close"].iloc[1])) /
                 pd.to_numeric(df["Adj Close"].iloc[1]))

# Calculate volatility, where volatility = std_dev * sqrt(trading period)
# 252 represents the 252 trading days within a year
n_time_periods = len(df)
volatility = df["Daily Returns"].std() * math.sqrt(n_time_periods)

# Calculate Maximum Draw-down
peak_index = df["High"][1:].idxmax()
peak = pd.to_numeric(df["High"][peak_index])
trough = pd.to_numeric(df["Low"][peak_index:].min())
maximum_draw_down = (peak - trough) / peak
