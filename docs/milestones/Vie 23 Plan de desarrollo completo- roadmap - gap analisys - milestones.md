
- **ROADMAP REALISTA**  
- **Milestones corregidos**  
- **Gap Analysis visual (ASCII, legible para GitHub)**  
- **Plan de rescate para alinear MASS Simple con el Pilot‑in‑a‑Box original**

---

# 📌 **1. ROADMAP REALISTA (MASS Simple → Pilot‑in‑a‑Box)**

Este roadmap está diseñado para:

- Cerrar MASS Simple (MVP real)  
- Extenderlo hacia el Pilot‑in‑a‑Box original  
- Mantener deuda técnica en cero  
- Asegurar reproducibilidad y gobernanza  

### 🧭 **Fases**

---

## **Fase 1 — Cierre del Backend (Semana 1–2)**  
**Objetivo:** dejar MASS Simple sólido, seguro y listo para extender.

### Entregables:
- Autenticación completa (HTTPBearer + JWT + roles mínimos)  
- Validación y sanitización de datos  
- Servicios desacoplados (`mass_service.py`, `auth_service.py`)  
- Documentación OpenAPI final  
- Tests mínimos (auth + ingestion)  
- Pipeline de ingesta estable  

**Resultado:** backend listo para integrarse con frontend, BioCore y observabilidad.

---

## **Fase 2 — Dashboard Profesional (Semana 3–4)**  
**Objetivo:** entregar UI funcional para KPIs, before/after y navegación.

### Entregables:
- Next.js + UI profesional neutra  
- KPIs iniciales  
- Vista before/after  
- Filtros por período/sitio/cluster  
- Export CSV básico  

**Resultado:** primera demo visible para stakeholders.

---

## **Fase 3 — M&V (Measurement & Verification) (Semana 5–6)**  
**Objetivo:** baseline, supuestos, comparación y reporte exportable.

### Entregables:
- Baseline configurable  
- Panel de supuestos  
- Comparación cuantitativa  
- Export PDF + CSV  
- Reproducibilidad por timestamp/versión  

**Resultado:** MASS Simple se convierte en un producto serio.

---

## **Fase 4 — Observabilidad + Audit Trail (Semana 7)**  
**Objetivo:** cumplir requisitos de hyperscalers.

### Entregables:
- OpenTelemetry (traces + metrics + logs estructurados)  
- Collector local  
- Correlación trace_id/span_id  
- Audit trail completo (inputs, outputs, versiones, commit hash)  
- Panel de auditoría  

**Resultado:** MASS Simple cumple estándares enterprise.

---

## **Fase 5 — Integración BioCore (Semana 8)**  
**Objetivo:** conectar el modelo real como caja negra.

### Entregables:
- Cliente robusto (timeouts, retries, circuit breaker)  
- Cache control  
- Recomendaciones reales en dashboard  
- Logs de cada recomendación  

**Resultado:** MASS Simple deja de ser un mock y se vuelve un producto real.

---

## **Fase 6 — Deploy Cloud + Helm Chart (Semana 9)**  
**Objetivo:** demo online para inversores y clientes.

### Entregables:
- Helm chart v0.1  
- Deploy cloud con HTTPS  
- Password-protected  
- Script de actualización  
- Notas de rollback  

**Resultado:** Pilot‑in‑a‑Box listo para PoC con hyperscalers.

---

# 📌 **2. MILESTONES CORREGIDOS (Basados en el estado real)**

Los milestones originales asumían un proyecto desde cero.  
Estos están ajustados al estado actual de MASS Simple.

---

## **Milestone A — Backend Hardening (100% MASS Simple)**
- Seguridad completa  
- Validación de datos  
- Servicios desacoplados  
- Documentación OpenAPI  
- Tests mínimos  
- Pipeline de ingesta estable  

**Duración:** 1–2 semanas  
**Dependencia:** ninguna  

---

## **Milestone B — Dashboard Profesional**
- Next.js  
- KPIs  
- Before/after  
- Filtros  
- Export CSV  

**Duración:** 2 semanas  
**Dependencia:** A  

---

## **Milestone C — M&V**
- Baseline  
- Supuestos  
- Comparación  
- Export PDF/CSV  

