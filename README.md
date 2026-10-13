# QuantaLab — Quantum Learning & Simulation Platform

QuantaLab is an open-source educational platform designed to teach quantum computing concepts and provide a sandboxed environment for executing quantum circuits.

## Tech Stack
- **Backend**: Python, FastAPI, SQLAlchemy
- **Frontend**: React, Node.js
- **Database**: PostgreSQL
- **Caching & Queues**: Redis, Celery
- **Containerization**: Docker, Docker Compose
- **Quantum SDKs**: Qiskit, Cirq, PennyLane

## Prerequisites
- Python 3.11+
- Node.js 20+
- Docker & Docker Compose
- PostgreSQL 16
- Redis 7

## Quick Start
1. **Clone the repo**
   ```bash
   git clone https://github.com/EgreenQuanta/QuantaLab.git
   cd QuantaLab
   ```
2. **Start Services**
   ```bash
   docker-compose up -d
   ```
3. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   alembic upgrade head
   python scripts/seed_db.py
   ```
4. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
5. **Access**
   Open `http://localhost:5173` in your browser.

## Architecture Overview
```mermaid
flowchart TD
    Client[Browser Client] <-->|HTTP/WS| Nginx[Nginx Proxy]
    Nginx <--> FastAPI[FastAPI Backend]
    FastAPI <--> Postgres[(PostgreSQL)]
    FastAPI <--> Redis[(Redis)]
    Redis <--> Celery[Celery Workers]
    Celery <--> DockerSandbox[Docker Sandbox (Quantum SDKs)]
```

## Environment Variables Reference
Please see `.env.example` in the backend and frontend directories for required environment variables.
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`
- `SECRET_KEY`

## Deployment
See the `deployment/` directory for systemd services, nginx configurations, and Dockerfiles for production deployment.

## Contributing
We welcome contributions! Please follow our standard fork-and-pull-request workflow. Ensure all tests pass before submitting a PR.

## License
MIT License (Placeholder)

---
**Team:** Egreen Quanta
