# Vortex Lotto Global Karma 2026 — PRD

## Original Problem Statement
User had an existing non-profit app ("Vortex Lotto Global Karma 2026") started on GitHub
(senci33-wq/Vortex-Lotto-Global-Karma-2026), originally built with **Python + Kivy** (main.py,
buildozer.spec). They wanted to finish it and test it **in the browser** before a Google Play
release (needs testers). The app is a non-profit quantum lottery number generator that also
promotes charitable donation projects ("Karma"). Uses ANU QRNG + external charity sites.
All UI text in GERMAN.

## Architecture / Decision
- Kivy cannot run on this platform → rebuilt as **Expo (React Native Web) + FastAPI + MongoDB**.
- Runs in browser (web preview) for testers AND as a future Android build.
- Backend proxies the ANU Quantum Random Number Generator (key in `ANU_API_KEY`); when no key is
  present it falls back to a cryptographically-secure RNG (`secrets`), labelled honestly in the UI.
- Original `projekte.json` (107 charity projects, 9 categories) embedded at `/app/backend/data/`.

## User Personas
- Non-profit supporter / lottery enthusiast who wants quantum-random numbers and discovers
  charities to support ("Karma").
- Beta testers using the browser version before Play Store launch.

## Core Requirements (static)
- 4 lottery games: Eurojackpot, Lotto 6aus49, Glücksspirale, Freiheit+.
- True/secure random number generation.
- Karma directory of 100+ donation orgs grouped by category with external links.
- Privacy-first (no tracking, no accounts), German UI, cosmic/quantum dark design.

## Implemented (with dates)
### 2026-06-28 — MVP
- Backend: `/api/games`, `/api/quantum/draw`, `/api/projects`, `/api/draws` (CRUD),
  `/api/analysis`. ANU quantum + crypto fallback. Rejection sampling (no modulo bias).
- Frontend tabs: Generator, Analyse, Karma, Vision (expo-router Tabs).
  - Generator: game chips + "QUANTUM ZIEHEN" with animated glowing balls + source badge.
  - Analyse: add/list/delete historical draws + HOT-number frequency bars.
  - Karma: hero, category chip filter, 107 project cards opening external sites.
  - Vision: manifesto + Datenschutz + contact.
- Design: Rajdhani + IBM Plex Sans fonts, cosmic dark theme, hero images.
- Full-stack tested by testing_agent (14/14 backend, all frontend flows pass).

### 2026-06-28 — Iteration 2 (user requests)
- **Karma random picker (the "heart"):** `GET /api/karma/random?category=` picks a project
  **uniformly at random** (rejection sampling) from all or one category. Prominent button +
  reveal modal ("Projekt öffnen" / "Nochmal ziehen"). source quantum/crypto labelled.
- **Unsorted combinations:** quantum draws now returned in drawn order (no sorting), like a
  real live draw.

## Known Minor Items
- IBM Plex Sans .ttf may fall back to system font on web preview (cosmetic).
- react-native-web deprecation warnings (shadow*/textShadow*/pointerEvents) — non-blocking.

## Backlog / Next
- P1: Provide real `ANU_API_KEY` to enable true quantum source (user to supply).
- P1: Optional Lotto-SYNC (fetch real winning numbers) — deferred per user.
- P2: Toggle sorted/unsorted view; share/copy a generated combination.
- P2: Persist favourite Karma projects locally.
