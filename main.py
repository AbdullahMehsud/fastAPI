from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel, Field, computed_field
from fastapi.responses import JSONResponse
from typing import Annotated, Optional, Literal
import json
app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="ID of the patient", example="P001")]
    name: Annotated[str, Field(..., description="The name of the patient", example="John Doe")]
    city: Annotated[str, Field(..., description="The city of the patient", example="New York")]
    age: Annotated[int, Field(..., description="The age of the patient", example=30)]
    gender: Annotated[str, Field(..., description="The gender of the patient", example="Male")]
    height: Annotated[float, Field(..., description="The height of the patient", example=175.5)]
    weight: Annotated[float, Field(..., description="The weight of the patient", example=70.0)]


    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height **2),2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal weight"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"

class UpdatePatient(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal["Male", "Female"]], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
    return data

def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f)
@app.get("/")
def hello():
    return {"message": "Patients management system API"}

@app.get("/about")
def about():
    return {"message": "All about the Patients management system API"}



@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def get_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve", example="P001")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description="Sort by height, weight, or bmi"), order: str = Query("asc", description="Sort order: asc or desc")):

    valid_fields = ["height", "weight", "bmi"]

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field. Must be one of {valid_fields}")

    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order. Must be 'asc' or 'desc'")

    data = load_data()

    sort_order = True if order == "desc" else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data

@app.post("/create")
def create_patient(patient: Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists")

    data[patient.id] = patient.model_dump(exclude=["id"])

    save_data(data)
    return JSONResponse(status_code=201, content={"message": "Patient created successfully"})


@app.put("/edit/{patient_id}")
def edit_patient(patient_id: str, patient_update: UpdatePatient):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    existing_patient_info['id'] = patient_id
    patient_pydantic_obj = Patient(**existing_patient_info)

    existing_patient_info = patient_pydantic_obj.model_dump(exclude=["id"])

    data[patient_id] = existing_patient_info

    save_data(data)

    return JSONResponse(status_code=200, content={"message": "Patient updated successfully"})

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    del data[patient_id]
    save_data(data)
    return JSONResponse(status_code=200, content={"message": "Patient deleted successfully"})
