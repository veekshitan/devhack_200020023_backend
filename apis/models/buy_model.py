from pydantic import BaseModel, Field

class UserBuyModel(BaseModel):
    roll_number:str = Field(...)
    good_number:str = Field(...)