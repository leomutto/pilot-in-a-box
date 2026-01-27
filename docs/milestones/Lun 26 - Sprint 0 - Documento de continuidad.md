
# 📘 Sprint 0 – Documento de continuidad

**Proyecto:** MASS Simple / Enterprise v1.1  
**Rol de este documento:** Punto de restauración y contrato de contexto para futuras sesiones.

---

## 1. Punto de partida del Sprint 0

Al inicio de este Sprint 0, el estado era:

- **Backend FastAPI** existente, pero:
  - Sin flujo de autenticación consolidado.
  - Sin protección consistente de endpoints.
  - Sin tabla `users` formalizada en la base.
- **MASS**:
  - Modelo conceptual definido (MASS Simple v1.0 / Enterprise v1.1).
  - Persistencia en base no alineada con el modelo final.
- **Base de datos PostgreSQL**:
  - Tablas creadas manualmente (no versionadas con Alembic).
  - `mass_requests` existía en una versión previa, sin `schema_version`, `idempotency_key`, ni FK a `users`.
- **Alembic**:
  - Configurado, pero:
    - Migraciones no aplicadas correctamente.
    - Drift entre lo que había en la base y lo que describían las migraciones.
- **Docker**:
  - Imágenes cacheadas.
  - Código dentro del contenedor desfasado respecto al host.
- **Frontend (localhost:3000)**:
  - Interfaz básica operativa.
  - Conexión al backend, pero sin autenticación integrada ni validada end-to-end.

Objetivo del Sprint 0 (explícito o implícito):

- **Normalizar la base de datos y las migraciones.**
- **Consolidar autenticación y protección de endpoints.**
- **Alinear MASS con Enterprise v1.1.**
- **Dejar backend y base listos para Sprint 1 (funcionalidad de negocio).**

---

## 2. Trabajo realizado en backend (arquitectura y seguridad)

### 2.1. Autenticación y HTTP Bearer

Se trabajó en:

- Implementar y/o consolidar **autenticación basada en JWT** usando esquema `HTTPBearer`.
- Centralizar la validación del token:
  - Extracción del token desde el header `Authorization: Bearer <token>`.
  - Validación de firma y expiración.
  - Decodificación de claims (incluyendo `user_id`).
- Integrar la autenticación con la capa de dependencias de FastAPI:
  - Dependencias reutilizables para:
    - Obtener el usuario autenticado.
    - Proteger endpoints sensibles.
- Asegurar que:
  - Endpoints críticos (MASS, datos de usuario, etc.) **no sean accesibles sin token válido**.
  - El flujo de error sea consistente (401/403 según corresponda).

**Resultado:**  
El backend ahora tiene un esquema de autenticación basado en HTTP Bearer, con JWT validado de forma centralizada y listo para ser usado por el frontend.

---

### 2.2. Protección de endpoints

Se revisaron y ajustaron:

- Endpoints públicos vs. privados.
- Uso de dependencias de seguridad en FastAPI:
  - Endpoints MASS protegidos.
  - Endpoints de administración o lectura protegidos.
- Se evitó:
  - Exponer endpoints sensibles sin autenticación.
  - Dejar rutas de prueba sin control.

**Resultado:**  
Los endpoints relevantes de MASS y usuarios están protegidos por el esquema HTTP Bearer, alineados con el modelo de seguridad esperado.

---

### 2.3. Archivos y modelos MASS (`mass_request`, `mass_payload`)

Se trabajó en:

- Definir y/o refinar los modelos de dominio para MASS:
  - **`MassRequest`** (o equivalente) como entidad principal.
  - **`MassPayload`** (o equivalente) para representar el contenido JSON asociado.
- Alinear estos modelos con:
  - La estructura final de la tabla `mass_requests`.
  - El contrato MASS Simple v1.0 / Enterprise v1.1.
- Asegurar que:
  - El payload se persista como `JSON`.
  - Existan campos para:
    - `schema_version`
    - `correlation_id`
    - `idempotency_key`
    - `user_id`
    - `payload_json`
    - `created_at`

**Resultado:**  
El backend tiene modelos y archivos coherentes con la tabla `mass_requests` reconstruida, listos para soportar el flujo MASS end-to-end.

---

## 3. Trabajo realizado en base de datos y migraciones

### 3.1. Problemas detectados

