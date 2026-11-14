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

temp = patient1.model_dump()
temp = patient1.model_dump(include={"name", "age"})
temp = patient1.model_dump(exclude={"name", "age"})
temp1 = patient1.model_dump_json()

print(temp)
print(type(temp))

print(temp1)
print(type(temp1))