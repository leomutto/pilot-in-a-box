Perfecto, Leonardo. Acá tenés **`DIAGRAM.md` completamente actualizado**, alineado con:

- MASS Simple  
- MASS Enterprise  
- Normalizadores separados  
- Nuevo flujo de datos  
- Nueva estructura de carpetas  
- Objetivo Pilot‑in‑a‑Box  

Listo para copiar y pegar.

---

# 📄 **DIAGRAM.md**  
*Diagramas ASCII de arquitectura, flujo, secuencia y visión Pilot‑in‑a‑Box*

---

# 1. Arquitectura General del Sistema

```
                   ┌──────────────────────────┐
                   │        Frontend          │
                   │         Next.js          │
                   │  (Dashboard Profesional) │
                   └─────────────┬────────────┘
                                 │
                                 ▼
                     ┌────────────────────────┐
                     │        FastAPI         │
                     │  MASS Simple + Ent.    │
                     └─────────────┬──────────┘
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

# 2. Arquitectura Interna del Backend

```
backend/
│
├── api/
│   ├── routes/
│   │   ├── auth.py
│   │   └── mass.py
│   └── schemas/
│       ├── mass_simple.py
│       ├── mass_payload.py
│       └── mass.py
│
├── services/
│   ├── mass_normalizer_simple.py
│   ├── mass_normalizer.py
│   └── auth_service.py
│
├── models/
│   ├── user.py
│   └── mass_request.py
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

# 3. Flujo de Datos (End‑to‑End)

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
Services (normalización + lógica)
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

# 4. Secuencia: MASS Simple (`POST /mass`)

```
Usuario
   │
   ▼
Frontend
   │  POST /mass
   ▼
FastAPI (MassSimplePayload)
   │
   ▼
normalize_mass_payload_simple
   │
   ▼
Generación automática:
  - correlation_id
  - idempotency_key
  - schema_version simple
   │
   ▼
SQLAlchemy → Postgres
   │
   ▼
FastAPI → Frontend → Usuario
```

---

# 5. Secuencia: MASS Enterprise (`POST /mass/generate`)

```
Usuario
   │
   ▼
Frontend
   │  POST /mass/generate
   ▼
FastAPI (MassPayload)
   │
   ▼
normalize_mass_payload (Enterprise)
   │
   ▼
SQLAlchemy → Postgres
   │
   ▼
FastAPI → Frontend → Usuario
```

---

# 6. Pipeline de Ingesta (CSV/Parquet) — Objetivo

```
Archivo CSV/Parquet
        │
        ▼
Validación de Schema (validators/)
        │
        ▼
Normalización (simple o enterprise)
        │
        ▼
SQLAlchemy (bulk insert)
        │
        ▼
Postgres
        │
        ▼
Audit Trail (futuro)
```

---

# 7. Observabilidad (OpenTelemetry) — Objetivo Pilot‑in‑a‑Box

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
Backend Observabilidad (Grafana/Tempo/Prometheus)
```

---

# 8. Audit Trail — Objetivo Pilot‑in‑a‑Box

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

# 9. Secuencia Completa Pilot‑in‑a‑Box (con BioCore)

```
Usuario
   │
   ▼
Frontend (Dashboard)
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
