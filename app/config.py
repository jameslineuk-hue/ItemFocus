import os

from dotenv import load_dotenv

load_dotenv()


def _require(name: str) -> str:
    v = os.getenv(name, "").strip()
    if not v:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return v


SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "").strip()


def assert_supabase_config() -> None:
    _require("SUPABASE_URL")
    _require("SUPABASE_SERVICE_ROLE_KEY")
