import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')
import pandas as pd

# import a LEXICON
def get_sentiment(text):
    sid = SentimentIntensityAnalyzer()

    sid = SentimentIntensityAnalyzer()

    sentiment_score = sid.polarity_scores(text)

    return sentiment_score

text = input("Enter a string : ") 

print(get_sentiment(text))