# 📘 **README.md — Pilot in a Box (MASS Simple)**

## 🚀 Overview

**Pilot in a Box — MASS Simple** es una versión minimalista y completamente reconstruida del backend MASS, diseñada para servir como base limpia, reproducible y extensible para futuros desarrollos.

Este proyecto **NO implementa MASS Enterprise v1.1**, ni pipelines de normalización, ni validadores complejos.  
En su lugar, ofrece:

- Un backend FastAPI minimalista  
- Un modelo único: `MassRequest`  
- Persistencia con SQLAlchemy + Alembic  
- Infraestructura reproducible con Docker Compose  
- Un punto de partida sólido para construir MASS simple paso a paso  

Este repositorio fue reseteado y limpiado para eliminar drift, código legacy y migraciones antiguas.

---

## 🏗️ Arquitectura del Proyecto

```
pilot-in-a-box/
│
├── backend/
│   ├── db/
│   │   ├── base.py              # Declarative Base
│   │   ├── session.py           # SessionLocal + engine
│   │   └── __init__.py
│   │
│   ├── models/
│   │   ├── mass.py              # Modelo MassRequest
│   │   └── __init__.py
│   │
│   ├── migrations/
│   │   ├── env.py               # Configuración Alembic
│   │   └── versions/
│   │       └── 1facca6dc8e8_create_mass_requests_table.py
│   │
│   ├── services/
│   │   └── mass_service.py      # Lógica de negocio MASS simple
│   │
│   ├── core/
│   │   └── validators/
│   │       └── mass_validator.py
│   │
│   ├── main.py                  # Punto de entrada FastAPI
│   ├── Dockerfile
│   └── .gitignore
│
├── frontend/                    # (Pendiente de actualización)
│
├── docker-compose.yml
└── README.md
```

---

## 📡 Endpoints (MASS Simple)

Los endpoints se encuentran en desarrollo.  
El objetivo es implementar:

### `POST /mass-requests/`
Crea un nuevo request MASS simple.

### `GET /mass-requests/{id}`
Obtiene un request por ID.

### `GET /mass-requests/`
Lista requests almacenados.

### `DELETE /mass-requests/{id}`
Elimina un request (soft delete opcional).

### `PATCH /mass-requests/{id}/status`
Actualiza el estado del request.

---

## 🗄️ Modelo Actual

### `MassRequest`

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
docker compose up --build
```

Esto inicia:

- Backend FastAPI en `http://localhost:8000`
- Base de datos Postgres en `localhost:5432`

### 3. Acceder a Swagger

```
http://localhost:8000/docs
```

---

## 🧪 Estado Actual del Proyecto

- Backend MASS simple reconstruido desde cero  
- Migración inicial aplicada  
- Base de datos limpia y sincronizada  
- Código legacy eliminado  
- `.gitignore` actualizado  
- Estructura estable y sin drift  

---

## 📦 Tecnologías Utilizadas

- **FastAPI**
- **SQLAlchemy**
- **Alembic**
- **Pydantic**
- **Docker & Docker Compose**
- **Python 3.11**

---

## 🧭 Roadmap MASS Simple

- [ ] Implementar POST `/mass-requests/`
- [ ] Implementar GET `/mass-requests/{id}`
- [ ] Implementar GET `/mass-requests/`
- [ ] Implementar DELETE `/mass-requests/{id}`
- [ ] Implementar actualización de estado
- [ ] Añadir pruebas unitarias
- [ ] Añadir autenticación opcional
- [ ] Integrar frontend minimalista

---

## 👤 Autor

**Leonardo Mutto**  
Arquitectura limpia, reproducibilidad y diseño de pipelines minimalistas.

---
