# Movies Storage API

An async FastAPI backend where registered users can create, list, update, and delete only their own movies.

## Request flow

```text
HTTP request -> route -> service -> repository -> PostgreSQL -> response
```

- `app/routes/`: HTTP endpoints, validation, and dependencies.
- `app/services/`: business rules such as duplicate checks.
- `app/repositories/`: async SQLAlchemy queries and writes.
- `app/models/`: persisted SQLAlchemy entities.
- `app/schemas/`: Pydantic request and response models.
- `app/core/`: password hashing and JWT authentication.

## Authentication and ownership

1. `POST /auth/register` validates the email/password and stores a password hash.
2. `POST /auth/login` verifies the password and returns a JWT carrying `user_id`.
3. Protected movie endpoints read `Authorization: Bearer <token>`.
4. `get_current_user` verifies the JWT and returns its `user_id`.
5. List, update, and delete queries use that `user_id` as `owner_id`.

The important rule is: a movie ID identifies a movie, while the verified JWT user ID proves who may access it. Update and delete require both values in their database query.

## Local setup

Create a `.env` file with an async PostgreSQL URL:

```env
DATABASE_URL=postgresql+asyncpg://postgres:replace-with-your-password@localhost:5432/movies
SECRET_KEY=replace-with-a-long-random-secret
```

Generate a value for `SECRET_KEY` with:

```powershell
.\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_urlsafe(32))"
```

Install dependencies and run the API:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

## Tests

Run the Week 1 unit tests:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Remaining Week 1 hardening

- Move `SECRET_KEY` in `app/core/jwt.py` from source code into environment configuration before deploying.
- Add integration tests against an isolated PostgreSQL database for registration, login, and every CRUD endpoint.
- Review the migration history before changing the `movies.title` uniqueness rule; it is currently globally unique, even though movies are owned per user.
