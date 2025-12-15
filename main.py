from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np

app = FastAPI()

# 1. Update the Model: Now we expect Data AND a License Key
class SheetData(BaseModel):
    data: list[list] 
    license_key: str  # <--- NEW LINE

@app.get("/")
def read_root():
    return {"status": "Online", "message": "Send POST requests to /clean"}

@app.post("/clean")
def clean_spreadsheet(payload: SheetData):
    
    # 2. THE SECURITY CHECK (The Guard)
    # This is your "Password". Only users who send this string can use the app.
    # You can change "PRO-USER-2024" to whatever you want.
    MY_SECRET_PASSWORD = "PRO-USER-2024"

    if payload.license_key != MY_SECRET_PASSWORD:
        # If the key is wrong, stop immediately.
        return {"error": "ACCESS DENIED: Invalid License Key. Please purchase a key."}

    # If the key is correct, the code continues...
    try:
        # A. Convert to DataFrame
        headers = payload.data[0]
        rows = payload.data[1:]
        
        df = pd.DataFrame(rows, columns=headers)

        # --- CLEANING LOGIC ---
        df.drop_duplicates(inplace=True)
        df = df.fillna("Unknown") 
        # ----------------------

        # B. Convert back to list
        new_headers = [df.columns.tolist()]
        new_values = df.values.tolist()
        clean_output = new_headers + new_values

        return {"cleaned_data": clean_output}

    except Exception as e:
        return {"error": str(e)}
