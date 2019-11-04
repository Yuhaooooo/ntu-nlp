import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')
import pandas as pd

#import a LEXICON


# import a LEXICON
def get_sentiment(text):
    sid = SentimentIntensityAnalyzer()

	sid = SentimentIntensityAnalyzer()

	sentiment_score = sid.polarity_scores(text)

	return sentiment_score

df = pd.read_csv("data.csv")

    sentiment_score = sid.polarity_scores(text)
right = 0
total = len(df)
for index, row in df.iterrows():
    sentiment_score = get_sentiment(row["text"])
    print(sentiment_score)
    if sentiment_score['compound'] >  0.05:
    	if row['stars'] > 2.0:
    		right += 1
    elif sentiment_score['compound'] > -0.05:
    	if row['stars'] == 2.0:
    		right += 1
    elif sentiment_score['compound'] < -0.05:
    	if row['stars'] < 2.0:
    		right += 1

    return sentiment_score
print(right / total)