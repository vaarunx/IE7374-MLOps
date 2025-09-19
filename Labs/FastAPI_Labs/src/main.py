from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from predict import predict_data
import uvicorn

app = FastAPI()

class DiabetesData(BaseModel):
    age: float
    sex: float
    bmi: float
    bp: float  # average blood pressure
    total_serum_cholesterol: float  # s1
    ldl_cholesterol: float  # s2
    hdl_cholesterol: float  # s3
    cholesterol_hdl_ratio: float  # s4
    log_serum_triglycerides: float  # s5
    blood_sugar_level: float  # s6

class DiabetesResponse(BaseModel):
    response: float

@app.get("/", status_code=status.HTTP_200_OK)
async def health_ping():
    return {"status": "healthy"}

@app.post("/predict", response_model=DiabetesResponse)
async def predict_diabetes(diabetes_features: DiabetesData):
    try:
        features = [[
            diabetes_features.age,
            diabetes_features.sex,
            diabetes_features.bmi,
            diabetes_features.bp,
            diabetes_features.total_serum_cholesterol,
            diabetes_features.ldl_cholesterol,
            diabetes_features.hdl_cholesterol,
            diabetes_features.cholesterol_hdl_ratio,
            diabetes_features.log_serum_triglycerides,
            diabetes_features.blood_sugar_level
        ]]

        prediction = predict_data(features)
        return DiabetesResponse(response=float(prediction[0]))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)