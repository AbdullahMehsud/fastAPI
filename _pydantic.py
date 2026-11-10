from pydantic import BaseModel

class Patient(BaseModel):
    name: str
    age: int

def insert_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("inserted")

patient_info = {"name": "abdullah", "age": 26}

patient1 = Patient(**patient_info)

insert_patient(patient1)