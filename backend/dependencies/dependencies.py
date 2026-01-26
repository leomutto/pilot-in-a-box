from fastapi import Depends

from core.security import get_current_user, require_role
from models.user import User


def current_user(user: User = Depends(get_current_user)) -> User:
    """
    Dependencia estándar para obtener el usuario autenticado.
    Uso en routers:
    def endpoint(user: User = Depends(current_user)):
        ...
    """
    return user


def admin_user(user: User = Depends(require_role("admin"))) -> User:
    """
    Dependencia para endpoints que requieren rol admin.
    Uso en routers:
    def endpoint(user: User = Depends(admin_user)):
        ...
    """
    return user
