# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

Repository: RealPlanner — a route planning app for realtors with a FastAPI backend and a React frontend.

Contents:
- Commands: build, run, test (including single-test examples)
- High-level architecture and where core logic lives
- Environment and debugging notes sourced from project docs

Commands

With Makefile (recommended)
- From repo root
  - Backend: make backend-install | backend-install-dev | backend-run | backend-test | backend-test-one FILE=tests/test_optimization.py | backend-curl-sh | backend-curl-py
  - Frontend: make frontend-install | frontend-start | frontend-build | frontend-test | frontend-test-one TEST=App.test.tsx or PATTERN="learn react"

Without Makefile

Backend (FastAPI, Python)
- Set environment (minimum for Routes API fallback)
  - In backend/.env
    - GOOGLE_MAPS_API_KEY={{GOOGLE_MAPS_API_KEY}}
    - GOOGLE_CLOUD_PROJECT_ID={{GOOGLE_CLOUD_PROJECT_ID}}
- Optional (Route Optimization API with OAuth)
  - In backend/.env
    - GOOGLE_SERVICE_ACCOUNT_KEY={"type": "service_account", ...}
    - Or point GOOGLE_SERVICE_ACCOUNT_KEY_PATH to a JSON file
- Start API server (expects frontend at http://localhost:3000 per CORS)
  - cd backend
  - uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --log-level debug
- Run all backend tests
  - cd backend
  - python3 tests/run_tests.py
- Run a single backend test (sample end-to-end optimization)
  - cd backend
  - python3 tests/test_optimization.py
- Quick API checks (server must be running)
- cd backend
  - ./scripts/test_with_curl.sh
  - Or: python3 scripts/test_with_curl.py

Frontend (React + TypeScript via Create React App)
- Install deps
  - cd frontend && npm install
- Start dev server
  - npm start
- Build
  - npm run build
- Run tests (watch mode)
  - npm test
- Run a single test
  - npm test -- App.test.tsx
  - or with a pattern: npm test -- -t "learn react"

High-level architecture

System overview (from README)
- Frontend: React + TypeScript (CRA), intended to integrate with Google Maps UI, generates JSON payloads for backend
- Backend: FastAPI service that plans optimized routes
- Data/identity: Supabase is referenced conceptually in README, but current codebase focuses on route planning logic (no active DB usage beyond a placeholder SQLAlchemy Base)
- External services: Google Route Optimization API (preferred), Google Routes API (fallback), plus internal greedy optimizer (final fallback)

Backend layout and flow
- Entry point: backend/app/main.py
  - Creates FastAPI app, sets CORS for localhost:3000, mounts API router
- API routing: backend/app/api/router.py → backend/app/api/v1/endpoints.py
  - GET /api/v1/ping
  - POST /api/v1/plan-route: accepts RoutePlanRequest; delegates to plan_optimized_route; returns RoutePlanResponse
  - POST /api/v1/generate-curl-commands: produces ready-to-run curl invocations for both Google APIs
- Config and logging: backend/app/core/
  - config.py: loads env via pydantic-settings and python-dotenv; includes helpers to locate/parse service account credentials
  - logging.py: configures structured logging; get_logger(name) sets DEBUG by default
- Schemas and models:
  - app/schemas/route.py: request/response models (HouseVisit, RoutePlanRequest, StopAssignment, RoutePlanResponse)
  - app/schemas/property.py: example Pydantic model (Property)
  - app/db/base.py: SQLAlchemy Base (no active persistence yet)
- Services (core route planning logic): backend/app/services/
  - routing.py: orchestrator. Steps:
    1) Geocode start/destination and each house address
    2) Build RouteOptimizationParams
    3) Try optimizers in order:
       - Google Route Optimization API (route_optimization_api.py)
       - Google Routes API (routes_api.py)
       - Greedy nearest-neighbor (greedy_optimizer.py)
    4) Return first successful route with optimization_method
  - route_optimization_api.py: integrates Google Route Optimization API; respects time windows; requires OAuth via service account
  - routes_api.py: integrates Google Routes API with optimizeWaypointOrder; API-key based; does not enforce time windows
  - greedy_optimizer.py: internal nearest-neighbor heuristic; computes schedule and validates time windows via time_windows.py
  - geocoding.py: address → lat/lng
  - time_windows.py: schedule computation and time window checks
  - curl_generator.py: builds example curl payloads for both Google APIs

Key behavioral notes (from docs)
- Fallback chain (ROUTE_OPTIMIZATION_ARCHITECTURE.md):
  1) Route Optimization API (best; enforces time windows)
  2) Routes API (good; does not enforce time windows; warnings emitted)
  3) Greedy algorithm (always available; no time-window enforcement; warnings emitted)
- Unified response format: the orchestrator normalizes outputs to RoutePlanResponse with route[] of stop assignments and optimization_method set to the method used
- Logging is verbose in DEBUG; watch server logs to see which optimizer was selected and why

Environment and configuration (backend/SETUP.md)
- Minimum to operate (Routes API + Greedy)
  - GOOGLE_MAPS_API_KEY and GOOGLE_CLOUD_PROJECT_ID
- Full setup (adds Route Optimization API)
  - Add GOOGLE_SERVICE_ACCOUNT_KEY (JSON string) or GOOGLE_SERVICE_ACCOUNT_KEY_PATH
  - Install auth libs if needed: pip install google-auth google-auth-oauthlib google-auth-httplib2
- The settings loader searches for .env using python-dotenv’s find_dotenv; service account key can be loaded from multiple path strategies

Testing strategy
- Backend includes runnable scripts instead of pytest by default
  - tests/run_tests.py executes the suite
  - tests/test_optimization.py runs an end-to-end flow against live Google APIs using future timestamps
  - Network access and valid API key are required
- Frontend uses CRA’s test runner (Jest + Testing Library)
  - Single test patterns supported via npm test -- -t "pattern"

Local development loop
- Start backend (port 8000) and frontend (port 3000); CORS is configured to allow http://localhost:3000
- Use frontend to construct payloads or run curl/python test scripts in backend to exercise the API
- For deeper backend debugging, see backend/docs/DEBUG_WITH_UVICORN_CURL.md and backend/docs/DEBUGGING_GUIDE.md (VS Code launch configs referenced there; step through route_optimization_api and routing orchestrator)

Notable files to consult
- README.md: product and system overview, tech choices, and future roadmap
- backend/ROUTE_OPTIMIZATION_ARCHITECTURE.md and backend/ROUTE_OPTIMIZATION.md: detailed design of the optimization approach and response normalization
- backend/SETUP.md: environment variables, differences between Google APIs, and troubleshooting
- backend/docs/DEBUG_WITH_UVICORN_CURL.md and backend/docs/DEBUGGING_GUIDE.md: practical debugging flows with uvicorn, curl, and VS Code

Gaps and cautions
- docker-compose.yaml and backend/Dockerfile are present but empty; prefer local runs via uvicorn and npm
- No centralized Python dependency manifest is committed (e.g., requirements.txt/pyproject.toml). If needed, install libs ad hoc as import errors surface (FastAPI, uvicorn, pydantic-settings, python-dotenv, requests, SQLAlchemy, google-auth, etc.)
- Time-window enforcement is only guaranteed when the Route Optimization API path succeeds; the fallback methods add validation/warnings but cannot enforce constraints

