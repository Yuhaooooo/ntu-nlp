from nltk.sentiment.vader import SentimentIntensityAnalyzer


# import a LEXICON
def get_sentiment(text):
    sid = SentimentIntensityAnalyzer()

    sentiment_score = sid.polarity_scores(text)

    return sentiment_score
