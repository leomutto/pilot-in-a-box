from sqlalchemy.orm import Session
from models.item import Item

def get_item(db, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()