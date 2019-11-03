from fastapi import FastAPI
from typing import List

from engine import SentimentService

app = FastAPI(title="Review Classification", openapi_url="/openapi.json")

sentiment_model = SentimentService('weight/sentiment-model.pt', 'weight/fields.pkl', 'cuda')


@app.post('/predict')
async def predict(sentence: str):
    response = sentiment_model.single_predict(sentence)

    return {'stars': response}


@app.post('/batch-predict')
async def batch_predict(sentences: List[str]):
    response = sentiment_model.batch_predict(sentences, 64)
    return {'stars': response}
