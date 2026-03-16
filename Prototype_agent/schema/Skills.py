from pydantic import BaseModel


class skill(BaseModel):
    skill :str[list]
