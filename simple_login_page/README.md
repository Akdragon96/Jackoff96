# Simple Login Page

A small Dockerized login and register app with:

- HTML, CSS, and JavaScript frontend
- Python Flask backend
- MySQL database
- Nginx reverse proxy

## Run

```bash
docker compose up --build
```

Open:

```text
http://localhost:8080
```

## Services

- `nginx`: public entrypoint on port `8080`
- `app`: Flask API and frontend server on port `5000` inside Docker
- `mysql`: MySQL 8 database with a persistent Docker volume

## API

- `POST /api/register`
- `POST /api/login`
- `POST /api/logout`
- `GET /api/me`
- `GET /api/health`
