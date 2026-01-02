# 📘 **README.md — Pilot in a Box (MASS v1.1)**

## 🚀 Overview

**Pilot in a Box** es una implementación completa del flujo MASS Enterprise v1.1, diseñada para demostrar un pipeline de ingesta, validación, normalización y procesamiento de señales energéticas, térmicas, de cooling y workload en un entorno reproducible basado en Docker.

El proyecto incluye:

- **Backend FastAPI** alineado con MASS v1.1  
- **Frontend Next.js** para enviar requests MASS  
- **Pipeline de normalización** modular y extensible  
- **Validación estricta del contrato MASS**  
- **Infraestructura reproducible con Docker Compose**  

Este repositorio sirve como base para pilotos, PoCs y despliegues iniciales de MASS.

---

## 🏗️ Arquitectura del Proyecto

```
pilot-in-a-box/
│
├── backend/
│   ├── app/
│   │   ├── ingestion/
│   │   │   ├── normalizers/        # Normalizadores MASS v1.1
│   │   │   ├── validators/         # Validación del contrato MASS
│   │   │   ├── pipelines/          # Pipeline de ingesta
│   │   │   ├── storage/            # Modelos de persistencia
│   │   │   ├── utils/              # Utilidades (tracing, tracking)
│   │   │   ├── routers.py          # Endpoints de ingesta
│   │   │   ├── service.py          # Lógica de negocio
│   │   │   ├── schemas_request.py  # Modelo Pydantic MASS v1.1
│   │   ├── main.py                 # Punto de entrada FastAPI
│   ├── Dockerfile
│
├── frontend/
│   ├── app/
│   │   ├── ingestion/page.tsx      # UI para enviar requests MASS
│   ├── services/
│       ├── ingestionApi.ts         # Cliente HTTP hacia el backend
│   ├── Dockerfile
│
├── docker-compose.yml
└── README.md
```

---

## 📡 Endpoints Principales

### `POST /v1/json-request/validate`
Valida que el request cumpla con el contrato MASS v1.1.

### `POST /v1/json-request/normalize`
Normaliza el payload MASS aplicando:

- conversión de unidades  
- limpieza de strings  
- normalización de números  
- estandarización de timestamps  

### `POST /v1/json-request/save`
Guarda el request normalizado en la base de datos.

### `POST /v1/json-request/send`
Envía el request a la blackbox (motor de recomendación).

### `GET /v1/json-request/{id}`
Recupera un request previamente guardado.

### `GET /v1/json-request/{id}/logs`
Devuelve logs asociados al procesamiento.

---

## 🔄 Flujo MASS v1.1 Implementado

```
┌──────────────┐
│   validate   │  → Validación estricta del contrato MASS
└───────┬──────┘
        │
┌───────▼──────┐
│   normalize  │  → Limpieza, conversión y estandarización
└───────┬──────┘
        │
┌───────▼──────┐
│     save     │  → Persistencia en base de datos
└───────┬──────┘
        │
┌───────▼──────┐
│     send     │  → Envío a motor de recomendación
└──────────────┘
```

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
- Frontend Next.js en `http://localhost:3000`
- Base de datos (si aplica)

### 3. Acceder a Swagger

```
http://localhost:8000/docs
```

---

## 🧪 Probar el flujo MASS

### 1. Enviar un request desde el frontend

```
http://localhost:3000/ingestion
```

### 2. Probar desde Swagger

- `/validate`
- `/normalize`
- `/save`
- `/send`

### 3. Ver logs y requests guardados

```
GET /v1/json-request/{id}
GET /v1/json-request/{id}/logs
```

---

## 📦 Tecnologías Utilizadas

- **FastAPI**  
- **Pydantic**  
- **Next.js 14**  
- **TypeScript**  
- **Docker & Docker Compose**  
- **Python 3.11**  

---

## 🧭 Roadmap

- [ ] Implementar `/save` con persistencia completa  
- [ ] Implementar `/send` con integración real a blackbox  
- [ ] Añadir pruebas unitarias para normalizadores  
- [ ] Añadir pruebas de integración para el pipeline  
- [ ] Añadir métricas y observabilidad  
- [ ] Añadir autenticación opcional  

---

## 👤 Autor

**Leonardo Mutto**  
Ingeniero especializado en arquitectura limpia, reproducibilidad y pipelines de ingesta.

