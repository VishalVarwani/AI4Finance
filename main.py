import streamlit as st
from news_assistant import run_news_assistant
from chatbot_assistant import run_chatbot_assistant
from portfolio_assistant import run_portfolio_assistant

# Streamlit UI
st.set_page_config(page_title="💰 AI Finance Agent", layout="wide")
st.title("💰 AI Finance Agent - Real-time Market Insights")

# Sidebar: Select Features
option = st.sidebar.selectbox("Choose Feature", [
    "AI-4 Financial News",
    "AI-4 Finance Chatbot",
    "AI-4 Portfolio Analysis"
])

# Run the selected assistant
if option == "AI-4 Financial News":
    run_news_assistant()
elif option == "AI-4 Finance Chatbot":
    run_chatbot_assistant()
elif option == "AI-4 Portfolio Analysis":
    run_portfolio_assistant()
