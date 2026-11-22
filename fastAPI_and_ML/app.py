from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Literal, Annotated
import pickle
import pandas as pd

#import ml model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

app = FastAPI()

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]

# pydantic model to validate incomming data
class UserInput(BaseModel):
    age: Annotated[int, Field(..., gt=0, le=120, description="Age of the user")]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the user")]
    height: Annotated[float, Field(..., gt=0, le=2.5, description="Height of the user")]
    income_lpa: Annotated[int, Field(..., gt=0, description="Income of the user")]
    smoker: Annotated[bool, Field(..., description="Smoker status of the user")]
    city: Annotated[str, Field(..., description="City of the user")]
    occupation: Annotated[Literal["retired", "freelancer", "student", "government_job", "business_owner", "unemployed", "private_job", ], Field(..., description="Occupation of the user")]


    @computed_field
    @property
    def bmi(self) -> float:
        bmi = self.weight/(self.height **2)
        return bmi

    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else: 
            return "low"

    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "adult"
        elif self.age < 45:
            return "middle_aged"
        else:
            return "senior"

    @computed_field
    @property
    def city_tier(self) -> str:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3

@app.post("/predict")
def predict_premium(user_input: UserInput):

    input_df = pd.DataFrame([{
            "bmi": user_input.bmi,
            "age_group": user_input.age_group,
            "city_tier": user_input.city_tier,
            "smoker": user_input.smoker,
            "lifestyle_risk": user_input.lifestyle_risk,
            "income_lpa": user_input.income_lpa,
            "occupation": user_input.occupation,
        }])

    prediction = model.predict(input_df)[0]
    return JSONResponse(status_code=200, content={"predicted category": prediction})