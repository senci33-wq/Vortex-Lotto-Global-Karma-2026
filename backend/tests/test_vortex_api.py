"""Backend API tests for Vortex Lotto Global Karma 2026."""
import os
import pytest
import requests

BASE_URL = (
    os.environ.get("EXPO_PUBLIC_BACKEND_URL")
    or os.environ.get("EXPO_BACKEND_URL")
    or "https://project-ready-go.preview.emergentagent.com"
).rstrip("/")
API = f"{BASE_URL}/api"


@pytest.fixture(scope="module")
def session():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


# ---- Health ----
class TestHealth:
    def test_root(self, session):
        r = session.get(f"{API}/")
        assert r.status_code == 200
        body = r.json()
        assert body.get("status") == "ok"


# ---- Games metadata ----
class TestGames:
    def test_list_games(self, session):
        r = session.get(f"{API}/games")
        assert r.status_code == 200
        games = r.json().get("games", [])
        keys = {g["key"] for g in games}
        assert keys == {"EJ", "L649", "GS", "FR"}, f"Got: {keys}"


# ---- Quantum draws per game ----
class TestQuantumDraw:
    @pytest.mark.parametrize("game,mc,mmin,mmax,ec,emin,emax,unique_main", [
        ("EJ", 5, 1, 50, 2, 1, 12, True),
        ("L649", 6, 1, 49, 1, 0, 9, True),
        ("GS", 7, 0, 9, 0, 0, 0, False),  # digits, repetition allowed
        ("FR", 7, 1, 38, 0, 0, 0, True),
    ])
    def test_draw_shape(self, session, game, mc, mmin, mmax, ec, emin, emax, unique_main):
        r = session.post(f"{API}/quantum/draw", json={"game": game})
        assert r.status_code == 200, r.text
        data = r.json()
        assert data["game"] == game
        assert data["source"] in ("crypto", "quantum")
        # Both sources are valid: server uses ANU legacy buffer (1/min) with crypto fallback
        main = data["main"]
        assert len(main) == mc, f"{game}: main len {len(main)} != {mc}"
        for v in main:
            assert mmin <= v <= mmax, f"{game}: main val {v} out of range [{mmin},{mmax}]"
        if unique_main:
            assert len(set(main)) == mc, f"{game}: main values not unique: {main}"
        extra = data["extra"]
        assert len(extra) == ec, f"{game}: extra len {len(extra)} != {ec}"
        for v in extra:
            assert emin <= v <= emax

    def test_unknown_game_400(self, session):
        r = session.post(f"{API}/quantum/draw", json={"game": "XXX"})
        assert r.status_code == 400


# ---- Projects ----
class TestProjects:
    def test_projects_total(self, session):
        r = session.get(f"{API}/projects")
        assert r.status_code == 200
        data = r.json()
        assert "categories" in data and "total" in data
        # Spec: 107 projects
        assert data["total"] == 107, f"total = {data['total']} (expected 107)"
        # Each category has projects list of name/url pairs
        for cat in data["categories"]:
            assert "category" in cat and "projects" in cat
            for p in cat["projects"]:
                assert "name" in p and "url" in p


# ---- Draws CRUD + Analysis ----
class TestDrawsCRUD:
    created_ids = []

    def test_create_draw(self, session):
        payload = {"game": "EJ", "main": [1, 2, 3, 4, 5], "extra": [1, 2]}
        r = session.post(f"{API}/draws", json=payload)
        assert r.status_code == 200, r.text
        d = r.json()
        assert d["game"] == "EJ"
        assert d["main"] == [1, 2, 3, 4, 5]
        assert d["extra"] == [1, 2]
        assert "id" in d
        TestDrawsCRUD.created_ids.append(d["id"])

    def test_create_invalid_short(self, session):
        r = session.post(f"{API}/draws", json={"game": "EJ", "main": [1, 2], "extra": []})
        assert r.status_code == 400

    def test_create_unknown_game(self, session):
        r = session.post(f"{API}/draws", json={"game": "ZZZ", "main": [1,2,3,4,5], "extra": []})
        assert r.status_code == 400

    def test_list_draws(self, session):
        r = session.get(f"{API}/draws", params={"game": "EJ"})
        assert r.status_code == 200
        rows = r.json()
        assert isinstance(rows, list)
        assert any(d["id"] in TestDrawsCRUD.created_ids for d in rows)

    def test_analysis(self, session):
        r = session.get(f"{API}/analysis", params={"game": "EJ"})
        assert r.status_code == 200
        a = r.json()
        for k in ("totalDraws", "counts", "hot", "cold", "max"):
            assert k in a, f"missing {k}"
        assert a["totalDraws"] >= 1
        # counts covers 1..50 for EJ
        ns = {c["n"] for c in a["counts"]}
        assert ns == set(range(1, 51))

    def test_delete_draw_and_404(self, session):
        for did in TestDrawsCRUD.created_ids:
            r = session.delete(f"{API}/draws/{did}")
            assert r.status_code == 200
            # second delete -> 404
            r2 = session.delete(f"{API}/draws/{did}")
            assert r2.status_code == 404
        TestDrawsCRUD.created_ids.clear()


# ---- Karma random project ----
class TestKarmaRandom:
    def test_karma_all(self, session):
        r = session.get(f"{API}/karma/random", params={"category": "ALLE"})
        assert r.status_code == 200, r.text
        data = r.json()
        assert "project" in data and "name" in data["project"] and "url" in data["project"]
        assert data["source"] in ("crypto", "quantum")
        assert data["poolSize"] == 107, f"poolSize {data['poolSize']} != 107 for ALLE"
        assert "category" in data and data["category"]

    def test_karma_augsburg_restricts(self, session):
        # Verify category restriction: every sample stays inside requested category
        # and poolSize matches the count for that category from /projects
        r_proj = session.get(f"{API}/projects")
        assert r_proj.status_code == 200
        cats = {c["category"]: c["count"] for c in r_proj.json()["categories"]}
        assert "AUGSBURG" in cats, f"AUGSBURG not in categories: {list(cats)}"
        expected = cats["AUGSBURG"]

        for _ in range(5):
            r = session.get(f"{API}/karma/random", params={"category": "AUGSBURG"})
            assert r.status_code == 200, r.text
            d = r.json()
            assert d["category"] == "AUGSBURG", f"got {d['category']}"
            assert d["poolSize"] == expected, f"poolSize {d['poolSize']} != {expected}"
            assert d["source"] in ("crypto", "quantum")

    def test_karma_unknown_category_404(self, session):
        r = session.get(f"{API}/karma/random", params={"category": "NICHT_VORHANDEN"})
        assert r.status_code == 404
