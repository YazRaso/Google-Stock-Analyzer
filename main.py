# Import modules
import pandas as pd
import numpy as np
import math
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import streamlit as st

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
df['Daily Returns'] = ((df['Adj Close'] - df['Open']) / df['Open'])
df['Daily Returns %'] = df["Daily Returns"] * 100

# Calculate Annual Return (2024-01-02) - (2024-12-03)
annual_return = 100 * (df["Adj Close"].iloc[-1] - df["Adj Close"].iloc[0]) / df["Adj Close"].iloc[0]

# Calculate volatility, where volatility = std_dev * sqrt(trading period)
annual_volatility = round((df["Daily Returns"].std() * math.sqrt(len(df))), 3)

peak_index = df["High"].idxmax()
peak = df["High"].iloc[peak_index]
trough_index = df["Low"].iloc[peak_index:].idxmin()
trough = df["Low"].iloc[trough_index]
max_draw_down = round(((peak - trough) / peak), 3)

trough_price = round(df['Close'].iloc[trough_index], 1)
peak_price = round(df['Close'].iloc[peak_index], 1)


# Create visuals

# heat map for daily returns
columns = ['Volume', 'Daily Returns', 'Adj Close',
           'Open', 'Close']


# Calculate Correlation Matrix
def corr_matrix():
    correlation_matrix = df[columns].corr()

    # Plot Heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title("Correlation Heatmap of Google Stock (2024)")
    plt.show()
    st.pyplot(plt)

    st.title("A correlation matrix ")


# Calculate SMAs (Simple Moving Average)
df['50 SMA'] = df['Close'].rolling(50).mean()
df['200 SMA'] = df['Close'].rolling(200).mean()


def cand_stick():
    # Create the candlestick chart
    candle_stick_fig = go.Figure(data=[
        go.Candlestick(
            x=df['Price'],
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
            x=df['Price'],  # Same x-axis (Date/Time)
            y=df['50 SMA'],
            mode='lines',
            name='50-Day SMA',
            line=dict(color='orange', width=1.5)
        )
    )

    # Add the 200-day moving average to the chart
    candle_stick_fig.add_trace(
        go.Scatter(
            x=df['Price'],
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
    st.plotly_chart(candle_stick_fig, use_container_width=True)
    st.title("Outline")

    st.write(
        "The above chart represents Alphabet's stock from the start of the year up to the 3rd of December. The chart includes detailed candlestick patterns with additional 50-Day and 200-Day SMAs (Simple Moving Averages) "
        "A SMA is designed to show the mean closing prices of a stock in a specified time period, in other words, the average price within a time frame.")

    st.title("Analysis")
    st.write(
        f"A quick glance on Alphabet's stock appears to peak on {df['Price'].iloc[peak_index]} with a price of {peak_price} USD, "
        f"consequently the stocks 2024 Maximum Draw Down seems to be approximately {max_draw_down} with the trough on"
        f" {df["Price"].iloc[trough_index]} with a price of {trough_price}USD. Alphabet's stock in 2024 has a volatility of {annual_volatility} opposed to the S&P 500's volatility of 0.1795. Alphabet's annual return in 2024 was {round(annual_return, 3)}% similar to the S&P 500's return of 24%.")


def volume_traded():
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

    st.pyplot(fig)

    st.title("Outline")
    st.write("The above chart represents Alphabet's stock price by its volume traded. Price by Volume charts are used by traders in the context of technical analysis to predict resistance and support of a specific security.")
    st.title("Analysis")
