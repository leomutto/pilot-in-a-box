from sqlalchemy.orm import Session
from repositories.item_repository import get_item
from schemas.item import Item

def get_item_by_id(db: Session, item_id: int) -> Item | None:
    item = get_item(db, item_id)
    if not item:
        return None
    return Item(
        id=item.id,
        name=item.name,
        description=item.description
    )