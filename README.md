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

## 3️⃣ Build and start Docker containers from scratch

From the project root, build all images and start the containers:

```bash
# Build all images
docker-compose build

# Start containers (Postgres first, then API, then client)
docker-compose up -d postgres
docker-compose up -d api
docker-compose up -d client
```

**Note:** You can also run all containers at once with:

```bash
# Build all images and start in detached mode
docker-compose up --build -d
```

If you encounter problems, try stop and restart the containers:
```bash
docker-compose down
docker-compose up
```