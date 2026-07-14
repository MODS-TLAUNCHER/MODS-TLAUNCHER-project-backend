from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.modules.resource.model import Resource
from app.modules.resource.repository import ResourceRepository
from app.modules.resource.schema import ResourceCreate, ResourceUpdate

class ResourceService:

    @staticmethod
    def get_all(db: Session):
        return ResourceRepository.get_all(db)

    @staticmethod
    def get_by_id(db: Session, resource_id: int) -> Resource:
        resource = ResourceRepository.get_by_id(db, resource_id)
        if resource is None:
            raise HTTPException(status_code=404, detail="Recurso no encontrado")
        return resource

    @staticmethod
    def create(db: Session, admin_id: int, payload: ResourceCreate) -> Resource:
        resource = Resource(
            title=payload.title,
            description=payload.description,
            type=payload.type.value,
            url=payload.url,
            created_by=admin_id,
        )
        return ResourceRepository.create(db, resource)

    @staticmethod
    def update(db: Session, resource_id: int, payload: ResourceUpdate) -> Resource:
        resource = ResourceService.get_by_id(db, resource_id)
        data = payload.model_dump(exclude_unset=True)
        if "type" in data and data["type"] is not None:
            data["type"] = data["type"].value if hasattr(data["type"], "value") else data["type"]
        for field, value in data.items():
            setattr(resource, field, value)
        return ResourceRepository.save(db, resource)

    @staticmethod
    def delete(db: Session, resource_id: int):
        resource = ResourceService.get_by_id(db, resource_id)
        ResourceRepository.delete(db, resource)
        return {"message": "Recurso eliminado"}