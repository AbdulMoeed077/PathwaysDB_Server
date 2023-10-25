from pydantic import BaseModel
from pydantic import Field

class RoleBase(BaseModel):
    name: str = Field(max_length=35)

class Role(RoleBase):
    id: str 
    is_active: bool
    
    class Config:
        from_attributes = True