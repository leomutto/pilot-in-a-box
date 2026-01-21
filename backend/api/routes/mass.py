from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.db.session import get_db
from backend.models.mass_request import MassRequest
from backend.dependencies.dependencies import get_current_user

router = APIRouter(prefix="/mass-requests", tags=["mass"])


# ---------------------------------------------------------
# LISTAR MASS REQUESTS
# ---------------------------------------------------------
@router.get("/")
def list_mass_requests(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return db.query(MassRequest).all()


# ---------------------------------------------------------
# OBTENER MASS REQUEST POR ID
# ---------------------------------------------------------
@router.get("/{request_id}")
def get_mass_request(
    request_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    req = db.query(MassRequest).filter(MassRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Mass request not found")
    return req


# ---------------------------------------------------------
# CREAR MASS REQUEST
# ---------------------------------------------------------
@router.post("/")
def create_mass_request(
    payload: dict,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    new_req = MassRequest(**payload)
    db.add(new_req)
    db.commit()
    db.refresh(new_req)
    return new_req


# ---------------------------------------------------------
# ELIMINAR MASS REQUEST
# ---------------------------------------------------------
@router.delete("/{request_id}")
def delete_mass_request(
    request_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    req = db.query(MassRequest).filter(MassRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Mass request not found")

    db.delete(req)
    db.commit()
    return {"message": "Mass request deleted"}