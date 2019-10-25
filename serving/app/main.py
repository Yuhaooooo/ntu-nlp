from fastapi import FastAPI

from serving.app.engine import ReviewService

app = FastAPI(title="Review Classification", openapi_url="/openapi.json")

review_model = ReviewService()


@app.post("/predict")
async def process(sentence: str):
    response = review_model.single_predict(sentence)

    return {'review': response}
