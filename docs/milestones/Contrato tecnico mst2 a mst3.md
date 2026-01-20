Perfecto, Leonardo.  
Acá tenés **el Documento de Continuidad oficial**, diseñado para que puedas copiarlo en esta UI antes de cada sesión y garantizar que **nunca más haya desvíos**, que **no se pierdan horas**, y que **el proyecto avance exactamente según la especificación del cliente**.

Lo escribí como un **contrato técnico**, claro, preciso y sin ambigüedades.

---

# 📘 **DOCUMENTO DE CONTINUIDAD — Milestone 2 → Milestone 3**  
**Estado oficial del proyecto**  
**Versión: 1.0 (19 Ene 2026)**  
**Responsable: Leonardo**

---

# 🟦 **1. Estado EXACTO del backend al finalizar Milestone 2**

### ✔ Arquitectura vigente
```
backend/
  app/
    api/
      v1/
        json_request.py
    core/
      config.py
      logging.py
    models/
      mass_request.py
    services/
      validate.py
      normalize.py
      save.py
      send.py
    db/
      base.py
      session.py
    main.py
```

### ✔ Endpoints activos
```
POST /v1/json-request/validate
POST /v1/json-request/normalize
POST /v1/json-request/save
POST /v1/json-request/send
GET  /v1/json-request/{id}/logs
```

### ✔ Esquema MASS vigente (el del cliente)
Este es el **único** contrato válido:

```json
{
  "mass_version": "1.1",
  "timestamp": "2025-01-01T12:00:00Z",
  "device": {
    "id": "string",
    "type": "string",
    "location": "string"
  },
  "metrics": {
    "temperature_celsius": 22.5,
    "humidity_percent": 55.2,
    "pressure_hpa": 1013.25
  },
  "metadata": {
    "operator": "string",
    "batch_id": "string",
    "notes": "string"
  }
}
```

### ✔ Base de datos
- Tabla principal: `mass_requests`
- Campos: id, payload_json, created_at, updated_at
- No existen tablas enterprise (tenant, idempotency, SLO, etc.)

### ✔ Validación
- Solo valida el MASS simple  
- No existen campos enterprise  
- No existe envelope enterprise  

### ✔ Normalización
- Limpieza de strings  
- Normalización de timestamp  
- Conversión de unidades  
- Validación de tipos  

### ✔ Save
- Guarda el MASS simple en Postgres  
- Devuelve un `id`  

### ✔ Send
- Envía el MASS simple a la blackbox  
- No requiere envelope enterprise  

---

# 🟩 **2. Estado EXACTO del frontend al finalizar Milestone 2**

### ✔ Rutas activas
```
/ingestion
/login (placeholder, sin backend)
/validate
/normalize
/save
/send
/logs
```

### ✔ Payload enviado al backend
El frontend envía **MASS simple**, sin envelope.

### ✔ No existe autenticación real
- No hay JWT  
- No hay tabla users  
- No hay login funcional  

---

# 🟥 **3. Qué NO debe modificarse en Milestone 3 (prohibido)**

### ❌ NO cambiar el contrato MASS  
### ❌ NO agregar campos enterprise  
### ❌ NO agregar envelope enterprise  
### ❌ NO modificar los endpoints  
### ❌ NO cambiar la estructura del JSON  
### ❌ NO agregar validaciones nuevas no solicitadas  
### ❌ NO alterar la base de datos  
### ❌ NO introducir multitenancy, idempotencia, SLO, data contracts, signals  
### ❌ NO modificar el pipeline MASS (validate → normalize → save → send → logs)

---

# 🟦 **4. Qué SÍ debe implementarse en Milestone 3 (únicamente)**

### ✔ 1. Instrumentar backend FastAPI con OpenTelemetry (traces)
- tracer provider  
- span processors  
- OTLP exporter  
- trace_id y span_id en logs  

### ✔ 2. Integrar OpenTelemetry Collector en Docker Compose
- puerto 4317 (gRPC)  
- puerto 4318 (HTTP)  
- pipeline: receiver → processor → exporter  

### ✔ 3. Instrumentar frontend Next.js con OpenTelemetry Web
- WebTracerProvider  
- FetchInstrumentation  
- propagación de traceparent  
- exportación a collector  

### ✔ 4. Añadir logs estructurados con trace_id y span_id
- logging JSON  
- correlación backend → blackbox  

### ✔ 5. Añadir métricas básicas
- latencia  
- throughput  
- errores  

---

# 🟩 **5. Ejemplo de JSON válido para pruebas**

```json
{
  "mass_version": "1.1",
  "timestamp": "2025-01-01T12:00:00Z",
  "device": {
    "id": "device-123",
    "type": "sensor",
    "location": "Buenos Aires"
  },
  "metrics": {
    "temperature_celsius": 22.5,
    "humidity_percent": 55.2,
    "pressure_hpa": 1013.25
  },
  "metadata": {
    "operator": "Leonardo",
    "batch_id": "batch-001",
    "notes": "Prueba inicial del pipeline MASS"
  }
}
```

---

# 🟦 **6. Punto EXACTO desde donde continuar Milestone 3**

### ✔ Backend  
- Estado: MASS simple  
- Sin envelope enterprise  
- Sin campos enterprise  
- Sin validadores enterprise  
- Sin modelos enterprise  
- Sin autenticación  
- Sin multitenancy  
- Sin idempotencia  

### ✔ Frontend  
- Envío de MASS simple  
- Sin login real  
- Sin tokens  
- Sin envelope enterprise  

### ✔ Objetivo inmediato  
**Agregar observabilidad sin alterar el contrato MASS.**

---

# 🟩 **7. Instrucciones para continuar sin desvíos**

Antes de cada sesión, Leonardo debe copiar en esta UI:

```
Continuamos desde el Documento de Continuidad — Milestone 2 → Milestone 3 (versión 1.0).
El backend usa MASS simple.
No se permite envelope enterprise.
No se permite agregar campos no solicitados.
Solo trabajamos en observabilidad.
```

Con eso, yo continúo EXACTAMENTE desde el estado correcto.

---

Si querés, puedo preparar también la **versión 1.1**, que incluiría:

- commit base sugerido  
- estructura de carpetas ideal  
- checklist de verificación rápida  

Solo decime y la preparo.
