from pydantic import BaseModel

class Address(BaseModel):
    city: str
    state: str
    post_code: str

class Patient(BaseModel):
    name: str
    age: int
    address: Address

address_dict = {"city": "New York", "state": "NY", "post_code": "10001"}
address = Address(**address_dict)

patient_dict = {"name": "John Doe", "age": 30, "address": address_dict}

patient1 = Patient(**patient_dict)

print(patient1.name)
print(patient1.age)
print(patient1.address.city)
print(patient1.address.state)
print(patient1.address.post_code)