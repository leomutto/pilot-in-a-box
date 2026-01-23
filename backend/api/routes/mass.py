from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.session import get_db
from models.mass import MassRequest
from dependencies.dependencies import get_current_user
from schemas.mass import MassRequestBase  # <-- IMPORTANTE

router = APIRouter(prefix="/mass-requests", tags=["mass"])


# ---------------------------------------------------------
# LISTAR MASS REQUESTS (solo del usuario autenticado)
# ---------------------------------------------------------
@router.get("/", response_model=list[MassRequestBase])
def list_mass_requests(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return db.query(MassRequest).filter(
        MassRequest.user_id == user.id
    ).all()


# ---------------------------------------------------------
# OBTENER MASS REQUEST POR ID (solo si pertenece al usuario)
# ---------------------------------------------------------
@router.get("/{request_id}", response_model=MassRequestBase)
def get_mass_request(
    request_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    req = db.query(MassRequest).filter(
        MassRequest.id == request_id,
        MassRequest.user_id == user.id
    ).first()

    if not req:
        raise HTTPException(status_code=404, detail="Mass request not found")

    return req


# ---------------------------------------------------------
# CREAR MASS REQUEST (asociado al usuario autenticado)
# ---------------------------------------------------------
@router.post("/", response_model=MassRequestBase)
def create_mass_request(
    payload: dict,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    new_req = MassRequest(
        user_id=user.id,
        payload_json=payload
    )

    db.add(new_req)
    db.commit()
    db.refresh(new_req)

    return new_req


# ---------------------------------------------------------
# ELIMINAR MASS REQUEST (solo si pertenece al usuario)
# ---------------------------------------------------------
@router.delete("/{request_id}")
def delete_mass_request(
    request_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    req = db.query(MassRequest).filter(
        MassRequest.id == request_id,
        MassRequest.user_id == user.id
    ).first()

    if not req:
        raise HTTPException(status_code=404, detail="Mass request not found")

    db.delete(req)
    db.commit()

    return {"message": "Mass request deleted"}