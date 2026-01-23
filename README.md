# 📘 **README.md — MASS Simple (Pilot‑in‑a‑Box Foundation)**

## 🚀 Overview

**MASS Simple** es el **MVP oficial** del ecosistema MASS y constituye la base técnica del futuro **Pilot‑in‑a‑Box** (PoC‑ready).  
Fue completamente reconstruido para ofrecer una arquitectura **limpia, reproducible y extensible**, eliminando drift, código legacy y migraciones obsoletas.

Este proyecto **NO implementa MASS Enterprise v1.1**, ni pipelines avanzados, ni validadores complejos.  
Su propósito es entregar un backend estable y minimalista sobre el cual construir:

- El **Pilot‑in‑a‑Box** (shadow mode, read‑only, con dashboard, M&V, BioCore, observabilidad)  
- MASS Enterprise en etapas posteriores  

### ✔ MASS Simple ofrece hoy:

- Backend **FastAPI** estable  
- Modelo único: `MassRequest`  
- Persistencia real con **SQLAlchemy + Alembic**  
- Infraestructura reproducible con **Docker Compose**  
- Arquitectura modular y preparada para escalar  
- Base sólida para implementar seguridad, validación, M&V, dashboard y BioCore  

---

## 🏗️ Arquitectura del Proyecto (Actualizada)

```
pilot-in-a-box/
│
├── backend/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── mass.py
│   │   │   └── __init__.py
│   │   └── schemas/
│   │       └── __init__.py
│   │
│   ├── app/
│   │   ├── main.py
│   │   └── __init__.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── validators/
│   │   └── __init__.py
│   │
│   ├── db/
│   │   ├── base.py
│   │   ├── session.py
│   │   └── __init__.py
│   │
│   ├── models/
│   │   ├── mass.py
│   │   ├── user.py
│   │   └── __init__.py
│   │
│   ├── schemas/
│   │   ├── mass.py
│   │   └── __init__.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   └── __init__.py
│   │
│   ├── migrations/
│   │   ├── env.py
│   │   └── versions/
│   │
│   ├── dependencies/
│   │   ├── db.py
│   │   ├── dependencies.py
│   │   └── __init__.py
│   │
│   ├── tests/
│   │   └── test_ingestion_pipeline.py
│   │
│   ├── Dockerfile
│   ├── alembic.ini
│   ├── requirements.txt
│   └── .gitignore
│
├── frontend/                # (Pendiente — se implementará en el Pilot‑in‑a‑Box)
│
├── docker-compose.yml
└── README.md
```

---

## 📡 Endpoints (Estado Actual)

Los endpoints están en desarrollo y evolucionarán hacia el MVP completo.

### `POST /mass-requests/`
Crea un nuevo request MASS.

### `GET /mass-requests/{id}`
Obtiene un request por ID.

### `GET /mass-requests/`
Lista requests almacenados.

### `DELETE /mass-requests/{id}`
Elimina un request.

### `PATCH /mass-requests/{id}/status`
Actualiza el estado del request.

---

## 🗄️ Modelo Actual — `MassRequest`

Campos:

- `id` (int, PK)  
- `payload` (JSON)  
- `status` (str: pending, processing, done)  
- `created_at` (datetime)  
- `updated_at` (datetime)  

---

## 🐳 Despliegue con Docker Compose

### 1. Clonar el repositorio

```bash
git clone https://github.com/leomutto/pilot-in-a-box.git
cd pilot-in-a-box
```

### 2. Levantar el entorno

```bash
docker compose up -d --build
```

Esto inicia:

- Backend FastAPI → `http://localhost:8000`
- Postgres → `localhost:5432`

### 3. Acceder a Swagger

```
http://localhost:8000/docs
```

---

## 🧪 Estado Actual del Proyecto

- Backend estable y reproducible  
- Conexión a Postgres funcionando  
- Alembic operativo  
- `.env` corregido y fuera del repo  
- Estructura limpia y coherente  
- Docker Compose determinístico  
- Código legacy eliminado  
- Punto de restauración estable  

---

## 📦 Tecnologías Utilizadas

- **FastAPI**  
- **SQLAlchemy**  
- **Alembic**  
- **Pydantic**  
- **Docker & Docker Compose**  
- **Python 3.11**  

---

## 🧭 Roadmap (MVP MASS Simple → Pilot‑in‑a‑Box)

### 🔥 Fase 1 — Cierre del Backend (MVP)
- [ ] Seguridad completa (HTTPBearer + JWT)
- [ ] Validación y sanitización de datos
- [ ] Servicios desacoplados
- [ ] Documentación OpenAPI
- [ ] Tests backend

### 🎨 Fase 2 — Dashboard (Next.js)
- [ ] Setup Next.js
- [ ] KPIs + tendencias
- [ ] Before/after
- [ ] Filtros
- [ ] Export CSV

### 📊 Fase 3 — M&V
- [ ] Baseline
- [ ] Supuestos
- [ ] Comparación cuantitativa
- [ ] Export PDF

### 🔍 Fase 4 — Observabilidad + Audit Trail
- [ ] OpenTelemetry
- [ ] Logs estructurados
- [ ] Audit trail completo

### 🧠 Fase 5 — Integración BioCore
- [ ] Cliente robusto (timeouts, retries, circuit breaker)
- [ ] Recomendaciones reales en dashboard

### ☁️ Fase 6 — Deploy Cloud + Helm Chart
- [ ] Helm chart v0.1
- [ ] HTTPS + password-protection
- [ ] Script de actualización

---

## 👤 Autor

**Leonardo Mutto**  
Arquitectura limpia, reproducibilidad y diseño de pipelines minimalistas.

---

# ✔️ README actualizado y alineado con el proyecto
