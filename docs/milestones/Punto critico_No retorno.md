Leonardo… acá tenés **el Documento de Continuidad unificado**, completamente integrado, coherente, sin contradicciones, y listo para copiar/pegar en tu próxima sesión.  
Este documento consolida:

- El estado actual del proyecto  
- Las reglas de oro para evitar drift  
- El plan de desarrollo de MASS simple  
- El plan de autenticación con Argon2 + JWT  
- El impacto en backend y frontend  
- El camino concreto para los próximos 3 días  

Todo en un único documento maestro.

---

# 📄 **DOCUMENTO DE CONTINUIDAD — MASS SIMPLE + AUTENTICACIÓN (MVP en 3 días)**

Copiá esto tal cual en tu próxima sesión para que pueda retomar sin desvíos.

---

# 🟦 1. Estado actual del proyecto

- Repositorio: **pilot-in-a-box**  
- Rama: **main**  
- Estado: **limpio, estable, sin drift**  
- Backend MASS simple reconstruido desde cero:
  - `Base` minimalista (`declarative_base`)
  - `MassRequest` como único modelo activo
  - `session.py` y `base.py` correctos
  - `env.py` limpio, sin sobrescritura de URL
  - `alembic.ini` apuntando a:
    ```
    postgresql://postgres:postgres@localhost:5432/pilot
    ```
- Docker funcionando correctamente:
  - Contenedor `pib-db` (Postgres)
  - Base `pilot` sincronizada
- No hay residuos del proyecto viejo en modelos ni migraciones.

---

# 🟦 2. Migraciones

- Carpeta `backend/migrations/versions/` contiene **solo**:
  ```
  1facca6dc8e8_create_mass_requests_table.py
  ```
- Migración generada automáticamente y aplicada con éxito.
- La tabla `mass_requests` existe en la base `pilot`.
- La tabla `alembic_version` está sincronizada.

---

# 🟦 3. Reglas de oro para evitar drift

1. **Nunca** reintroducir modelos viejos (users, items, roles, etc.).  
2. `backend/db/base.py` debe seguir minimalista.  
3. `env.py` NO debe importar `settings.DATABASE_URL`.  
4. Siempre ejecutar Alembic desde:
   ```
   backend/
   ```
5. La carpeta `versions/` debe contener solo migraciones válidas del proyecto actual.  
6. Si aparece:
   ```
   Target database is not up to date
   ```
   revisar:
   - que no haya migraciones viejas en `versions/`
   - que Alembic esté usando el `alembic.ini` correcto
   - que la base `pilot` esté limpia

---

# 🟦 4. Alcance de seguridad para el MVP (Autenticación mínima)

El MVP debe incluir **login real** con:

### ✔ Requisitos incluidos
- Un solo tipo de usuario (sin roles, sin permisos avanzados).  
- Usuario seed en la base:
  - email: `admin@example.com`
  - password: definido por Leonardo
- Password hashing con **Argon2** (`argon2-cffi`).
- Endpoint:
  ```
  POST /auth/login
  ```
  que recibe email + password y devuelve tokens.
- Tokens tipo JWT:
  - `access_token` (expira en 15–30 min)
  - `refresh_token` opcional (solo si hay tiempo)
- Protección obligatoria:
  ```
  Authorization: Bearer <token>
  ```
  en todos los endpoints `/mass-requests/*`.

### ❌ No incluido en el MVP
- Registro de usuarios  
- Recuperación de contraseña  
- Multi-tenant  
- Roles o permisos  
- Auditoría avanzada  

**Objetivo:**  
El cliente debe ver que MASS tiene login, seguridad y tokens, y que sin login no se puede usar.

---

# 🟦 5. Impacto en backend MASS simple

### ✔ Agregar modelo `User`
Campos mínimos:
- `id`
- `email`
- `hashed_password`
- `created_at`

### ✔ Servicio de autenticación
Debe:
- buscar usuario por email  
- verificar contraseña con Argon2  
- generar JWT  
- exponer funciones para `get_current_user`

### ✔ Modificaciones en archivos existentes
1. `models/user.py`  
   - Confirmar que contiene `id`, `email`, `hashed_password`.  
   - Si no, corregir.

2. `core/security.py`  
   - instalar `argon2-cffi`  
   - crear `hash_password`  
   - crear `verify_password`  
   - generar JWT

3. `services/auth_service.py`  
   - validar credenciales  
   - generar tokens

4. `routers/auth.py`  
   - exponer:
     ```
     POST /auth/login
     ```
   - devolver:
     ```json
     {
       "access_token": "...",
       "token_type": "bearer"
     }
     ```

5. `routers/mass.py`  
   - agregar dependencia `get_current_user`  
   - proteger todos los endpoints

### ✔ Crear usuario seed
En migración o script:
- email: `admin@example.com`
- password: el que defina Leonardo  
- hasheado con Argon2

---

# 🟦 6. Impacto en la UI del MVP

### ✔ Pantalla de Login
- Formulario: email + password  
- Botón “Ingresar”  
- Si login OK → guardar token (localStorage o memory)  
- Redirigir al dashboard  

### ✔ Pantalla de Dashboard
- Listado de `mass_requests`  
- Botón “Nueva request”  

### ✔ Pantalla de Nueva Request
- Formulario simple (3–5 campos)  
- Enviar token en el header  

### ✔ Comportamiento obligatorio
Si no hay token → redirigir al login.

---

# 🟦 7. Camino concreto desde donde estamos (orden de ejecución)

1. **Agregar modelo User** y seed del usuario demo.  
2. **Configurar Argon2** y hashear password.  
3. **Crear endpoint `POST /auth/login`** que devuelva JWT.  
4. **Proteger `/mass-requests/*`** con token.  
5. **Implementar UI:**
   - Login  
   - Dashboard  
   - Nueva Request  
   - Listado  

---

# 🟦 8. Próximos pasos del desarrollo (MASS simple)

1. Implementar endpoint **POST /mass-requests/**  
2. Implementar servicio correspondiente  
3. Implementar validaciones Pydantic  
4. Implementar GET `/mass-requests/{id}`  
5. Implementar GET `/mass-requests/` (listado)  
6. Implementar DELETE (soft delete si corresponde)  
7. Implementar actualización de estado (pending → processing → done)  
8. Preparar pruebas unitarias  

---

# 🟦 9. Cómo debe continuar Copilot cuando pegues este documento

Cuando abras la nueva sesión y pegues este documento, debo:

- Reconocer el estado exacto del proyecto.  
- Mantener disciplina estricta de continuidad.  
- No introducir modelos, endpoints o migraciones ajenas a MASS simple.  
- No asumir nada fuera del documento.  
- Continuar desde el punto que indiques.  
- Mantener el enfoque en minimalismo, reversibilidad y cero drift.  

---

Leonardo, este documento es tu **piedra angular** para los próximos 3 días.  
Con esto, MASS simple + login seguro + UI mínima es totalmente alcanzable.

Cuando quieras, avanzamos con el **modelo User**, el **seed**, y el **endpoint /auth/login**.
