# FastShip
A learning-focused FastAPI repository built around a simple Pizza Delivery API. This project is designed to learn FastAPI and SQLModel by reading [official documentation](https://fastapi.tiangolo.com/learn/) and applying concepts step by step in a real-world CRUD API.
[based on](https://github.com/fastapi/full-stack-fastapi-template)
# Docker
- Starting
  - Open Docker Desktop
  - docker compose up --build 
  - 
## Links
- [FastApi Doc](https://fastapi.tiangolo.com/learn/)
  - Configure the app entrypoint in pyproject.toml
  - Usage of FastAPI CLI

## Commands and Findings
- .venv\Scripts\activate  ==> activate my virtual environment
- fastapi dev  ==> to  Run app in dev Mode
- uv run pytest tests/ . -v ==> Run all py test cmd
- uv run ruff check . --fix  ==> ruff must be installed
- uv pip freeze > requirements.txt ==>  in that file you see all used package
- uv export --format requirements-txt --no-hashes > requirements.txt ==>  to sync with uv add package 
- ruff check . ==> Check or lint the  code  to find code spelling
- docker build --tag ghis . ===> creat eimage named ghis
- docker run -d -p 8000:8000 youimagename ==>  run the image
- docker-compose up --build ==>   Run  Docker with all custom services
- 
## External packages
- prometheus-fastapi-instrumentator:
  - prometheus for fastapi
  - Instrumentator().instrument(app).expose(app): provide endpoint /metrics
 


# Features
- Monitoring mit Prometheus & Grafana 
  - FastAPI Service monitoren
  - Metric over Exporters
  - Libraries
    - prometheus-fastapi-instrumentator: 


 # Security
 - Oauth2
   - A protocol

