import os
import json
import secrets
import logging
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Optional

import requests
from fastapi import FastAPI, APIRouter, HTTPException, Query
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
import uuid

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")

mongo_url = os.environ["MONGO_URL"]
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ["DB_NAME"]]

app = FastAPI(title="Vortex Lotto Global Karma 2026")
api_router = APIRouter(prefix="/api")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("vortex")

# ---------------------------------------------------------------------------
# Lottery configuration (mirrors the original Kivy app)
#   mc = main count, mm = main max, ec = extra count, em = extra max
# ---------------------------------------------------------------------------
GAMES = {
    "EJ": {"key": "EJ", "name": "Eurojackpot", "color": "#22d3ee", "mc": 5, "mmin": 1, "mm": 50,
           "ec": 2, "emin": 1, "em": 12, "extraLabel": "Eurozahlen", "digits": False},
    "L649": {"key": "L649", "name": "Lotto 6aus49", "color": "#10b981", "mc": 6, "mmin": 1, "mm": 49,
             "ec": 1, "emin": 0, "em": 9, "extraLabel": "Superzahl", "digits": False},
    "GS": {"key": "GS", "name": "Glücksspirale", "color": "#fbbf24", "mc": 7, "mmin": 0, "mm": 9,
           "ec": 0, "emin": 0, "em": 0, "extraLabel": None, "digits": True},
    "FR": {"key": "FR", "name": "Freiheit+", "color": "#f43f5e", "mc": 7, "mmin": 1, "mm": 38,
           "ec": 0, "emin": 0, "em": 0, "extraLabel": None, "digits": False},
}

PROJECTS_FILE = ROOT_DIR / "data" / "projekte.json"
ANU_URL = "https://api.quantumnumbers.anu.edu.au/"


# ---------------------------------------------------------------------------
# Quantum / crypto randomness
# ---------------------------------------------------------------------------
def _fetch_anu(n: int) -> Optional[List[int]]:
    key = os.environ.get("ANU_API_KEY", "").strip()
    if not key:
        return None
    try:
        r = requests.get(
            ANU_URL,
            headers={"x-api-key": key},
            params={"type": "uint16", "length": max(1, min(n, 1024))},
            timeout=8,
        )
        data = r.json()
        if r.status_code == 200 and data.get("success") and isinstance(data.get("data"), list):
            return [int(x) for x in data["data"]]
        logger.warning("ANU API non-success: %s", data)
    except Exception as e:  # noqa: BLE001
        logger.warning("ANU API failed: %s", e)
    return None


class RandomPool:
    """Yields random 16-bit ints from a quantum pool, refilling with crypto bytes."""

    def __init__(self, pool: List[int], source: str):
        self._pool = pool
        self._i = 0
        self.source = source

    def _next(self) -> int:
        if self._i >= len(self._pool):
            self._pool.extend(secrets.randbelow(65536) for _ in range(64))
        v = self._pool[self._i]
        self._i += 1
        return v

    def pick(self, count: int, lo: int, hi: int, unique: bool = True) -> List[int]:
        span = hi - lo + 1
        limit = 65536 - (65536 % span)  # rejection sampling to avoid modulo bias
        res: List[int] = []
        guard = 0
        while len(res) < count and guard < 100000:
            guard += 1
            r = self._next()
            if r >= limit:
                continue
            v = lo + (r % span)
            if unique and v in res:
                continue
            res.append(v)
        return res


def make_pool(n: int) -> RandomPool:
    quantum = _fetch_anu(n)
    if quantum:
        return RandomPool(quantum, "quantum")
    return RandomPool([secrets.randbelow(65536) for _ in range(max(n, 32))], "crypto")


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------
class DrawCreate(BaseModel):
    game: str
    main: List[int]
    extra: List[int] = Field(default_factory=list)


