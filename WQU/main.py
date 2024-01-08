import sqlite3

from config import settings
from data import SQLRepository
from fastapi import FastAPI
from model import GarchModel
from pydantic import BaseModel


class FitIn(BaseModel):
    ticker: str
    use_new_data: bool
    n_observations: int
    p: int
    q: int

class FitOut(FitIn):
    success: bool
    message: str

def build_model(ticker, use_new_data):
    connection =  sqlite3.connect(settings.db_name, check_same_thread=False)
    repo = SQLRepository(connection=connection)
    model = GarchModel(ticker=ticker, use_new_data=use_new_data, repo=repo)
    return model

app = FastAPI()

@app.get("/hello", status_code=200)
def hello():
    return {"message": "Hello World!"}

@app.post("/fit", status_code=200, response_model=FitOut)
def fit_model(request: FitIn):
    # Create dictionary from 'payload'
    response = request.dict()

    try:
        model = build_model(ticker=request.ticker, use_new_data=request.use_new_data)

        model.wrangle_data(n_observations=request.n_observations)

        model.fit(p=request.p, q=request.q)

        filename = model.dump()

        response["success"] = True

        response["message"] = f"Trained and saved '{filename}'."
    
    except Exception as e:
        response["success"] = False
        response["message"] = str(e)

    return response