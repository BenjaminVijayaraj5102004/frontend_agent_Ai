from pydantic import BaseModel

class contact(BaseModel):
    email:str
    phone:str
    linkedin:str
    github:str
    