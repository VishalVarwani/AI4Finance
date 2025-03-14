import streamlit as st
import yfinance as yf
import pandas as pd
import re

# Initialize session state for portfolio
if "portfolio" not in st.session_state:
    st.session_state.portfolio = {}

def run_portfolio_assistant():
    st.subheader("📊 AI-4 Portfolio Analysis")
    user_input = st.text_input("Enter portfolio details (e.g., '10 shares of AAPL at $150').")

    if st.button("Update Portfolio"):
        new_portfolio = re.findall(r'(\d+) shares? of (\w+) at \$?([\d.]+)', user_input)
        if new_portfolio:
            for shares, ticker, price in new_portfolio:
                ticker = ticker.upper()
                st.session_state.portfolio[ticker] = {
                    "shares": int(shares),
                    "buy_price": float(price)
                }
            st.success("✅ Portfolio updated!")

    if st.button("Show Portfolio Analysis"):
        if st.session_state.portfolio:
            tickers = list(st.session_state.portfolio.keys())
            stock_prices = {ticker: yf.Ticker(ticker).history(period="1d")["Close"].iloc[-1] for ticker in tickers}

            portfolio_data = []
            total_investment, total_value = 0, 0

            for ticker, data in st.session_state.portfolio.items():
                shares = data["shares"]
                buy_price = data["buy_price"]
                current_price = stock_prices.get(ticker, 0)
                investment = shares * buy_price
                current_value = shares * current_price
                profit_loss = current_value - investment

                portfolio_data.append([ticker, shares, buy_price, current_price, profit_loss])
                total_investment += investment
                total_value += current_value

            df = pd.DataFrame(portfolio_data, columns=["Ticker", "Shares", "Buy Price", "Current Price", "Profit/Loss"])
            st.dataframe(df)

            st.write(f"💰 **Total Investment:** ${total_investment:.2f}")
            st.write(f"📈 **Current Portfolio Value:** ${total_value:.2f}")
