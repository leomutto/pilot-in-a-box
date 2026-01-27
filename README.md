Perfecto, Leonardo. Acá tenés **el README.md completamente actualizado**, alineado con:

- MASS Simple funcionando  
- MASS Enterprise funcionando  
- Normalizadores separados  
- Nuevos endpoints reales  
- Nueva arquitectura  
- Nuevo roadmap  
- Estado actual del backend  

Listo para copiar y pegar.

---

# 📘 **README.md — MASS Simple + MASS Enterprise (Pilot‑in‑a‑Box Foundation)**

## 🚀 Overview

Este repositorio contiene la base técnica del ecosistema MASS y del futuro **Pilot‑in‑a‑Box**.  
El backend fue reconstruido desde cero para ofrecer una arquitectura **limpia, reproducible y extensible**, eliminando drift, código legacy y migraciones obsoletas.

Actualmente implementa **dos pipelines MASS coexistentes**:

### ✔ MASS Simple  
- Payload libre  
- Normalización flexible  
- Ideal para ingesta rápida y pruebas  

### ✔ MASS Enterprise (v1.1 parcial)  
- Contrato formal  
- Trazabilidad completa  
- Estructura estandarizada  
- Normalización Enterprise  

Ambos conviven en un backend estable, modular y preparado para escalar hacia:

- Dashboard profesional (Next.js)  
- M&V (Measurement & Verification)  
- Observabilidad (OpenTelemetry)  
- Audit Trail  
- Integración BioCore  
- Deploy Cloud (Helm Chart)  

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
│   │       ├── mass_simple.py
│   │       ├── mass_payload.py
│   │       └── mass.py
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
│   │   ├── mass_request.py
│   │   ├── user.py
│   │   └── __init__.py
│   │
│   ├── schemas/
│   │   ├── mass_request.py
│   │   └── __init__.py
│   │
│   ├── services/
│   │   ├── mass_normalizer_simple.py
│   │   ├── mass_normalizer.py
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
├── frontend/                # (Pendiente — se implementará en Pilot‑in‑a‑Box)
│
├── docker-compose.yml
└── README.md
```

---

## 📡 Endpoints (Estado Actual)

### ✔ MASS Simple  
**`POST /mass`**  
- Recibe `{ "payload": {...} }`  
- Normaliza automáticamente  
- Genera metadata Enterprise  
- Persiste en `MassRequest`

### ✔ MASS Enterprise  
**`POST /mass/generate`**  
- Requiere contrato Enterprise v1.1  
- Normalización estricta  
- Persistencia con trazabilidad

### ✔ Recuperación  
**`GET /mass/{id}`**  
Devuelve un MASS request almacenado.

---

## 🗄️ Modelo Actual — `MassRequest`

Campos:

- `id` (int, PK)  
- `user_id`  
- `schema_version`  
- `correlation_id`  
- `idempotency_key`  
- `payload_json` (JSON normalizado)  
- `created_at` (datetime)  

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

- MASS Simple funcionando  
- MASS Enterprise funcionando  
- Normalizadores separados  
- Persistencia unificada  
- Autenticación JWT operativa  
- Alembic estable  
- Docker Compose determinístico  
- Arquitectura limpia y modular  
- Punto de restauración sólido  

---

## 📦 Tecnologías Utilizadas

- **FastAPI**  
- **SQLAlchemy**  
- **Alembic**  
- **Pydantic**  
- **Docker & Docker Compose**  
- **Python 3.11**  

---

## 🧭 Roadmap (MASS Simple + Enterprise → Pilot‑in‑a‑Box)

### 🔥 Fase 1 — Backend Hardening
- [ ] Validación estricta MASS Enterprise  
- [ ] Normalización Enterprise completa  
- [ ] Servicios desacoplados  
- [ ] Seguridad: HTTPBearer + JWT  
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

