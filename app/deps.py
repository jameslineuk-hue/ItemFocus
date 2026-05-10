from fastapi import Header, HTTPException

from app import config


def require_admin(
    authorization: str | None = Header(default=None),
    x_admin_key: str | None = Header(default=None, alias="X-Admin-Key"),
) -> None:
    if not config.ADMIN_SECRET:
        raise HTTPException(status_code=503, detail="Admin API is not configured")
    token = ""
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization[7:].strip()
    elif x_admin_key:
        token = x_admin_key.strip()
    if not token or token != config.ADMIN_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")