class Draw(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    game: str
    main: List[int]
    extra: List[int] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@api_router.get("/")
async def root():
    return {"app": "Vortex Lotto Global Karma 2026", "status": "ok"}


@api_router.get("/games")
async def get_games():
    return {"games": list(GAMES.values())}


@api_router.post("/quantum/draw")
async def quantum_draw(payload: dict):
    game = payload.get("game")
    cfg = GAMES.get(game)
    if not cfg:
        raise HTTPException(status_code=400, detail="Unbekanntes Spiel")

    pool = make_pool(48)
    if cfg["digits"]:
        # Glücksspirale: 7 single digits 0-9 (repetition allowed), order preserved
        main = pool.pick(cfg["mc"], cfg["mmin"], cfg["mm"], unique=False)
    else:
        # Drawn order (unsorted), like a real live draw
        main = pool.pick(cfg["mc"], cfg["mmin"], cfg["mm"], unique=True)

    extra: List[int] = []
    if cfg["ec"] > 0:
        extra = pool.pick(cfg["ec"], cfg["emin"], cfg["em"], unique=True)

    return {
        "game": game,
        "name": cfg["name"],
        "main": main,
        "extra": extra,
        "source": pool.source,
        "extraLabel": cfg["extraLabel"],
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


@api_router.get("/projects")
async def get_projects():
    try:
        with open(PROJECTS_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Projekte nicht ladbar: {e}")

    categories = []
    total = 0
    for cat, items in raw.items():
        projects = [{"name": it[0], "url": it[1]} for it in items if len(it) >= 2]
        total += len(projects)
        categories.append({"category": cat, "count": len(projects), "projects": projects})
    return {"categories": categories, "total": total}


@api_router.post("/draws", response_model=Draw)
async def add_draw(payload: DrawCreate):
    cfg = GAMES.get(payload.game)
    if not cfg:
        raise HTTPException(status_code=400, detail="Unbekanntes Spiel")
    if len(payload.main) < cfg["mc"]:
        raise HTTPException(status_code=400, detail=f"Mindestens {cfg['mc']} Zahlen erforderlich")
    draw = Draw(game=payload.game, main=payload.main[: cfg["mc"]], extra=payload.extra[: cfg["ec"]])
    await db.draws.insert_one(draw.model_dump())
    return draw


@api_router.get("/draws", response_model=List[Draw])
async def list_draws(game: str = Query(...)):
    docs = await db.draws.find({"game": game}, {"_id": 0}).sort("created_at", -1).to_list(500)
    return [Draw(**d) for d in docs]


@api_router.delete("/draws/{draw_id}")
async def delete_draw(draw_id: str):
    res = await db.draws.delete_one({"id": draw_id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Ziehung nicht gefunden")
    return {"deleted": draw_id}


@api_router.get("/analysis")
async def analysis(game: str = Query(...)):
    cfg = GAMES.get(game)
    if not cfg:
        raise HTTPException(status_code=400, detail="Unbekanntes Spiel")
    docs = await db.draws.find({"game": game}, {"_id": 0, "main": 1}).to_list(1000)

    counts = {n: 0 for n in range(cfg["mmin"], cfg["mm"] + 1)}
    for d in docs:
        for v in d.get("main", []):
            if v in counts:
                counts[v] += 1

    items = [{"n": n, "count": c} for n, c in counts.items()]
    max_count = max((i["count"] for i in items), default=0)
    by_count = sorted(items, key=lambda x: (-x["count"], x["n"]))
    hot = [i for i in by_count if i["count"] > 0][:6]
    cold = sorted(items, key=lambda x: (x["count"], x["n"]))[:6]

    return {
        "game": game,
        "name": cfg["name"],
        "totalDraws": len(docs),
        "max": max_count,
        "counts": items,
        "hot": hot,
        "cold": cold,
    }


@api_router.get("/karma/random")
async def karma_random(category: str = Query("ALLE")):
    try:
        with open(PROJECTS_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Projekte nicht ladbar: {e}")

    pool_items = []
    for cat, items in raw.items():
        if category != "ALLE" and cat != category:
            continue
        for it in items:
            if len(it) >= 2:
                pool_items.append({"name": it[0], "url": it[1], "category": cat})

    if not pool_items:
        raise HTTPException(status_code=404, detail="Keine Projekte gefunden")

    pool = make_pool(8)
    # Uniform pick via rejection sampling over [0, n-1]
    idx = pool.pick(1, 0, len(pool_items) - 1, unique=True)[0]
    chosen = pool_items[idx]

    return {
        "project": {"name": chosen["name"], "url": chosen["url"]},
        "category": chosen["category"],
        "poolSize": len(pool_items),
        "source": pool.source,
        "picked_at": datetime.now(timezone.utc).isoformat(),
    }


app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
