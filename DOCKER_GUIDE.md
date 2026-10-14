# FuturePath AI — Docker setup guide

This bundle contains a local MVP with a Next.js login page and FastAPI authentication API. Docker Compose runs both services. SQLite stores local test accounts in `backend/data/`.

> **Development only:** The included `backend/.env` contains a placeholder JWT secret so the project can start locally. Replace it with a strong secret before sharing the app or deploying it. The current MVP sends the JWT in a URL after login; do not deploy this authentication flow publicly until it is replaced with a secure HttpOnly-cookie/session flow.

## 1. Install Docker

Install and start Docker Desktop:
- macOS / Windows: https://www.docker.com/products/docker-desktop/
- Linux: install Docker Engine and the Docker Compose plugin.

Verify in a terminal:

```bash
docker --version
docker compose version
```

## 2. Extract the ZIP

Extract `futurepath-ai-mvp-docker.zip`. Open a terminal in the extracted `futurepath-ai-mvp-docker` directory — the same directory that contains `docker-compose.yml`.

Expected key files:

```text
futurepath-ai-mvp-docker/
├── docker-compose.yml
├── DOCKER_GUIDE.md
├── frontend/
│   ├── .dockerignore
│   ├── .env.local
│   ├── .env.example
│   ├── Dockerfile
│   └── package.json
└── backend/
    ├── .dockerignore
    ├── .env
    ├── .env.example
    ├── Dockerfile
    ├── requirements.txt
    └── app/
```

Files beginning with a dot can be hidden by your file manager. In VS Code, they should be visible in the Explorer; in Finder, use **Command + Shift + .** to show hidden files.

## 3. Configure the backend environment

Open `backend/.env`. It is included for local convenience and uses a development-only placeholder secret.

For a stronger local secret, generate one:

```bash
openssl rand -hex 32
```

Copy the output into the `JWT_SECRET=` value in `backend/.env`. Do not put quotation marks around the value. Keep this file private and do not commit it to Git.

Google SSO is optional. The app starts without Google credentials, but the Google button will report that SSO is not configured until you add credentials (see step 8).

## 4. Build the containers

Run these commands from the project root:

```bash
docker compose config
docker compose build
```

The first command checks the Compose configuration. The second builds the frontend and backend images.

## 5. Start the application

```bash
docker compose up -d
docker compose ps
```

Open these URLs:

- Frontend login page: http://localhost:3000
- Backend health check: http://localhost:8000/health
- Interactive API docs: http://localhost:8000/docs

The health endpoint should return JSON similar to:

```json
{"status":"ok","service":"futurepath-ai-api"}
```

## 6. Create a local test account

There is a backend registration endpoint, but the current login UI does not yet include a registration form. With the containers running, run this in a terminal:

```bash
curl -X POST http://localhost:8000/auth/register   -H "Content-Type: application/json"   -d '{
    "username": "demo",
    "email": "demo@example.com",
    "password": "DemoPassword123!"
  }'
```

A successful response returns the created user details. Then visit http://localhost:3000 and sign in using:

- Username: `demo`
- Password: `DemoPassword123!`

Use only this sample password for local testing. Change it if you adapt this project for real users.

If the account already exists, the API returns a conflict response; you can simply try logging in.

## 7. Useful Docker commands

Run / start:

```bash
docker compose up -d
```

View running services:

```bash
docker compose ps
```

Follow logs:

```bash
docker compose logs -f
```

View only API or frontend logs:

```bash
docker compose logs -f api
docker compose logs -f frontend
```

Rebuild after changing source files or Docker configuration:

```bash
docker compose up -d --build
```

Stop containers but keep local database data:

```bash
docker compose down
```

The SQLite database is persisted under `backend/data/`, so stopping or rebuilding containers does not normally delete local accounts.

To stop and also delete the database, manually remove `backend/data/` after stopping the containers. Only do this if you are happy to lose local test accounts.

## 8. Optional: enable Google SSO

1. Open Google Cloud Console: https://console.cloud.google.com/
2. Configure the OAuth consent screen.
3. Create an OAuth 2.0 Client ID with application type **Web application**.
4. Add this authorized redirect URI exactly:

   `http://localhost:8000/auth/google/callback`

5. Copy the client ID and secret into `backend/.env`:

   ```dotenv
   GOOGLE_CLIENT_ID=your-client-id
   GOOGLE_CLIENT_SECRET=your-client-secret
   ```

6. Restart the API:

   ```bash
   docker compose up -d --build api
   ```

Try **Continue with Google** on the login page. Google may require that your account be added as a test user while the consent screen is in testing mode.

## 9. Troubleshooting

### Port 3000 or 8000 is already in use
Stop the other process using that port, or change the left-hand port in `docker-compose.yml`. If you change the frontend port, also update `FRONTEND_URL` in `backend/.env` and the Compose environment.

### Login page loads but API calls fail
Check that the API is healthy at http://localhost:8000/health, then inspect:

```bash
docker compose logs --tail=100 api frontend
```

For this local Docker setup, the browser must use `http://localhost:8000` as the API URL. Do not change the frontend API URL to `http://api:8000`; the hostname `api` is for container-to-container networking, while browser requests need `localhost`.

### Google SSO returns a configuration error
Check `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` in `backend/.env`, confirm the callback URL exactly matches Google Cloud Console, and rebuild/restart the API.

### Start from a clean container build
```bash
docker compose down
docker compose build --no-cache
docker compose up -d
```

## 10. Security and production checklist

Before a public launch:
- Replace the JWT-in-URL redirect with a secure HttpOnly cookie/session or a one-time exchange code.
- Use HTTPS and secure cookie settings.
- Use a production-grade secret manager; never commit `.env`.
- Configure production CORS and OAuth callback URLs.
- Consider PostgreSQL, backups, rate limiting, email verification, password reset, monitoring, and a security review.
