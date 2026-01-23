
# 📄 **ESTIMATE.md**  
*Estimación de horas de desarrollo para completar MASS Simple → Pilot‑in‑a‑Box*

---

# # 1. Resumen Ejecutivo

Esta estimación se basa en:

- El estado actual real del proyecto MASS Simple  
- El gap contra el alcance original del Pilot‑in‑a‑Box  
- El roadmap y los milestones corregidos  
- La arquitectura objetivo  
- Buenas prácticas de ingeniería y tiempos razonables para un dev senior  

La estimación contempla backend, frontend, observabilidad, M&V, BioCore y deploy cloud.

---

# # 2. Estimación por EPIC

## **EPIC 1 — Backend Hardening (MVP MASS Simple)**  
**64–90 h**

| Feature | Horas |
|--------|-------|
| Seguridad completa | 18–24 h |
| Validación + sanitización + normalización | 16–22 h |
| Servicios desacoplados | 10–14 h |
| Documentación OpenAPI | 8–12 h |
| Tests | 12–18 h |

---

## **EPIC 2 — Dashboard Profesional (Next.js)**  
**54–78 h**

| Feature | Horas |
|--------|-------|
| Setup Next.js + UI | 12–18 h |
| KPIs + tendencias | 16–22 h |
| Before/after + filtros | 20–28 h |
| Export CSV | 6–10 h |

---

## **EPIC 3 — M&V (Measurement & Verification)**  
**48–66 h**

| Feature | Horas |
|--------|-------|
| Baseline | 12–16 h |
| Supuestos | 10–14 h |
| Comparación cuantitativa | 16–22 h |
| Export PDF | 10–14 h |

---

## **EPIC 4 — Observabilidad + Audit Trail**  
**38–58 h**

| Feature | Horas |
|--------|-------|
| OpenTelemetry backend | 12–18 h |
| OpenTelemetry frontend | 6–10 h |
| Logs estructurados | 6–10 h |
| Audit trail completo | 14–20 h |

---

## **EPIC 5 — Integración BioCore**  
**22–32 h**

| Feature | Horas |
|--------|-------|
| Cliente BioCore | 12–18 h |
| Recomendaciones en dashboard | 10–14 h |

---

## **EPIC 6 — Deploy Cloud + Helm Chart**  
**28–42 h**

| Feature | Horas |
|--------|-------|
| Helm chart | 12–18 h |
| HTTPS + password-protection | 10–14 h |
| Scripts de operación | 6–10 h |

---

# # 3. Total de horas estimadas

### **Total optimista:** 254 h  
### **Total realista:** **300–330 h**  
### **Total conservador:** 360 h  

---

# # 4. Factores que pueden acelerar

- UI prearmada  
- Plantillas OTEL  
- Helm chart base  
- Dataset estable  
- BioCore estable desde el inicio  

**Ahorro estimado:** 10–15%

---

# # 5. Factores que pueden retrasar

- Cambios en dataset  
- Cambios en metodología M&V  
- Requerimientos de UI personalizados  
- Cambios en API de BioCore  
- Requerimientos de seguridad adicionales  

**Retraso estimado:** 10–20%

---

# # 6. Conclusión

Para entregar un **Pilot‑in‑a‑Box completo**, alineado con el documento original del cliente y con estándares enterprise, se requieren:

# ⭐ **300–330 horas de desarrollo (estimación realista)**

---
