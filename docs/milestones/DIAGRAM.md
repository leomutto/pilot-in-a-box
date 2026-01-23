
```
docs/DIAGRAM.md
```

Incluye:

- Arquitectura general  
- Arquitectura backend  
- Flujo de datos  
- Secuencia MASS Request  
- Secuencia BioCore (objetivo Pilot‑in‑a‑Box)  
- Pipeline de ingesta  
- Observabilidad (OTEL)  
- Audit trail  

Todo está alineado con MASS Simple y con la visión del Pilot‑in‑a‑Box.

---

# 📄 **DIAGRAM.md**  
*Diagramas ASCII de arquitectura, flujo y secuencia*

---

# # 1. Arquitectura General del Sistema

```
                   ┌──────────────────────────┐
                   │        Frontend          │
                   │        Next.js           │
                   │  (Dashboard Profesional) │
                   └─────────────┬────────────┘
                                 │
                                 ▼
                     ┌──────────────────────┐
                     │      FastAPI         │
                     │   (MASS Simple API)  │
                     └─────────────┬────────┘
                                   │
         ┌─────────────────────────┼──────────────────────────┐
         ▼                         ▼                          ▼
┌────────────────┐     ┌────────────────────┐     ┌──────────────────────┐
│  Services       │     │   Observabilidad   │     │      BioCore         │
│ (auth, mass)    │     │   OpenTelemetry    │     │   (Caja Negra)       │
└────────────────┘     └────────────────────┘     └──────────────────────┘
         │                         │                          │
         ▼                         │                          │
┌────────────────┐                │                          │
│   SQLAlchemy    │                │                          │
└────────────────┘                │                          │
         │                         │                          │
         ▼                         ▼                          ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                                Postgres                                  │
└──────────────────────────────────────────────────────────────────────────┘
```

---

# # 2. Arquitectura Interna del Backend

```
backend/
│
├── api/
│   ├── routes/
│   │   ├── auth.py
│   │   └── mass.py
│   └── schemas/
│
├── services/
│   ├── auth_service.py
│   └── mass_service.py
│
├── models/
│   ├── user.py
│   └── mass.py
│
├── schemas/
│   ├── user.py
│   └── mass.py
│
├── core/
│   ├── config.py
│   ├── security.py
│   └── validators/
│
├── db/
│   ├── session.py
│   └── base.py
│
└── migrations/
```

---

# # 3. Flujo de Datos (End-to-End)

```
Usuario
   │
   ▼
Frontend (Next.js)
   │  HTTP + JWT
   ▼
FastAPI (routes)
   │  valida schemas
   ▼
Services (lógica)
   │
   ▼
SQLAlchemy (ORM)
   │
   ▼
Postgres (persistencia)
   │
   ▼
Respuesta → Frontend → Usuario
```

---

# # 4. Secuencia: MASS Request (Actual)

```
Usuario
   │
   ▼
Frontend
   │  POST /mass
   ▼
FastAPI (mass.py)
   │  valida payload
   ▼
mass_service.py
   │  lógica de negocio
   ▼
SQLAlchemy
   │  inserta / consulta
   ▼
Postgres
   │
   ▼
FastAPI → Frontend → Usuario
```

---

# # 5. Secuencia: Integración BioCore (Objetivo Pilot‑in‑a‑Box)

```
Usuario
   │
   ▼
Frontend (Dashboard)
   │  GET /recommendations
   ▼
FastAPI (mass.py)
   │
   ▼
mass_service.py
   │
   │  Llama a BioCore:
   │  POST http://biocore/recommend
   ▼
BioCore (Caja Negra)
   │  procesa
   ▼
Respuesta BioCore
   │
   ▼
mass_service.py
   │  agrega metadata + audit trail
   ▼
FastAPI
   │
   ▼
Frontend → Usuario
```

---

# # 6. Pipeline de Ingesta (CSV/Parquet)

```
Archivo CSV/Parquet
        │
        ▼
Validación de Schema (validators/)
        │
        ▼
Normalización
        │
        ▼
SQLAlchemy (bulk insert)
        │
        ▼
Postgres
        │
        ▼
Audit Trail (pendiente)
```

---

# # 7. Observabilidad (OpenTelemetry)

```
Request Usuario
       │
       ▼
┌──────────────────────────────────────────────┐
│ FastAPI Instrumentado (OTEL Middleware)      │
│  - trace_id                                  │
│  - span_id                                   │
│  - métricas                                  │
│  - logs estructurados                        │
└──────────────────────────────────────────────┘
       │
       ▼
Collector OTLP (local o remoto)
       │
       ▼
Backend de Observabilidad (Grafana/Tempo/Prometheus)
```

---

# # 8. Audit Trail (Objetivo Pilot‑in‑a‑Box)

```
Operación (ej: MASS Request)
        │
        ▼
Captura de:
  - timestamp
  - usuario
  - inputs
  - outputs
  - versión dataset
  - versión BioCore
  - commit hash
  - trace_id/span_id
        │
        ▼
Persistencia en Postgres
        │
        ▼
Panel de Auditoría (Dashboard)
```

---

# # 9. Diagrama de Secuencia Completo (Pilot‑in‑a‑Box)

```
Usuario
   │
   ▼
Frontend
   │───────────────► FastAPI
   │                 │
   │                 ▼
   │           mass_service
   │                 │
   │                 │───────────────► BioCore (/recommend)
   │                 │                │
   │                 │                ▼
   │                 │           Respuesta BioCore
   │                 │◄───────────────│
   │                 │
   │                 ▼
   │           Audit Trail
   │                 │
   │                 ▼
   │───────────────◄│
   ▼
Usuario (Dashboard)
```

---
