import sqlite3

from config import settings
from data import SQLRepository
from fastapi import FastAPI
from model import GarchModel
from pydantic import BaseModel

# uvicorn main:app --reload --workers 1 --host localhost --port 8008
class FitIn(BaseModel):
    ticker: str
    use_new_data: bool
    n_observations: int
    p: int
    q: int

class FitOut(FitIn):
    success: bool
    message: str

class PredictIn(BaseModel):
    ticker: str
    n_days: int

class PredictOut(PredictIn):
    success: bool
    forecast: dict
    message: str

def build_model(ticker, use_new_data):
    # Create DB connection
    connection =  sqlite3.connect(settings.db_name, check_same_thread=False)
    # Create 'SQLRepository
    repo = SQLRepository(connection=connection)
    # Create model
    model = GarchModel(ticker=ticker, use_new_data=use_new_data, repo=repo)
    return model

app = FastAPI()

@app.get("/hello", status_code=200)
def hello():
    return {"message": "Hello World!"}

@app.post("/fit", status_code=200, response_model=FitOut)
def fit_model(request: FitIn):
    # Create dictionary from 'payload'
    response = request.model_dump()

    try:
        # Build model
        model = build_model(ticker=request.ticker, use_new_data=request.use_new_data)

        # Wrangle data
        model.wrangle_data(n_observations=request.n_observations)

        # Fit model
        model.fit(p=request.p, q=request.q)

        # Save model
        filename = model.dump()

        response["success"] = True

        response["message"] = f"Trained and saved '{filename}'."
    
    except Exception as e:
        response["success"] = False
        response["message"] = str(e)

    return response


# `"/hello" path with 200 status code
@app.get("/hello", status_code=200)
def hello():
    """Return dictionary with greeting message."""
    return {"message": "Hello World!"}


@app.post("/predict", status_code=200, response_model=PredictOut)
def get_prediction(request: PredictIn):

    # Create `response` dictionary from `request`
    response = request.dict()

    # Create try block to handle exceptions
    try:
        # Build model with `build_model` function
        model = build_model(ticker=request.ticker, use_new_data=False)

        # Load stored model
        model.load()

        # Generate prediction
        prediction = model.predict_volatility(horizon=request.n_days)

        # Add `"success"` key to `response`
        response["success"] = True

        # Add `"forecast"` key to `response`
        response["forecast"] = prediction

        # Add `"message"` key to `response`
        response["message"] = ""

    # Create except block
    except Exception as e:
        # Add `"success"` key to `response`
        response["success"] = False

        # Add `"forecast"` key to `response`
        response["forecast"] = {}

        #  Add `"message"` key to `response`
        response["message"] = str(e)

    # Return response
    return response