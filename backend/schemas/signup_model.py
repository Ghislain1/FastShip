from pydantic import BaseModel
from typing import Optional


class SignUpModel(BaseModel):
    id: Optional[int]
    username: str  # = Field(..., min_length=1, max_length=10)
    email: str
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]

    # Binding DTO to Model
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "johndoe@yahoo.fr",
                "password": "000",
                "is_active": True,
                "is_staff": False,
            }
        }
