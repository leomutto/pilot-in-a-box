
# 📄 **ARCHITECTURE.md**  
*Arquitectura técnica de MASS Simple y lineamientos para evolución hacia Pilot‑in‑a‑Box*

---

# # 1. Visión General

MASS Simple es un backend FastAPI modular, reproducible y orientado a convertirse en la base del **Pilot‑in‑a‑Box**: un sistema read‑only, auditable y listo para integrarse con BioCore y con un dashboard profesional.

La arquitectura actual prioriza:

- **Simplicidad**  
- **Reproducibilidad**  
- **Aislamiento de responsabilidades**  
- **Escalabilidad futura**  
- **Compatibilidad con estándares enterprise**  

Este documento describe la arquitectura actual y los lineamientos para su evolución.

---

# # 2. Componentes Principales

```
MASS Simple
│
├── Backend (FastAPI)
│   ├── API Layer (routes)
│   ├── Services Layer
│   ├── Models (SQLAlchemy)
│   ├── Schemas (Pydantic)
│   ├── Core (config, security, validators)
│   ├── DB (session, base)
│   ├── Migrations (Alembic)
│   └── Tests
│
├── Database (Postgres)
│
└── Infrastructure
    ├── Docker Compose
    ├── Environment Variables
    └── Future: Helm Chart (K8s)
```

---

# # 3. Backend Architecture (FastAPI)

El backend sigue una arquitectura **clean modular**, separando:

### ✔ **API Layer**
Ubicada en `api/routes/`.

Responsabilidades:
- Definir endpoints
- Validar entrada vía schemas
- Delegar lógica a servicios
- Manejar códigos HTTP

### ✔ **Services Layer**
Ubicada en `services/`.

Responsabilidades:
- Lógica de negocio
- Orquestación de modelos
- Validaciones adicionales
- Manejo de errores de dominio

Ejemplo:  
- `auth_service.py`  
- `mass_service.py` (pendiente)

### ✔ **Models (SQLAlchemy)**
Ubicados en `models/`.

Responsabilidades:
- Definir tablas
- Relaciones
- Constraints

### ✔ **Schemas (Pydantic)**
Ubicados en `schemas/`.

Responsabilidades:
- Validación de entrada/salida
- Serialización
- Tipado estricto

### ✔ **Core**
Ubicado en `core/`.

Incluye:
- `config.py` → carga de variables de entorno  
- `security.py` → JWT, hashing, autenticación  
- `validators/` → validación de payloads MASS  

### ✔ **DB Layer**
Ubicada en `db/`.

Incluye:
- `session.py` → SessionLocal  
- `base.py` → Base declarativa  
- Alembic para migraciones  

---

# # 4. Flujo de Datos

### 1. Request del usuario  
→ pasa por autenticación (JWT + HTTPBearer)

### 2. API Layer  
→ valida entrada con schemas  
→ delega a servicios

### 3. Services Layer  
→ ejecuta lógica  
→ interactúa con modelos  
→ aplica validaciones adicionales

### 4. DB Layer  
→ persiste o consulta datos

### 5. API Layer  
→ serializa respuesta  
→ retorna JSON

---

# # 5. Seguridad

### Estado actual
- JWT funcional  
- OAuth2PasswordBearer aún presente  
- HTTPBearer pendiente  
- Roles mínimos no implementados  
- CORS no configurado  
- Rate limiting no implementado  

### Estado objetivo
- Autenticación: **HTTPBearer + JWT**  
- Autorización: **roles (admin/viewer)**  
- Secrets: **solo por env vars**  
- CORS: **restrictivo**  
- Rate limiting: **nivel API Gateway o middleware**  

---

# # 6. Pipeline de Datos MASS

### Estado actual
- Ingesta parcial  
- Validación incompleta  
- Normalización no documentada  
- Tests mínimos  

### Estado objetivo
- Validación estricta (schemas + validators)  
- Normalización reproducible  
- Versionado de datasets  
- Manejo de errores estandarizado  
- Tests completos  

---

# # 7. Observabilidad (Objetivo Pilot‑in‑a‑Box)

### Estado actual
No implementado.

### Estado objetivo
- OpenTelemetry (traces + metrics + logs)  
- Propagación de contexto  
- Logs estructurados (JSON)  
- Collector local  
- Dashboards base (Grafana opcional)  

---

# # 8. Audit Trail (Objetivo Pilot‑in‑a‑Box)

### Estado actual
No implementado.

### Estado objetivo
Registrar por cada operación:
- timestamp  
- inputs  
- outputs  
- versión dataset  
- versión BioCore  
- commit hash  
- trace_id/span_id  

Con:
- Panel de auditoría  
- Export CSV/PDF  

---

# # 9. Integración BioCore

### Estado actual
No implementado.

### Estado objetivo
Cliente robusto:
- Timeouts  
- Retries exponenciales  
- Circuit breaker  
- Cache control  

Endpoints esperados:
- `/recommend`  
- `/health`  
- `/version`  

Dashboard debe mostrar:
- recomendaciones  
- impacto estimado  
- explicación high-level  

---

# # 10. Frontend (Next.js)

### Estado actual
No existe.

### Estado objetivo
Dashboard profesional con:
- KPIs  
- Tendencias  
- Before/after  
- Filtros  
- Export CSV/PDF  
- Recomendaciones BioCore  

---

# # 11. Infraestructura

### Docker Compose (actual)
- Backend  
- Postgres  
- Reproducible  
- Determinístico  

### Helm Chart (objetivo)
- Single namespace  
- Values por entorno  
- TLS/HTTPS  
- Password-protection  
- Script de actualización  
- Notas de rollback  

---

# # 12. Roadmap Arquitectónico

1. **Cerrar backend (seguridad + validación + servicios)**  
2. **Construir dashboard Next.js**  
3. **Implementar M&V**  
4. **Agregar observabilidad**  
5. **Agregar audit trail**  
6. **Integrar BioCore**  
7. **Crear Helm chart + deploy cloud**  

---

# # 13. Conclusión

La arquitectura de MASS Simple es sólida, limpia y lista para escalar.  
El backend ya está estable y reproducible; ahora el foco es:

- seguridad  
- pipeline de datos  
- dashboard  
- M&V  
- observabilidad  
- audit trail  
- BioCore  
- deploy cloud  

Con estos elementos, MASS Simple se convierte en un **Pilot‑in‑a‑Box real**, apto para PoCs con hyperscalers.

---
