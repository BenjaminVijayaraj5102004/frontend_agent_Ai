from pydantic import BaseModel


class About(BaseModel):
    name:str
    age :int
    dob :str
    gender:str
    profession:str
    studies:str
    