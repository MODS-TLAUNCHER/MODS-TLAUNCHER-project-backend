from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user, get_db, require_admin
from app.modules.resource.schema import ResourceCreate, ResourceResponse, ResourceUpdate
from app.modules.resource.service import ResourceService
from app.modules.user.model import User

router = APIRouter(prefix="/resources", tags=["Resources"])

@router.get("", response_model=List[ResourceResponse])
def get_resources(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ResourceService.get_all(db)

@router.get("/{resource_id}", response_model=ResourceResponse)
def get_resource(
    resource_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ResourceService.get_by_id(db, resource_id)

@router.post("", response_model=ResourceResponse, status_code=201)
def create_resource(
    payload: ResourceCreate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    return ResourceService.create(db, admin.id, payload)

@router.patch("/{resource_id}", response_model=ResourceResponse)
def update_resource(
    resource_id: int,
    payload: ResourceUpdate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    return ResourceService.update(db, resource_id, payload)


@router.delete("/{resource_id}")
def delete_resource(
    resource_id: int,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    return ResourceService.delete(db, resource_id)