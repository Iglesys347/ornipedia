# Ornipedia

Ornipedia is a bird encyclopedia: an image gallery of birds, browsable by species and sub-species, available in several languages.

The repository contains three parts:

| Folder | Content |
| --- | --- |
| [`api/`](api/) | REST API built with FastAPI, SQLAlchemy and PostgreSQL (migrations with Alembic) |
| [`front/`](front/) | Web application built with Vue 3, Vuetify and Pinia |
| [`deploy/`](deploy/) | Ansible playbooks to deploy the whole application (NGINX, Gunicorn, Certbot) |

## Run the project locally

### 1. Database

Start a PostgreSQL server, for instance with Docker:

```bash
docker run -d --name ornipedia-db -p 5432:5432 \
  -e POSTGRES_PASSWORD=mysecretpassword -e POSTGRES_DB=ornipedia postgres:16
```

### 2. API

```bash
cd api
python -m venv venv && source venv/bin/activate
pip install -r requirements/dev-requirements.txt
alembic upgrade head              # create the database schema
uvicorn src.main:app --reload     # API available on http://localhost:8000
```

The interactive API documentation is available on <http://localhost:8000/docs>. See [api/README.md](api/README.md) for the configuration.

### 3. Front

```bash
cd front
npm install
npm run dev                       # front available on http://localhost:3000
```

The URL of the API used by the front is configured by `VITE_API_URL` in [front/.env](front/.env) (`http://localhost:8000` by default).

> [!NOTE]
> For the front to be allowed to call the API from another origin, add its URL to the API `ALLOWED_ORIGINS` setting (e.g. `ORNIPEDIA_ALLOWED_ORIGINS=http://localhost:3000`).

## Deployment

See [deploy/README.md](deploy/README.md).

## License

[GPL-3.0](LICENSE)
