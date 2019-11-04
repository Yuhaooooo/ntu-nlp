import os
import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("data.csv")
df = df.drop(["review_id", "user_id", "business_id", "useful", "funny", "cool", "date"], axis=1)

train, test = train_test_split(df, test_size=0.2)
train.to_csv(os.path.join("train.csv"))
test.to_csv(os.path.join("val.csv"))
