from pydantic import BaseModel,Field


class RoleBase(BaseModel):
    name: str = Field(min_length=2,max_length=50)


class RoleCreate(RoleBase):
    pass


class RoleResponse(RoleBase):
    id: int

    model_config = {
        "from_attributes": True
    }