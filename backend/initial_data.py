from sqlalchemy.orm import Session

from db.session import SessionLocal
from models.user import User
from core.security import hash_password


def init_admin():
    db: Session = SessionLocal()

    email = "admin@example.com"
    password = "CAMBIAR_POR_LEONARDO"

    user = db.query(User).filter(User.email == email).first()

    if not user:
        user = User(
            email=email,
            hashed_password=hash_password(password)
        )
        db.add(user)
        db.commit()
        print("Admin user created")
    else:
        print("Admin already exists")

    db.close()


if __name__ == "__main__":
    init_admin()