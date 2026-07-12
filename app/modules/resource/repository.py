from sqlalchemy.orm import Session
from app.modules.resource.model import Resource

class ResourceRepository:

    @staticmethod
    def get_all(db: Session):
        return db.query(Resource).order_by(Resource.id.desc()).all()

    @staticmethod
    def get_by_id(db: Session, resource_id: int):
        return db.query(Resource).filter(Resource.id == resource_id).first()

    @staticmethod
    def create(db: Session, resource: Resource) -> Resource:
        db.add(resource)
        db.commit()
        db.refresh(resource)
        return resource

    @staticmethod
    def save(db: Session, resource: Resource) -> Resource:
        db.commit()
        db.refresh(resource)
        return resource

    @staticmethod
    def delete(db: Session, resource: Resource):
        db.delete(resource)
        db.commit()