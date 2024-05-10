from pydantic import BaseModel


class BaseDTO(BaseModel):
    class Config:
        orm_mode = True
        use_enum_values = True
