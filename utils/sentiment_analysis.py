import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    score = sia.polarity_scores(text)
    return "Positive" if score["compound"] >= 0.05 else "Negative" if score["compound"] <= -0.05 else "Neutral"
