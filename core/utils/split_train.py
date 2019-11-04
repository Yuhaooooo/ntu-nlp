import os
from os.path import join
import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv(join(os.getcwd(), 'core', 'data', 'data.csv'))
df = df.drop(["review_id", "user_id", "business_id", "useful", "funny", "cool", "date"], axis=1)

train, test = train_test_split(df, test_size=0.2)
try:
	train = train.drop(['Unnamed: 0'], axis=1)
except:
	pass
train.to_csv(join(os.getcwd(), 'core', 'data', 'train.csv'))
test.to_csv(join(os.getcwd(), 'core', 'data', 'val.csv'))
