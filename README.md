## ItemFocus

ItemFocus builds on the idea behind KeyFocus with a clearer scope: attach a QR tag to valuables (laptop, keys, wallet, …). Someone who finds the item opens the link and sees owner contact details. This version is engineered for deployment on Render with contact data persisted in Supabase.

The stack combines:

- **Python (FastAPI)** — small REST API backed by Supabase and **serves** the bundled static HTML/CSS/JS from `static/` on the same host.
- **Static site** — `index.html`, `create.html`, and `finder` flow in `found.html`, calling `/api/*` on the same origin.

### Prerequisites

1. Create a Supabase project.
2. In the SQL editor, run [`sql/001_finder_tags.sql`](sql/001_finder_tags.sql).
3. In **Project Settings → API**, note:
   - `Project URL`
   - `service_role` key (keep secret; **never expose it to the browser**)

The backend uses **only** the **service role** key server-side so the table can stay locked down behind Row Level Security with no anon policies.

### API

| Method | Path | Purpose |
|--------|------|--------|
| `GET` | `/api/health` | Liveness for hosting checks |
| `POST` | `/api/tags` | Create a tag; body `{ "category", "owner_name", "owner_phone" }` |
| `GET` | `/api/tags/{code}` | Finder lookup by public code (`IF-XXXXXX`) |

Responses use JSON. New tags receive `public_code`, `finder_path`, and `finder_url`.

### Running locally

Use **Python 3.11** (see [`.python-version`](.python-version)) so dependency wheels resolve cleanly—for example macOS/Homebrew defaults to too-new Python builds that may compile pydantic from source.

```bash
cd ItemFocus
python3.11 -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # edit with your Supabase credentials
uvicorn app.main:app --reload --port 8000
```

Then open:

- http://localhost:8000/index.html  
- http://localhost:8000/create.html  

The finder page expects a query string, for example:

- http://localhost:8000/found.html?code=IF-AB12CD  

### Deploying on Render

1. Push this repository to GitHub or GitLab.
2. In Render: **New** → **Blueprint** and select the repo, or **New** → **Web Service** with:
   - **Runtime:** Python  
   - **Build command:** `pip install -r requirements.txt`  
   - **Start command:**  
     `uvicorn app.main:app --host 0.0.0.0 --port $PORT --proxy-headers --forwarded-allow-ips '*'`  
3. Add environment variables in the service:
   - `SUPABASE_URL`
   - `SUPABASE_SERVICE_ROLE_KEY`
4. Deploy. Visiting `/` loads `index.html` via `StaticFiles(html=True)`; use `/found.html?code=…` from printed or generated QR codes.

This repo includes [`render.yaml`](render.yaml) for a Blueprint (`sync: false` means set Supabase vars in the Render dashboard).

### Security notes

- Treat each tag URL like a bearer secret—anyone with the link can view the saved contact fields.
- Rotate the service role key if it leaks; GitHub bots should ignore `.env` via [.gitignore](.gitignore).
- Prefer HTTPS (Render provides TLS). `--proxy-headers` keeps `finder_url` on `https://` when created through the deployed API.

### Learnings carried from KeyFocus

- Clear separation between **public landing** and **code-gated finder** UX.
- Short, human-readable codes with a distinctive prefix (**IF-**).
- Printable QR workflows (still using a hosted QR image service on the create page; swap for a local library later if you need fully offline QR generation).

### Next iterations (ideas)

- Owner login and edit/disable tags.
- Rate limiting on finder lookups.
- Optional message field (“Reward offered”, dorm room, …).
- Optional hash-based tokens instead of enumerable codes.
