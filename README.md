# LLM for User Stories - Analytical Dashboard

This project is an analytical dashboard designed to visualize research data on LLMs as a tool to help students with users stories. It is built using a modern microservice architecture, fully containerized for easy deployment.

## 🏗️ Architecture Stack
- **Frontend**: Next.js (React)
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL 16
- **Orchestration**: Docker Compose

---

## 📋 Prerequisites

Ensure you have the following installed:
- **Docker**: `v28.3.2` or higher
- **Docker Compose**: `v2.40.3` or higher
- **WSL2** (If running on Windows)

## 📂 Project Structure
```text
.
├── client/            # Next.js Frontend application
├── Data/              # Database configurations 
├── server/            # FastAPI Backend & Database configurations
├── docker-compose.yml # Project orchestration
└── README.md          # Project documentation
```
---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone <(...)/devops-ms-llm-us.git>
cd devops-ms-llm-us
```

### 2. Configure Environment Variables
Ensure you have a .env file inside the **server/** directory with the following variables:

```bash
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_db
DATABASE_URL=postgresql://your_user:your_password@postgres:5432/your_db
```

and a .env.local inside the **client/** directory with the following variable:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8001
```

### 3. Run with Docker Compose
From the project root, build and start the entire stack:
```bash
docker compose up -d --build
```

### 4. Access the Services
Once the containers are running, access:

* **Frontend Dashboard**: http://localhost:3001
* **API Documentation (Swagger)**: http://localhost:8001/docs
* **API Health Check**: http://localhost:8001/health

---

## 5. Install models
The application has a ollama container. Execute the following command to install the default model

```bash
docker exec -it devops-ms-llm-us-ollama-1 ollama pull phi:3-mini
```