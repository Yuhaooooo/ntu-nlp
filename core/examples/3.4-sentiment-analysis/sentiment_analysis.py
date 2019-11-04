from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
from pathlib import Path
from tqdm import tqdm


# import a LEXICON
def get_sentiment(text):
    sid = SentimentIntensityAnalyzer()
    return sid.polarity_scores(text)


CORE_DIR = Path(__file__).absolute().parent / '../../'
df = pd.read_csv(CORE_DIR / 'data/data.csv')

right = 0
total = len(df)
scores = []
for index, row in tqdm(df.iterrows()):
    sentiment_score = get_sentiment(row["text"])
    scores.append(str(sentiment_score))
    if sentiment_score['compound'] > 0.05:
        if row['stars'] > 2.0:
            right += 1
    elif sentiment_score['compound'] > -0.05:
        if row['stars'] == 2.0:
            right += 1
    elif sentiment_score['compound'] < -0.05:
        if row['stars'] < 2.0:
            right += 1

print('Accuracy {}'.format(right / total))

with open(CORE_DIR / 'output/result.txt', 'w') as f:
    f.writelines(scores)
print('Finish prediction, result is saved in core/output/result.txt')
