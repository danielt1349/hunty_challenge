# REST API with Python, FastAPI, Pydantic, SQLAlchemy and Docker

### Instructions:

- Run docker-compose to enable database engine
- docker exec -it postgres bash: 
  - psql -U postgres -d fastapi, 
  - CREATE DATABASE fastapi, 
  - \c fastapi
  - CREATE EXTENSION IF NOT EXISTS "uuid-ossp"
- Run project requirements inside virtualenv (python 3.6)
- Run migrations: 
  - alembic upgrade head
  - alembic revision --autogenerate -m "New Migration"
- Run project
- Api-doc: http://localhost:8000/docs#

### Extra:
Depending of the system configurations you could be need set
this environment vars -> LANG=en_US.utf-8;LC_ALL=en_US.utf-8
