# PizzaDeliveryApi
A learning-focused FastAPI repository built around a simple Pizza Delivery API. This project is designed to learn FastAPI and SQLModel by reading [official documentation](https://fastapi.tiangolo.com/learn/) and applying concepts step by step in a real-world CRUD API.

## Links
- [FastApi Doc](https://fastapi.tiangolo.com/learn/)
  - Configure the app entrypoint in pyproject.toml
  - Usage of FastAPI CLI
  - 

## Commands and Findings
- .venv\Scripts\activate  ==> activate my virtual environment
- fastapi dev app/main.py  ==> to  Run app in dev Mode
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


## 🎯 Learning Goals

* Understand **FastAPI fundamentals**
* Learn **SQLModel** (Pydantic + SQLAlchemy together)
* Build a **clean REST API**
* Learn **dependency injection**
* Practice **database modeling & relationships**
* Read and apply **official docs**, not magic code

---

## 🍕 Why a Pizza Delivery API?

Because it’s:

* Simple but realistic
* Has **real entities** (Pizza, Order, Customer)
* Covers **CRUD**, relationships, and business logic
* Easy to extend later **(auth, payments, async, etc.)**

---

## 🧠 What You’ll Learn (Step by Step)

### 1️⃣ FastAPI Basics

* Path operations (`GET`, `POST`, `PUT`, `DELETE`)
* Request & response models
* Automatic OpenAPI docs (`/docs`)
* Validation with Pydantic

### 2️⃣ SQLModel Basics

* Defining models
* Table vs schema models
* SQLite for fast iteration
* Sessions and engine
* Relationships (Order ↔ Pizza)

### 3️⃣ API Design

* CRUD endpoints
* Clear route structure
* Separation of concerns
* Error handling



## 🗂️ Suggested Repo Structure

```
fastapi-sqlmodel-pizza-delivery/
│
├── app/
│   ├── main.py          # FastAPI app entry point
|   ├── __init__.py      # ← Empty file, makes 'app' as package
│   ├── db.py            # Engine & session
│   ├── models/          # SQLModel models
│   ├── schemas/         # Request/response schemas ie. CustomerPublic
│   ├── services/        # Database operations and combine table model and data model i.e CustomerService
│   ├── routes/
│   │   ├── pizzas.py
│   │   ├── orders.py
│   │   └── customers.py
│
├── README.md
├── requirements.txt
└── pizza.db             # SQLite database
```

---



## 🧭 How to Learn with This Repo

1. **Read FastAPI docs**
2. Implement *one endpoint*
3. Test it in `/docs`
4. Read SQLModel docs
5. Improve the model
6. Repeat 🚀

No rushing. No copy-paste hell.

---

## 🖼️ Mental Model (What’s Happening)

Request → FastAPI → Validation → SQLModel → Database → Response

---

## 🚀 Next Natural Extensions

Once you’re comfortable:

* Authentication (JWT)
* Async database
* Alembic migrations
* Pagination & filtering
* Docker**

---

