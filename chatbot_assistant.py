import streamlit as st
import re
from utils.stock_data import get_stock_price, get_moving_average
import yfinance as yf
import ollama


NEWS_API_KEY = "YOUR_NEWS_API_KEY"  # Replace with your actual NewsAPI key

def get_stock_trend_data(ticker, period="6mo"):
    """Fetch historical stock data and extract key statistics."""
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)

        if hist.empty:
            return None  # No data available

        min_price = hist['Close'].min()
        max_price = hist['Close'].max()
        latest_price = hist['Close'].iloc[-1]
        avg_volume = hist['Volume'].mean()

        return {
            "latest_price": latest_price,
            "min_price": min_price,
            "max_price": max_price,
            "avg_volume": avg_volume
        }
    except Exception as e:
        st.error(f"⚠️ Error fetching stock data: {e}")
        return None

def get_stock_news(ticker):
    """Fetch the latest news related to the stock from NewsAPI."""
    url = f"https://newsapi.org/v2/everything?q={ticker}&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    
    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200 or "articles" not in data:
            return "⚠️ Error fetching news data."

        articles = data["articles"][:3]  # Get the top 3 recent news articles

        news_summary = []
        for article in articles:
            news_summary.append(f"- {article['title']}: {article['description']}")

        return "\n".join(news_summary) if news_summary else "No relevant news found."
    
    except Exception as e:
        return f"⚠️ Error fetching news: {e}"

def generate_stock_summary(ticker, stock_data, news_data):
    """Use Ollama to generate an AI-powered stock trend summary with real news data."""
    if not stock_data:
        return "⚠️ No stock data available for this ticker."

    prompt = f"""
    Analyze the last 6 months of stock price data for {ticker}. 
    - Latest price: ${stock_data['latest_price']:.2f}
    - Minimum price: ${stock_data['min_price']:.2f}
    - Maximum price: ${stock_data['max_price']:.2f}
    - Average trading volume: {stock_data['avg_volume']:.2f} 

    Recent News Headlines:
    {news_data}

    Based on this data and news, provide a summary of the key trends, major price movements, and potential reasons for fluctuations.
    """

    try:
        response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
        return response["message"]["content"]
    except Exception as e:
        return f"⚠️ Error generating analysis: {e}"

def extract_ticker_from_input(user_input):
    """Extracts a valid stock ticker from user input using regex."""
    match = re.search(r'\b[A-Z]{1,5}\b', user_input)
    return match.group(0) if match else None

def run_chatbot_assistant():
    st.subheader("🤖 AI-4 Finance Chatbot")
    user_input = st.text_input("Ask about stock prices, trends, or moving averages!")

    if st.button("Analyze"):
        if user_input:
            response = None
            fig = None  # Initialize plot variable

            # Extract ticker symbol
            ticker = extract_ticker_from_input(user_input)
            if not ticker:
                st.error("⚠️ Could not detect a stock ticker in your query.")
                return

            # **Stock Price Request**
            if "price" in user_input.lower():
                response, fig = get_stock_price(ticker)

            # **Moving Average Request**
            ma_match = re.search(r'(\d+)-day moving average', user_input, re.IGNORECASE)
            if ma_match:
                ma_period = int(ma_match.group(1))  # Extract Moving Average Period
                response, fig = get_moving_average(ticker, ma_period)

            # **Stock Trend Analysis (Ollama + Real News)**
            if "trend" in user_input.lower() or "performed" in user_input.lower():
                stock_data = get_stock_trend_data(ticker)
                news_data = get_stock_news(ticker)  # Fetch real news
                response = generate_stock_summary(ticker, stock_data, news_data)

            # Display **Text Response**
            if response:
                st.write(response)

            # Display **Chart if Available**
            if fig:
                st.plotly_chart(fig, use_container_width=True)