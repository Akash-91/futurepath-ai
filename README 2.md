# FuturePath AI — Login MVP

This is a starter MVP for FuturePath AI, currently focused on the login experience.

## Included
- Responsive Next.js login page
- Username/email and password login
- FastAPI authentication API
- Password hashing and JWT access tokens
- Optional Google OAuth/SSO scaffold
- SQLite persistence for local testing
- Dockerfiles, Docker Compose, and `.dockerignore` files for both services
- Local `.env` files plus safe example templates
- Step-by-step Docker instructions in [`DOCKER_GUIDE.md`](./DOCKER_GUIDE.md)

## Quick start with Docker

From this folder:

```bash
docker compose config
docker compose build
docker compose up -d
```

Then open:
- http://localhost:3000 — login
- http://localhost:8000/health — API health
- http://localhost:8000/docs — API docs

Create a local test user by following the registration command in `DOCKER_GUIDE.md`.

## Environment files

- `backend/.env` and `frontend/.env.local` are included for local convenience.
- `.env.example` files document the expected values.
- The included backend JWT secret is **development-only**. Replace it before any shared or public deployment.
- `.dockerignore` files prevent local environment files, dependencies, caches, and database data from being copied into build images.
- `.gitignore` prevents environment files from being committed accidentally.

## Important security note

This is not production-ready authentication. The current MVP passes the JWT in the URL during redirect. Replace this with an HttpOnly-cookie/session or one-time exchange-code design before deploying publicly. Google SSO requires your own OAuth credentials.
