# Milestone 4 — Seguridad, Autenticación y Roles

## 🎯 Objetivo General
Implementar un sistema de autenticación y autorización robusto, escalable y alineado con estándares modernos, integrando:

- JWT con expiración y refresh tokens
- Roles y permisos (RBAC)
- Protección de endpoints del backend
- Integración con el frontend
- Middleware de seguridad
- Auditoría y trazabilidad

---

# 1. Autenticación con JWT (Access + Refresh)

### Tareas
- Crear modelo `User`
- Crear tabla `users`
- Crear endpoint `/auth/login`
- Crear endpoint `/auth/refresh`
- Crear endpoint `/auth/me`
- Implementar hashing de contraseñas (bcrypt)
- Implementar expiración de tokens

### Resultado
Usuarios pueden autenticarse y obtener tokens seguros.

---

# 2. Autorización basada en roles (RBAC)

### Tareas
- Crear tabla `roles`
- Crear tabla `user_roles`
- Definir roles:
  - `admin`
  - `analyst`
  - `viewer`
- Crear dependencia FastAPI:
  ```python
  def require_role(role: str):
      ...
  ```
- Proteger endpoints:
  ```python
  @router.get("/logs", dependencies=[Depends(require_role("admin"))])
  ```

### Resultado
Control de acceso granular y seguro.

---

# 3. Middleware de seguridad

### Tareas
- Crear middleware que:
  - valide JWT
  - extraiga `user_id`
  - agregue `user_id` al contexto de trazas OTel
  - registre auditoría

### Resultado
Cada request queda asociada a un usuario.

---

# 4. Auditoría y trazabilidad

### Tareas
- Crear tabla `audit_logs`
- Registrar:
  - user_id
  - endpoint
  - método
  - timestamp
  - trace_id
- Integrar con OpenTelemetry

### Resultado
Auditoría completa y correlacionada con trazas.

---

# 5. Integración con el frontend

### Tareas
- Crear formulario de login
- Guardar tokens en `httpOnly cookies`
- Implementar refresh automático
- Proteger rutas del frontend
- Mostrar datos del usuario autenticado

### Resultado
Frontend seguro y sincronizado con backend.

---

# 6. Documentación

### Tareas
- Documentar flujo de autenticación
- Documentar roles y permisos
- Documentar endpoints protegidos
- Actualizar README

---

# ✔ Resultado Final del Milestone 4

- Autenticación JWT completa  
- Roles y permisos funcionando  
- Auditoría integrada con OTel  
- Backend protegido  
- Frontend con login y rutas seguras  
- Documentación lista para revisión  