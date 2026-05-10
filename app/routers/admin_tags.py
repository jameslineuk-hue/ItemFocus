from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request

from app import schemas
from app.deps import require_admin
from app.db import get_client

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(require_admin)])

_TABLE = "finder_tags"


def _finder_urls(request: Request, public_code: str) -> tuple[str, str]:
    finder_path = f"/found.html?code={public_code}"
    base = str(request.base_url).rstrip("/")
    finder_url = f"{base}{finder_path}"
    return finder_path, finder_url


@router.get("/tags", response_model=list[schemas.AdminTagRow])
def list_tags(request: Request) -> list[schemas.AdminTagRow]:
    supabase = get_client()
    res = (
        supabase.table(_TABLE)
        .select("id, public_code, category, owner_name, owner_phone, created_at")
        .order("created_at", desc=True)
        .execute()
    )
    rows = getattr(res, "data", None) or []
    out: list[schemas.AdminTagRow] = []
    for row in rows:
        pub = row["public_code"]
        path, url = _finder_urls(request, pub)
        out.append(
            schemas.AdminTagRow(
                id=row["id"],
                public_code=pub,
                category=row["category"],
                owner_name=row["owner_name"],
                owner_phone=row["owner_phone"],
                created_at=row["created_at"],
                finder_path=path,
                finder_url=url,
            )
        )
    return out


@router.get("/tags/{tag_id}", response_model=schemas.AdminTagRow)
def get_tag(request: Request, tag_id: UUID) -> schemas.AdminTagRow:
    supabase = get_client()
    res = (
        supabase.table(_TABLE)
        .select("id, public_code, category, owner_name, owner_phone, created_at")
        .eq("id", str(tag_id))
        .limit(1)
        .execute()
    )
    data = getattr(res, "data", None) or []
    if not data:
        raise HTTPException(status_code=404, detail="Not found")
    row = data[0]
    pub = row["public_code"]
    path, url = _finder_urls(request, pub)
    return schemas.AdminTagRow(
        id=row["id"],
        public_code=pub,
        category=row["category"],
        owner_name=row["owner_name"],
        owner_phone=row["owner_phone"],
        created_at=row["created_at"],
        finder_path=path,
        finder_url=url,
    )


@router.patch("/tags/{tag_id}", response_model=schemas.AdminTagRow)
def update_tag(request: Request, tag_id: UUID, body: schemas.UpdateTagBody) -> schemas.AdminTagRow:
    supabase = get_client()
    exists = (
        supabase.table(_TABLE).select("id").eq("id", str(tag_id)).limit(1).execute()
    )
    if not (getattr(exists, "data", None) or []):
        raise HTTPException(status_code=404, detail="Not found")
    name = body.owner_name.strip()
    phone = body.owner_phone.strip()
    supabase.table(_TABLE).update(
        {
            "category": body.category,
            "owner_name": name,
            "owner_phone": phone,
        }
    ).eq("id", str(tag_id)).execute()
    return get_tag(request, tag_id)


@router.delete("/tags/{tag_id}")
def delete_tag(tag_id: UUID) -> dict[str, str]:
    supabase = get_client()
    exists = (
        supabase.table(_TABLE).select("id").eq("id", str(tag_id)).limit(1).execute()
    )
    if not (getattr(exists, "data", None) or []):
        raise HTTPException(status_code=404, detail="Not found")
    supabase.table(_TABLE).delete().eq("id", str(tag_id)).execute()
    return {"status": "deleted"}
