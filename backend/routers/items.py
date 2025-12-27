from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.item import Item
from services.item_service import get_item_by_id
from dependencies.db import get_db

router = APIRouter(prefix="/items", tags=["Items"])

@router.get("/{item_id}", response_model=Item)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = get_item_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item