from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request

from app import codes, schemas
from app.db import get_client
from app.deps import require_admin

router = APIRouter(tags=["tags"])

_TABLE = "finder_tags"
_MAX_ATTEMPTS = 25


@router.post("/tags", response_model=schemas.CreateTagResponse, dependencies=[Depends(require_admin)])
def create_tag(body: schemas.CreateTagBody, request: Request) -> schemas.CreateTagResponse:
    supabase = get_client()
    name = body.owner_name.strip()
    phone = body.owner_phone.strip()

    for _ in range(_MAX_ATTEMPTS):
        public_code = codes.random_item_code()
        chk = (
            supabase.table(_TABLE)
            .select("public_code")
            .eq("public_code", public_code)
            .limit(1)
            .execute()
        )
        rows = getattr(chk, "data", None) or []
        if rows:
            continue

        row = {
            "public_code": public_code,
            "category": body.category,
            "owner_name": name,
            "owner_phone": phone,
        }
        supabase.table(_TABLE).insert(row).execute()

        finder_path = f"/found.html?code={public_code}"
        base = str(request.base_url).rstrip("/")
        finder_url = f"{base}{finder_path}"
        return schemas.CreateTagResponse(
            public_code=public_code,
            finder_path=finder_path,
            finder_url=finder_url,
        )

    raise HTTPException(status_code=500, detail="Could not allocate a unique tag code")


@router.get("/tags/{code}", response_model=schemas.FinderResponse)
def get_tag_for_finder(code: str) -> schemas.FinderResponse:
    key = codes.normalize_code(code)
    if not key:
        raise HTTPException(status_code=404, detail="Not found")

    supabase = get_client()
    res = (
        supabase.table(_TABLE)
        .select("public_code, category, owner_name, owner_phone")
        .eq("public_code", key)
        .limit(1)
        .execute()
    )
    data = getattr(res, "data", None) or []
    if not data:
        raise HTTPException(status_code=404, detail="Not found")

    row = data[0]
    return schemas.FinderResponse(
        public_code=row["public_code"],
        category=row["category"],
        owner_name=row["owner_name"],
        owner_phone=row["owner_phone"],
    )
