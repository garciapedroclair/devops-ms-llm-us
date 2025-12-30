# DevOps Microservice: FastAPI + PostgreSQL + React

This project is a simple microservice architecture:

- **Backend**: FastAPI  
- **Frontend**: React + Vite  
- **Database**: PostgreSQL  
- **Dockerized**: all services run with `docker-compose`

---

## Prerequisites
- Docker & Docker Compose installed   

---

## 1️⃣ Clone the repository

```bash
git clone <repo-url>
cd devops-ms-llm-us
```

---

## 2️⃣ Environment variables

Create `.env` files for backend and frontend:

### Backend (`server/.env`)

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=dev_db
POSTGRES_PORT=5432
```

### Frontend (`client/.env`)

```env
VITE_API_URL=http://localhost:8000
```

---

## 3️⃣ Build and start Docker containers

From the project root:

```bash
docker-compose up --build
```

- Backend: http://localhost:8000  
- Frontend: http://localhost:3000  

---