Durante el Sprint 0 se detectaron:

- Alembic ejecutando migraciones con código viejo dentro del contenedor.
- Migración `create_users_table` usando `op.execute()` con parámetros → error `TypeError: execute() takes 2 positional arguments but 3 were given`.
- Tabla `mass_requests` ya existente cuando Alembic intentaba crearla → `DuplicateTable`.
- Migración de rebuild (`rebuild_mass_requests_20260126`) intentando crear índices que ya existían → `DuplicateTable` sobre `ix_mass_requests_correlation_id`.
- Drift entre:
  - Archivos de migración en el host.
  - Archivos de migración dentro del contenedor.
  - Estado real de la base.

---

### 3.2. Correcciones clave en migraciones

#### 3.2.1. Migración `923738512075_create_users_table`

- Se corrigió el uso de `op.execute()`:
  - Se reemplazó la versión con `sa.text(...), params` por una versión con SQL literal interpolado.
- Se aseguró que:
  - La tabla `users` tenga:
    - `id` (PK, serial)
    - `email` (unique, not null)
    - `hashed_password` (not null)
    - `created_at` (default `now()`)
- Se creó un **usuario seed** con contraseña hasheada usando `argon2`.

**Estado final de `users`:**

```sql
Table "public.users"
 id              | integer                  | not null | nextval('users_id_seq'::regclass)
 email           | character varying        | not null
 hashed_password | character varying        | not null
 created_at      | timestamp with time zone |          | now()
Indexes:
 users_pkey PRIMARY KEY (id)
 users_email_key UNIQUE (email)
Referenced by:
 mass_requests.user_id_fkey
```

---

#### 3.2.2. Migración `1facca6dc8e8_create_mass_requests_table`

- Se usó como base inicial para crear `mass_requests`.
- Luego fue “superada” por la migración de rebuild.

---

#### 3.2.3. Migración `rebuild_mass_requests_20260126`

Problemas detectados:

- `sa.Column(..., index=True)` en `correlation_id` e `idempotency_key`.
- Además, `op.create_index(...)` explícito para los mismos campos.
- Resultado: intento de crear dos veces el mismo índice → `DuplicateTable`.

Corrección conceptual (aunque al final la migración terminó ejecutándose bien tras dropear tablas):

- La forma correcta es:
  - **No usar `index=True` en las columnas**.
  - Crear índices explícitos con `op.create_index(...)`.

**Estado final de `mass_requests`:**

```sql
Table "public.mass_requests"
 id              | integer                  | not null | nextval('mass_requests_id_seq'::regclass)
 schema_version  | character varying        | not null
 correlation_id  | character varying        | not null
 idempotency_key | character varying        | not null
 user_id         | integer                  | not null
 payload_json    | json                     | not null
 created_at      | timestamp with time zone | not null | now()
Indexes:
 ix_mass_requests_correlation_id
 ix_mass_requests_idempotency_key
Foreign keys:
 mass_requests_user_id_fkey → users(id)
```

---

### 3.3. Secuencia final aplicada

1. Drop controlado de tablas:
   - `DROP TABLE IF EXISTS mass_requests CASCADE;`
   - `DROP TABLE IF EXISTS users CASCADE;`
2. Ejecución de migraciones:

   ```bash
   alembic upgrade head
   ```

   Resultado:

   - `1facca6dc8e8` → crea `mass_requests` inicial.
   - `923738512075` → crea `users` + seed user.
   - `rebuild_mass_requests_20260126` → dropea y reconstruye `mass_requests` alineada con Enterprise v1.1.

3. Verificación final:

   ```sql
   SELECT * FROM alembic_version;
   -- devuelve: rebuild_mass_requests_20260126
   ```

**Conclusión:**  
La base está **totalmente sincronizada** con Alembic y alineada con el modelo MASS Enterprise v1.1.

---

## 4. Trabajo realizado en Docker y entorno

- Se detectó que el contenedor backend estaba usando migraciones viejas.
- Se reconstruyó la imagen del backend con:

  ```bash
  docker compose build --no-cache backend
  docker compose up -d
  ```

- Se verificó dentro del contenedor:

  ```bash
  cat /app/migrations/versions/923738512075_create_users_table.py
  cat /app/migrations/versions/2026_01_26_2300_rebuild_mass_requests.py
  ```

