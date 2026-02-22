from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import pandas as pd
import numpy as np

app = FastAPI()

# Allow React to talk to FastAPI [cite: 196]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the saved artifacts
model = pickle.load(open("iphone_model.pkl", "rb"))
model_cols = pickle.load(open("model_columns.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

class PredictionRequest(BaseModel):
    model_name: str
    ram: float
    memory: float
    is_used: bool

@app.post("/predict")
def predict(data: PredictionRequest):
    # 1. Create empty input row
    input_df = pd.DataFrame(0, index=[0], columns=model_cols)
    
    # 2. Scale RAM/Memory using saved scaler
    scaled_values = scaler.transform([[data.ram, data.memory]])
    input_df['RAM_GB'] = scaled_values[0][0]
    input_df['Memory_GB'] = scaled_values[0][1]
    
    # 3. Set Condition and Model
    input_df['Condition_Enc'] = 1 if data.is_used else 0
    model_col = f"Model_{data.model_name}"
    if model_col in input_df.columns:
        input_df[model_col] = 1
        
    # 4. Predict [cite: 195]
    price = model.predict(input_df)[0]
    return {"price": round(float(price), 2)}