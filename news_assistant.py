import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import ollama
from utils.sentiment_analysis import analyze_sentiment

NEWS_API_KEY = "ae09145d1cae4d0cbe0979918b809abf"

def ask_ollama(prompt):
    """Use Ollama to generate AI-powered financial insights."""
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]

def get_financial_news(ticker):
    url = f"https://newsapi.org/v2/everything?q={ticker}&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200 or "articles" not in data:
            return f"Error fetching news: {data.get('message', 'Unknown error')}"

        articles = data["articles"][:5]
        news_list = [
            {
                "title": article['title'],
                "description": article['description'] or "No description available.",
                "url": article['url']
            }
            for article in articles if article.get('title') and article.get('description')
        ]

        return news_list if news_list else "No recent news found."

    except Exception as e:
        return f"Error fetching news: {str(e)}"

def run_news_assistant():
    st.subheader("📰 AI-4 Financial News")
    news_query = st.text_input("Enter a stock ticker (e.g., AAPL) or company name:")

    if st.button("Get News"):
        if news_query:
            news_articles = get_financial_news(news_query)

            if isinstance(news_articles, str):
                st.error(news_articles)
                return

            if news_articles:
                st.write(f"📊 **Top 5 News Articles for {news_query.upper()}**")
                news_data = []

                for article in news_articles:
                    title = article["title"]
                    description = article["description"]
                    url = article["url"]
                    sentiment = analyze_sentiment(title + " " + description)

                    # Generate AI-powered insights with Ollama
                    summary_prompt = f"Summarize this financial news article in simple terms: {title} - {description}"
                    summary = ask_ollama(summary_prompt)

                    sentiment_prompt = f"The following news article has a {sentiment} sentiment. Explain how this sentiment could impact the stock price and investor behavior: {title} - {description}"
                    sentiment_impact = ask_ollama(sentiment_prompt)

                    insights_prompt = f"Given this news article and its sentiment, provide investment insights on whether an investor should buy, hold, or sell this stock: {title} - {description}"
                    investment_insight = ask_ollama(insights_prompt)

                    news_data.append({
                        "Title": title,
                        "Sentiment": sentiment,
                        "Summary": summary,
                        "Impact on Stock": sentiment_impact,
                        "Investment Insight": investment_insight,
                        "URL": url
                    })

                news_df = pd.DataFrame(news_data)
                st.dataframe(news_df)

                st.write(f"🤖 **AI Summary:** {ask_ollama(f'What does this news mean for investors in {news_query}?')}")