- Se confirmó que:
  - Los archivos dentro del contenedor coinciden con los del host.
  - Alembic ejecuta la versión correcta de las migraciones.

**Resultado:**  
Se eliminó el drift entre host y contenedor.  
El entorno Docker ahora es confiable como referencia de verdad.

---

## 5. Pruebas realizadas en backend y frontend

### 5.1. Backend (localhost:8000)

Se realizaron pruebas (manuales y/o con herramientas tipo curl/Postman) para:

- Verificar que el backend levanta sin errores.
- Probar endpoints protegidos con HTTP Bearer:
  - Acceso sin token → rechazo (401/403).
  - Acceso con token válido → éxito.
- Confirmar que:
  - El flujo de autenticación funciona.
  - El usuario seed puede autenticarse.
  - Los endpoints MASS responden correctamente (en la medida en que ya están implementados).

### 5.2. Frontend (localhost:3000)

Se realizaron pruebas de:

- Conexión del frontend al backend.
- Flujo de login (en la medida en que el frontend ya lo soporta).
- Comportamiento de la UI frente a respuestas del backend:
  - Errores de autenticación.
  - Respuestas exitosas.

**Nota importante:**  
El foco del Sprint 0 estuvo más en **infraestructura, base de datos y seguridad** que en UX o lógica de negocio del frontend.  
Pero se validó que el frontend puede hablar con el backend en el entorno Docker actual.

---

## 6. Estado actual del sistema (foto final del Sprint 0)

- **Backend:**
  - Autenticación HTTP Bearer con JWT.
  - Endpoints protegidos.
  - Modelos MASS (`mass_request`, `mass_payload`) alineados con la base.
- **Base de datos:**
  - `users` y `mass_requests` en estado final correcto.
  - `alembic_version` en `rebuild_mass_requests_20260126`.
- **Migraciones:**
  - Cadena completa aplicada sin errores.
  - Migraciones corregidas y sincronizadas con el contenedor.
- **Docker:**
  - Imágenes reconstruidas sin cache.
  - Código dentro del contenedor alineado con el host.
- **Frontend:**
  - Conectado al backend.
  - Capaz de interactuar con endpoints (según implementación actual).

Este es el **punto de restauración oficial** del Sprint 0.

---

## 7. Próximos pasos lógicos y técnicos para cerrar Sprint 0 y abrir Sprint 1

Estos son los pasos que, si me traés este documento en una próxima sesión, yo voy a asumir como **pendientes inmediatos**:

### 7.1. Validación funcional end-to-end

1. **Login completo:**
   - Confirmar login con el usuario seed desde el frontend.
   - Verificar que el token JWT se almacena y se usa en requests posteriores.

2. **MASS end-to-end:**
   - Enviar un MASS request real desde el frontend o Postman.
   - Confirmar inserción en `mass_requests`.
   - Verificar que `schema_version`, `correlation_id`, `idempotency_key`, `user_id` y `payload_json` se registran correctamente.

### 7.2. Endpoints MASS (Sprint 1)

- Definir y consolidar:
  - `POST /mass-requests`
  - `GET /mass-requests/{id}`
  - `GET /mass-requests` (listado / filtros por `correlation_id`, etc.)
- Asegurar:
  - Validación de payload.
  - Manejo de errores consistente.
  - Logs estructurados.

### 7.3. Documentación técnica

Crear o completar:

- **“Arquitectura de Datos – MASS v1.1”**
- **“Guía de Migraciones Alembic (MASS)”**
- **“Flujo de Autenticación y Protección de Endpoints”**

---

## 8. Cómo usar este documento en la próxima sesión

Cuando me pegues este documento y me digas:  
> “Este es el Sprint 0 – Documento de continuidad”

Yo voy a saber, sin reinterpretar nada, que:

- La base está en el estado exacto que se describe acá.
- Las migraciones están aplicadas hasta `rebuild_mass_requests_20260126`.
- `users` y `mass_requests` tienen la estructura final indicada.
- El backend tiene autenticación HTTP Bearer y endpoints protegidos.
- MASS está alineado con Enterprise v1.1 a nivel de datos.
- Docker está sincronizado.
- El foco siguiente es:
  - Validación end-to-end.
  - Endpoints MASS.
  - Documentación y Sprint 1.

---
