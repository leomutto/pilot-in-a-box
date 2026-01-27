Perfecto, Leonardo. Documento recibido.

Aquí tenés **`ARCHITECTURE.md` completamente actualizado**, alineado con el estado REAL del proyecto después de la sesión de hoy, incluyendo:

- MASS Simple + MASS Enterprise conviviendo  
- Normalizadores separados  
- Nuevo flujo de datos  
- Nuevos endpoints  
- Nueva estructura de carpetas  
- Roadmap ajustado  
- Arquitectura lista para Pilot‑in‑a‑Box  

Listo para copiar y pegar.

---

# 📄 **ARCHITECTURE.md**  
*Arquitectura técnica de MASS Simple + MASS Enterprise y lineamientos hacia Pilot‑in‑a‑Box*

---

# 1. Visión General

El backend MASS ahora implementa **dos pipelines coexistentes**:

- **MASS Simple** → payload libre, normalización flexible, ideal para ingesta rápida  
- **MASS Enterprise v1.1 (parcial)** → contrato formal, trazabilidad completa, estructura estandarizada  

Ambos conviven en un backend FastAPI modular, reproducible y preparado para evolucionar hacia el **Pilot‑in‑a‑Box**, un sistema auditable, observable y listo para integrarse con BioCore.

La arquitectura prioriza:

- Simplicidad  
- Reproducibilidad  
- Aislamiento de responsabilidades  
- Escalabilidad  
- Compatibilidad con estándares enterprise  

---

# 2. Componentes Principales

```
MASS Backend
│
├── API Layer (FastAPI)
│   ├── MASS Simple → POST /mass
│   ├── MASS Enterprise → POST /mass/generate
│   └── GET /mass/{id}
│
├── Services
│   ├── Normalización Simple
│   ├── Normalización Enterprise
│   └── Autenticación
│
├── Models (SQLAlchemy)
│   └── MassRequest
│
├── Schemas (Pydantic)
│   ├── MassSimplePayload
│   ├── MassPayload (Enterprise)
│   └── MassRequestBase
│
├── Core
│   ├── Config
│   ├── Security (JWT)
│   └── Validators (futuro)
│
├── DB Layer
│   ├── Session
│   ├── Base
│   └── Alembic
│
└── Infraestructura
    ├── Docker Compose
    └── Variables de entorno
```

---

# 3. Backend Architecture (FastAPI)

El backend sigue una arquitectura **clean modular**, con capas bien definidas.

## ✔ API Layer (`routes/`)
Responsabilidades:
- Definir endpoints
- Validar entrada con schemas
- Delegar a servicios
- Manejar errores HTTP

Endpoints actuales:

| Endpoint | Tipo | Descripción |
|---------|------|-------------|
| `POST /mass` | MASS Simple | Ingesta flexible con normalización automática |
| `POST /mass/generate` | MASS Enterprise | Ingesta formal con contrato v1.1 |
| `GET /mass/{id}` | Común | Recuperación de requests |

---

## ✔ Services Layer (`services/`)
Responsabilidades:
- Lógica de negocio
- Normalización
- Validaciones adicionales
- Orquestación de modelos

Servicios actuales:

- `mass_normalizer_simple.py`
- `mass_normalizer.py` (Enterprise)
- `auth_service.py`

---

## ✔ Models (`models/`)
Modelo único:

### `MassRequest`
- `id`
- `user_id`
- `schema_version`
- `correlation_id`
- `idempotency_key`
- `payload_json`
- `created_at`

---

## ✔ Schemas (`schemas/`)

### MASS Simple
```python
class MassSimplePayload:
    payload: Dict[str, Any]
```

### MASS Enterprise
```python
class MassPayload:
    schema_version
    correlation_id
    trace
    request
    payload
```

### Base de lectura
```python
class MassRequestBase
```

---

## ✔ Core (`core/`)
Incluye:

- Configuración
- Seguridad (JWT)
- Validadores futuros
- Middlewares futuros

---

## ✔ DB Layer (`db/`)
- `session.py` → SessionLocal  
- `base.py` → Declarative Base  
- Alembic para migraciones  

---

# 4. Flujo de Datos

## MASS Simple (`POST /mass`)

```
Cliente
 → API Layer (MassSimplePayload)
 → Normalizador Simple
 → Generación automática de metadata Enterprise
 → Persistencia en MassRequest
 → Respuesta con IDs y payload normalizado
```

## MASS Enterprise (`POST /mass/generate`)

```
Cliente
 → API Layer (MassPayload)
 → Normalizador Enterprise
 → Persistencia en MassRequest
 → Respuesta con metadata Enterprise
```

## Recuperación (`GET /mass/{id}`)

```
Cliente → API → DB → JSON
```

---

# 5. Seguridad

### Estado actual
- JWT funcional
- Autenticación obligatoria
- Roles no implementados
- CORS no configurado

### Objetivo
- HTTPBearer + JWT
- Roles (admin/viewer)
- CORS restrictivo
- Rate limiting (middleware o API Gateway)

---

# 6. Pipeline MASS

### Estado actual
- MASS Simple completo
- MASS Enterprise v1.1 parcialmente implementado
- Normalizadores separados
- Persistencia unificada

### Objetivo
- Validación estricta Enterprise
- Versionado de payloads
- Manejo de errores estandarizado
- Tests completos

---

# 7. Observabilidad (Objetivo Pilot‑in‑a‑Box)

### Estado actual
No implementado.

### Objetivo
- OpenTelemetry
- Logs estructurados
- Métricas
- Dashboards (Grafana opcional)

---

# 8. Audit Trail

### Estado actual
No implementado.

### Objetivo
Registrar:
- Inputs
- Outputs
- Timestamps
- trace_id/span_id
- Versión de dataset
- Versión de BioCore
- Commit hash

---

# 9. Integración BioCore

### Estado actual
No implementado.

### Objetivo
Cliente robusto:
- Retries
- Timeouts
- Circuit breaker
- Cache control

Endpoints esperados:
- `/recommend`
- `/health`
- `/version`

---

# 10. Frontend (Next.js)

### Estado actual
No existe.

### Objetivo
Dashboard con:
- KPIs
- Tendencias
- Before/after
- Export CSV/PDF
- Recomendaciones BioCore

---

# 11. Infraestructura

### Docker Compose (actual)
- Backend
- Postgres
- Reproducible

### Helm Chart (objetivo)
- TLS
- Password-protection
- Values por entorno
- Rollbacks

---

# 12. Roadmap Arquitectónico

1. Cerrar backend (validación + seguridad + servicios)
2. Construir dashboard Next.js
3. Implementar M&V
4. Agregar observabilidad
5. Agregar audit trail
6. Integrar BioCore
7. Crear Helm chart + deploy cloud

---

# 13. Conclusión

La arquitectura MASS actual es sólida, limpia y preparada para escalar hacia un **Pilot‑in‑a‑Box real**, con MASS Simple y MASS Enterprise conviviendo sin conflicto y una base técnica lista para observabilidad, M&V, audit trail y BioCore.

---
