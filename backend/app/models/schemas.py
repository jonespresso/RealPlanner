from pydantic import BaseModel

class Property(BaseModel):
    id: int
    address: str
    description: str
    open_hours: str
    link: str

    class Config:
        orm_mode = True