**Duración:** 2 semanas  
**Dependencia:** B  

---

## **Milestone D — Observabilidad + Audit Trail**
- OpenTelemetry  
- Logs estructurados  
- Collector  
- Audit trail completo  

**Duración:** 1 semana  
**Dependencia:** C  

---

## **Milestone E — Integración BioCore**
- Cliente robusto  
- Recomendaciones reales  
- Logs de cada recomendación  

**Duración:** 1 semana  
**Dependencia:** D  

---

## **Milestone F — Deploy Cloud + Helm Chart**
- Helm chart  
- HTTPS  
- Password-protection  
- Script de actualización  

**Duración:** 1 semana  
**Dependencia:** E  

---

# 📌 **3. GAP ANALYSIS VISUAL (ASCII)**

Este análisis muestra **qué pide el Pilot‑in‑a‑Box** vs **qué tiene MASS Simple hoy**.

```
+---------------------------+----------------------+----------------------+
| COMPONENTE                | ESTADO ACTUAL       | GAP                 |
+---------------------------+----------------------+----------------------+
| Backend FastAPI           | ✔ Estable           | —                    |
| Postgres                  | ✔ Conectado         | —                    |
| Docker Compose            | ✔ Determinístico    | —                    |
| Next.js Dashboard         | ✘ No existe         | 100%                 |
| Ingesta completa          | ◐ Parcial           | 40%                  |
| Validación/normalización  | ◐ Parcial           | 50%                  |
| M&V                       | ✘ No existe         | 100%                 |
| KPIs / Before-After       | ✘ No existe         | 100%                 |
| Export CSV/PDF            | ✘ No existe         | 100%                 |
| Audit Trail               | ✘ No existe         | 100%                 |
| Observabilidad (OTEL)     | ✘ No existe         | 100%                 |
| Seguridad (JWT/Roles)     | ◐ Parcial           | 60%                  |
| BioCore Integration       | ✘ No existe         | 100%                 |
| Helm Chart                | ✘ No existe         | 100%                 |
| Deploy Cloud HTTPS        | ✘ No existe         | 100%                 |
+---------------------------+----------------------+----------------------+
```

---

# 📌 **4. PLAN DE RESCATE (Alineación con Pilot‑in‑a‑Box)**

Este plan está diseñado para **cerrar MASS Simple** y **alinearlo con el Pilot‑in‑a‑Box original**, sin reescribir nada y sin deuda técnica.

---

## **Paso 1 — Consolidar Backend (rescate inmediato)**
- Terminar autenticación  
- Validar datos  
- Desacoplar servicios  
- Documentación OpenAPI  
- Tests mínimos  

**Resultado:** backend sólido y extensible.

---

## **Paso 2 — Construir Dashboard (rescate funcional)**
- Next.js  
- KPIs  
- Before/after  
- Filtros  
- Export CSV  

**Resultado:** primera demo real.

---

## **Paso 3 — Implementar M&V (rescate metodológico)**
- Baseline  
- Supuestos  
- Comparación  
- Export PDF/CSV  

**Resultado:** MASS Simple se vuelve un producto serio.

---

## **Paso 4 — Observabilidad + Audit Trail (rescate enterprise)**
- OpenTelemetry  
- Logs estructurados  
- Collector  
- Audit trail completo  

**Resultado:** cumple estándares de hyperscalers.

---

## **Paso 5 — Integrar BioCore (rescate de valor real)**
- Cliente robusto  
- Recomendaciones reales  
- Logs de cada recomendación  

**Resultado:** MASS Simple deja de ser un mock.

---

## **Paso 6 — Deploy Cloud + Helm Chart (rescate final)**
- Helm chart  
- HTTPS  
- Password-protection  
- Script de actualización  

**Resultado:** Pilot‑in‑a‑Box listo para PoC.

---

# 🎯 **CONCLUSIÓN**

Con este roadmap, milestones corregidos, gap analysis y plan de rescate:

- MASS Simple puede transformarse en un **Pilot‑in‑a‑Box real**  
- Sin reescrituras  
- Sin deuda técnica  
- Con un camino claro y ejecutable  
- Y con un orden que evita retrocesos  

