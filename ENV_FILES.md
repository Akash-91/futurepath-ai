# Environment files and Google OAuth

FuturePath AI uses application-level Google OAuth credentials. **A new user never uploads or enters these credentials.** The credentials belong to the FuturePath deployment and are configured once by the application owner.

## Local Docker development

Create `backend/.env` from `backend/.env.example` and set:

```dotenv
JWT_SECRET=<strong-random-secret>
GOOGLE_CLIENT_ID=<your-google-web-client-id>
GOOGLE_CLIENT_SECRET=<your-google-client-secret>
FRONTEND_URL=http://localhost:3000
BACKEND_URL=http://localhost:8000
COOKIE_SECURE=false
```

`backend/.env` is intentionally ignored by Git. Never commit the real Google client secret or JWT secret.

## Production

Configure the same variables as deployment-level environment/secret values. Do not put production secrets in the repository.

At minimum:

- `GOOGLE_CLIENT_ID`: the public OAuth client identifier for FuturePath AI.
- `GOOGLE_CLIENT_SECRET`: the private OAuth client secret; server-side only.
- `JWT_SECRET`: a long, random signing secret unique to the deployment.
- `FRONTEND_URL`: the public FuturePath frontend URL.
- `BACKEND_URL`: the public FuturePath API URL.
- `COOKIE_SECURE=true`: required when the application is served over HTTPS.

For a production deployment, configure the Google OAuth client with the exact callback URL:

`https://<your-api-domain>/auth/google/callback`

The Google OAuth client is created once by the FuturePath owner. Every user then clicks **Continue with Google**, authenticates with their own Google account, and FuturePath automatically creates or finds their user record.

## What users need

Users only need their own Google account. They do **not** need:

- Google Cloud Console access
- a Google Client ID
- a Google Client Secret
- a `.env` file
- Docker

The browser talks to FuturePath's login endpoint; the backend performs the OAuth exchange using the deployment's server-side credentials.

## Docker note

The Docker Compose file injects `backend/.env` into the API container with `env_file`. The frontend only receives `NEXT_PUBLIC_API_BASE_URL`, which is safe to expose to the browser. The Google Client Secret is never sent to the frontend.
