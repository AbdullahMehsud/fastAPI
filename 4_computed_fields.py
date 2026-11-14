from pydantic import AnyUrl, BaseModel, EmailStr, Field, field_validator, model_validator, computed_field
from typing import List
from typing import Optional, Dict, Annotated
class Patient(BaseModel):
    name: str
    age: int
    email: EmailStr
    linkedin_url: AnyUrl
    weight: float
    height: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight /(self.height ** 2), 2)
        return bmi
def insert_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.allergies[0])
    print(patient.allergies[1])
    print(patient.email)
    print(patient.linkedin_url)
    print("BMI", patient.bmi)
    # print(patient.contact_details["email"])
    print(patient.contact_details["phone"])
    print("inserted")

def update_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.email)
    print("updated")

patient_info = {"name": "abdullah", "email": "abdullah@hdfc.com", "linkedin_url": "https://www.linkedin.com/in/abdullah", "age": 26, "weight": 70.5, "height": 1.75, "allergies": ["pollen", "dust"], "married": False, "contact_details": { "phone": "123-456-7890"}}

patient1 = Patient(**patient_info)

insert_patient(patient1)

update_patient(patient1)