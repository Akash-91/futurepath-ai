# Environment files explained

- `backend/.env`: local runtime configuration consumed by Docker Compose. It contains a development-only JWT secret and blank Google OAuth values.
- `backend/.env.example`: template showing the required backend settings.
- `frontend/.env.local`: local frontend API URL for running Next.js outside Docker.
- `frontend/.env.example` and `frontend/.env.local.example`: frontend configuration templates.
- `.dockerignore` in each service prevents local `.env` files from being copied into the corresponding image.
- `.gitignore` prevents real environment files from being committed to Git.

The Docker Compose file injects `backend/.env` into the API container using `env_file`. The frontend API URL is passed as a Docker build argument because `NEXT_PUBLIC_*` variables are embedded into the Next.js browser bundle at build time.
