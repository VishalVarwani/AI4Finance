import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

def get_stock_price(ticker, period="6mo"):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)  # Fetch last 6 months of stock data
        latest_price = hist['Close'].iloc[-1]

        # Create an interactive Plotly chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hist.index, 
            y=hist['Close'], 
            mode='lines', 
            name='Stock Price', 
            line=dict(color='blue')
        ))

        # Add title & labels
        fig.update_layout(
            title=f"{ticker.upper()} Stock Price Over {period}",
            xaxis_title="Date",
            yaxis_title="Stock Price ($)",
            template="plotly_dark"
        )

        return f"The current price of {ticker.upper()} is ${latest_price:.2f}", fig

    except Exception as e:
        return f"Error fetching stock price: {str(e)}", None
    
def get_moving_average(ticker, window):
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period="6mo")
        df[f"SMA_{window}"] = df["Close"].rolling(window=window).mean()

        # Create a Moving Average Chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df["Close"], mode='lines', name='Closing Price'))
        fig.add_trace(go.Scatter(x=df.index, y=df[f"SMA_{window}"], mode='lines', name=f"{window}-Day SMA", line=dict(dash='dash')))

        fig.update_layout(
            title=f"{ticker.upper()} {window}-Day Moving Average",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            xaxis_rangeslider_visible=True
        )

        return f"Displaying {window}-Day Moving Average for {ticker.upper()}", fig

    except Exception as e:
        return f"Error generating moving average plot: {str(e)}", None
