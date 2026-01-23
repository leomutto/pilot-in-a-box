# 📄 **PROJECT_MANAGEMENT.md**  
*Tablero Kanban + Backlog priorizado (EPIC → Feature → Task)*

---

# # 1. Kanban Board (Texto para GitHub Projects)

Este tablero está diseñado para ser replicado en GitHub Projects como columnas y tarjetas.

---

## 🟥 **TODO (Prioridad Alta)**

### Seguridad
- Implementar `HTTPBearer` en `auth.py`
- Habilitar modal de Authorize en Swagger
- Validar JWT en endpoints protegidos
- Crear roles mínimos (admin/viewer)
- Configurar CORS restrictivo

### Pipeline de Datos
- Completar validadores en `core/validators`
- Normalización de payloads MASS
- Manejo de errores estandarizado
- Versionado de datasets

### Servicios
- Crear `mass_service.py`
- Revisar `auth_service.py`
- Separar lógica de negocio de rutas

### Documentación
- Completar OpenAPI (modelos, ejemplos, respuestas)
- README del backend

---

## 🟧 **IN PROGRESS**
- Limpieza de módulos
- Tests de ingesta
- Tests de autenticación

---

## 🟨 **READY FOR REVIEW**
- Estructura backend estable  
- Docker Compose determinístico  
- Alembic funcionando  

---

## 🟦 **BLOCKED / WAITING**
- Esperando container BioCore  
- Definir baseline y supuestos  
- Esperando acceso a DNS/subdominio  

---

## 🟩 **DONE**
- Backend estable  
- DB conectada  
- `.env` corregido  
- Estructura de carpetas limpia  
- Repositorio sincronizado  
- Docker Compose funcionando  

---

# # 2. Backlog Priorizado (EPIC → Feature → Task)

Organizado por impacto, dependencias y alineación con Pilot‑in‑a‑Box.

---

# **EPIC 1 — Backend Hardening (MVP MASS Simple)**

## Feature 1.1 — Seguridad Completa
- Reemplazar OAuth2PasswordBearer por HTTPBearer  
- Habilitar modal de Authorize en Swagger  
- Validar JWT en cada endpoint  
- Crear roles mínimos (admin/viewer)  
- Configurar CORS restrictivo  
- Agregar rate limiting básico  

## Feature 1.2 — Validación y Sanitización de Datos
- Completar validadores en `core/validators`  
- Normalizar payloads MASS  
- Manejo de errores estandarizado  
- Versionado de datasets  

## Feature 1.3 — Servicios Desacoplados
- Crear `mass_service.py`  
- Revisar `auth_service.py`  
- Separar rutas de lógica de negocio  
- Crear capa de repositorios si es necesario  

## Feature 1.4 — Documentación OpenAPI
- Describir modelos  
- Describir respuestas  
- Agregar ejemplos  
- Documentar errores  

## Feature 1.5 — Tests
- Completar `test_ingestion_pipeline.py`  
- Agregar tests de autenticación  
- Agregar tests de MASS Requests  

---

# **EPIC 2 — Dashboard Profesional (Next.js)**

## Feature 2.1 — Setup de Frontend
- Crear proyecto Next.js  
- Configurar UI profesional neutra  
- Integrar autenticación con backend  

## Feature 2.2 — KPIs y Tendencias
- Endpoint KPIs  
- Componente de KPIs  
- Gráficos de tendencias  

## Feature 2.3 — Before/After
- Endpoint before/after  
- Vista comparativa  
- Filtros por período/sitio/cluster  

## Feature 2.4 — Export CSV
- Endpoint export CSV  
- Botón de exportación  
- Validación de filtros  

---

# **EPIC 3 — M&V (Measurement & Verification)**

## Feature 3.1 — Baseline
- Definir baseline configurable  
- Endpoint baseline  
- UI de baseline  

## Feature 3.2 — Supuestos
- Panel de supuestos  
- Validación de supuestos  
- Persistencia  

## Feature 3.3 — Comparación Before/After
- Endpoint comparación  
- UI de comparación  
- Cálculo cuantitativo  

## Feature 3.4 — Export PDF
- Generación PDF  
- Branding mínimo  
- Firma de versión  

---

# **EPIC 4 — Observabilidad + Audit Trail**

## Feature 4.1 — OpenTelemetry
- Instrumentar backend  
- Instrumentar frontend (web vitals)  
- Configurar collector local  
- Export OTLP  

## Feature 4.2 — Logs Estructurados
- Formato JSON  
- Correlación trace_id/span_id  
- Logging de errores  

## Feature 4.3 — Audit Trail Completo
- Registrar inputs/outputs  
- Registrar versión dataset  
- Registrar versión BioCore  
- Registrar commit hash  
- Panel de auditoría  

---

# **EPIC 5 — Integración BioCore**

## Feature 5.1 — Cliente BioCore
- Implementar cliente con retries exponenciales  
- Timeouts  
- Circuit breaker  
- Cache control  

## Feature 5.2 — Recomendaciones en Dashboard
- Endpoint recomendaciones  
- UI de recomendaciones  
- Logs de cada recomendación  

---

# **EPIC 6 — Deploy Cloud + Helm Chart**

## Feature 6.1 — Helm Chart
- Crear chart v0.1  
- Values por entorno  
- Pipeline de deploy  

## Feature 6.2 — HTTPS + Password Protection
- Configurar TLS  
- Configurar password-protection  
- Integrar con subdominio del cliente  

## Feature 6.3 — Scripts de Operación
- Script de actualización  
- Script de rollback  
- Documentación de despliegue  

---

