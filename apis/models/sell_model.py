from pydantic import BaseModel, Field


class SellModel(BaseModel):
    roll_number:str = Field(...)
    item_name:str = Field(...)
    cost:str = Field(...)
    images:str=Field(...)
    unique_good_number:int = Field(...)