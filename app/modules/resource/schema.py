from enum import Enum
from pydantic import BaseModel, ConfigDict, Field

class ResourceType(str, Enum):
    ARTICULO = "Articulo"
    ENLACE = "Enlace"

class ResourceCreate(BaseModel):
    title: str = Field(max_length=150)
    description: str | None = None
    type: ResourceType
    url: str | None = Field(default=None, max_length=255)

class ResourceUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=150)
    description: str | None = None
    type: ResourceType | None = None
    url: str | None = Field(default=None, max_length=255)

class ResourceResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    type: str | None = None
    url: str | None = None
    created_by: int | None = None
    model_config = ConfigDict(from_attributes=True)