from pydantic import AnyUrl, BaseModel, EmailStr, Field, field_validator
from typing import List
from typing import Optional, Dict, Annotated
class Patient(BaseModel):
    name: str
    age: int
    email: EmailStr
    linkedin_url: AnyUrl
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    @field_validator("email")
    @classmethod
    def email_validator(cls, value):
        valid_domains = ['hdfc.com', 'icici.com']
        domain_name = value.split("@")[-1]

        if domain_name not in valid_domains: 
            raise ValueError('Not a valid domain')
        return value

    @field_validator('name')
    @classmethod
    def transform_name(cls, value):
        return value.upper()

    @field_validator("age", mode="before")
    @classmethod
    def validate_age(cls, value):
        if value < 0:
            raise ValueError('Age cannot be negative')
        return value

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

patient_info = {"name": "abdullah", "email": "abdullah@hdfc.com", "linkedin_url": "https://www.linkedin.com/in/abdullah", "age": 26, "weight": 70.5, "allergies": ["pollen", "dust"], "married": False, "contact_details": { "phone": "123-456-7890"}}

patient1 = Patient(**patient_info)

insert_patient(patient1)

update_patient(patient1)