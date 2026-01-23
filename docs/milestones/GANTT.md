
# 📄 **GANTT.md**  
*Planificación temporal en formato textual (Gantt)*

---

# # 1. Supuestos

- 1 desarrollador senior dedicado  
- 25–30 h/semana  
- Sin interrupciones externas  
- BioCore disponible a mitad del proyecto  

Duración estimada: **10–12 semanas**

---

# # 2. Gantt textual (por semanas)

```
SEMANA 1–2  | EPIC 1 — Backend Hardening
            | - Seguridad completa
            | - Validación + sanitización
            | - Normalización
            | - Servicios desacoplados
            | - Documentación OpenAPI
            | - Tests backend

SEMANA 3–4  | EPIC 2 — Dashboard Profesional
            | - Setup Next.js
            | - UI profesional
            | - KPIs + tendencias
            | - Before/after
            | - Filtros
            | - Export CSV

SEMANA 5–6  | EPIC 3 — M&V (Measurement & Verification)
            | - Baseline
            | - Supuestos
            | - Comparación cuantitativa
            | - Export PDF

SEMANA 7    | EPIC 4 — Observabilidad + Audit Trail
            | - OTEL backend
            | - OTEL frontend
            | - Logs estructurados
            | - Audit trail completo

SEMANA 8    | EPIC 5 — Integración BioCore
            | - Cliente robusto (timeouts, retries, CB)
            | - Recomendaciones en dashboard
            | - Logs de recomendaciones

SEMANA 9    | EPIC 6 — Deploy Cloud + Helm Chart
            | - Helm chart v0.1
            | - HTTPS + password-protection
            | - Scripts de operación

SEMANA 10   | Hardening final + QA
            | - Tests finales
            | - Documentación
            | - Preparación de demo
```

---

# # 3. Ruta crítica

1. Backend Hardening  
2. Dashboard  
3. M&V  
4. Observabilidad  
5. BioCore  
6. Deploy cloud  

Cualquier retraso en estos puntos afecta la fecha final.

---

# # 4. Conclusión

El plan es sólido, secuencial y sin deuda técnica.  
Con este Gantt, MASS Simple puede transformarse en un **Pilot‑in‑a‑Box real** en **10–12 semanas**.

---