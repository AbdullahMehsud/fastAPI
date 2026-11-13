from pydantic import AnyUrl, BaseModel, EmailStr, Field
from typing import List
from typing import Optional, Dict, Annotated
class Patient(BaseModel):
    name: Annotated[str, Field(max_length=100, description="The name of the patient")]
    age: int = Field(gt=0, lt=120)
    email: EmailStr
    linkedin_url: AnyUrl
    weight: Annotated[float, Field(gt=0, strict=True)]
    married: Annotated[bool, Field(default=False, description="Indicates if the patient is married")]
    allergies: Optional[List[str]]
    contact_details: Dict[str, str]

def insert_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.allergies[0])
    print(patient.allergies[1])
    print(patient.email)
    print(patient.linkedin_url)
    # print(patient.contact_details["email"])
    print(patient.contact_details["phone"])
    print("inserted")

def update_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.email)
    print("updated")

patient_info = {"name": "abdullah", "email": "abdullah@example.com", "linkedin_url": "https://www.linkedin.com/in/abdullah", "age": 26, "weight": 70.5, "allergies": ["pollen", "dust"], "married": False, "contact_details": { "phone": "123-456-7890"}}

patient1 = Patient(**patient_info)

insert_patient(patient1)

update_patient(patient1)