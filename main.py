# Import modules
import pandas as pd
import numpy as np
import math
import seaborn as sns
import matplotlib.pyplot as plt

# Use Kaggle dataset
stock_data = pd.read_csv("./GOOG.csv")

# Initialize dataframe
df = pd.DataFrame(stock_data)
# Drop first row to ensure minimal confusion when period setting
df = df.iloc[1:]
df["Adj Close"] = df["Adj Close"].astype(float)
df["Volume"] = df["Volume"].astype(float)
df["Open"] = df["Open"].astype(float)
df["High"] = df["High"].astype(float)
df["Low"] = df["Low"].astype(float)
df["Close"] = df["Close"].astype(float)

df = df.dropna()
df = df.drop_duplicates()

# Calculate daily returns
df['Daily Returns'] = ((df['Adj Close']- df['Open']) / df['Open'])
df['Daily Returns %'] = df["Daily Returns"] * 100

# Calculate Annual Return (2024-01-02) - (2024-12-03)
annual_return = 100 * (df["Adj Close"].iloc[-1] - df["Adj Close"].iloc[0]) / df["Adj Close"].iloc[0]

# Calculate volatility, where volatility = std_dev * sqrt(trading period)
annual_volatility = df["Daily Returns"].std() * math.sqrt(len(df))

peak_index = df["High"].idxmax()
peak = pd.to_numeric(df["High"][peak_index])
trough = pd.to_numeric(df["Low"][peak_index:].min())
max_draw_down = (peak - trough) / peak
print(max_draw_down)

# Create visuals

# heat map for daily returns
columns = ['Volume', 'Daily Returns', 'Adj Close',
           'Open', 'Close']

# Calculate Correlation Matrix
correlation_matrix = df[columns].corr()

# Plot Heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title("Correlation Heatmap of Google Stock (2024)")
plt.show()

# Plot the Closing Price
plt.figure(figsize=(12, 6))
plt.plot(df['Price'], df['Close'], label='Closing Price', color='green')

# Add labels and title
plt.title("Google Stock Closing Prices (2024)", fontsize=16)
plt.xlabel("Date", fontsize=12)
plt.ylabel("Price (USD)", fontsize=12)
plt.legend()
plt.grid(True)
plt.show()

import plotly.graph_objects as go

# Calculate SMAs (Simple Moving Average)
df['50 SMA'] = df['Close'].rolling(50).mean()
df['200 SMA'] = df['Close'].rolling(200).mean()

# Create the candlestick chart
candle_stick_fig = go.Figure(data=[
    go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        increasing_line_color='green',
        decreasing_line_color='red'
    )
])

# Add the 50-day moving average to the chart
candle_stick_fig.add_trace(
    go.Scatter(
        x=df.index,  # Same x-axis (Date/Time)
        y=df['50 SMA'],
        mode='lines',
        name='50-Day SMA',
        line=dict(color='orange', width=1.5)
    )
)

# Add the 200-day moving average to the chart
candle_stick_fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df['200 SMA'],
        mode='lines',
        name='200-Day SMA',
        line=dict(color='green', width=1.5)
    )
)

# Update layout for the chart
candle_stick_fig.update_layout(
    title='Google Stock Candlestick Chart 2024',
    xaxis_title='Date',
    yaxis_title='Price (USD)',
    xaxis_rangeslider_visible=False,
)

# Display the chart
candle_stick_fig.show()

fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot the stock price (line chart)
ax1.plot(df['Price'], df['Close'], color='blue', label='Closing Price')
ax1.set_xlabel('Date')  # Label reflects the datetime on x-axis
ax1.set_ylabel('Price (USD)', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# Create a secondary axis for volume
ax2 = ax1.twinx()
ax2.bar(df['Price'], df['Volume'], color='green', alpha=0.3, label='Volume')
ax2.set_ylabel('Volume', color='green')
ax2.tick_params(axis='y', labelcolor='green')

# Add a title and legend
fig.suptitle('Google Stock: Price vs. Volume', fontsize=14)
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

plt.show()

