# biUNestar - Backend (FastAPI)

Migración del backend de **biUNestar** (bienestar universitario para
estudiantes de la Universidad Nacional de Colombia) de Django a **FastAPI**,
siguiendo los requisitos funcionales/no funcionales del análisis MoSCoW del
proyecto (`Submission_03.pdf`).

Arquitectura por capas, un módulo por entidad:

```
app/modules/<entidad>/
├── model.py        # SQLAlchemy ORM (tabla real en Postgres, esquema `bienestar`)
├── schema.py         # Pydantic (request/response)
├── repository.py       # Acceso a datos (queries)
├── service.py            # Reglas de negocio
└── router.py                # Endpoints FastAPI
```

## Estado del proyecto

### ✅ Autenticación — sin contraseña, con Google Sign-In
No se maneja contraseña en ningún momento. El front-end obtiene un
`id_token` de Google (Google Identity Services) y lo manda a la API, que lo
verifica contra `GOOGLE_CLIENT_ID` y emite un JWT propio.

| Endpoint | Descripción |
|---|---|
| `POST /auth/google` | Login/registro con `id_token` de Google. Crea la cuenta si es la primera vez. Devuelve `access_token` (JWT), `is_new_user`, `profile_incomplete`. |
| `GET /auth/me` | Perfil del usuario autenticado. |

- Solo se aceptan correos de los dominios en `ALLOWED_EMAIL_DOMAINS` (por defecto `unal.edu.co`).
- El primer administrador se crea manualmente en la base de datos (ver sección "Bootstrapping del primer admin" más abajo) — no hay auto-promoción por seguridad.

### ✅ Usuarios y roles (RF_01–RF_05, RF_17)
| Endpoint | Acceso |
|---|---|
| `GET /users` | Solo admin |
| `GET /users/{id}` | Cualquier autenticado |
| `GET /users/by-email/{institutional_email}` | Cualquier autenticado |
| `POST /users` | Solo admin (alta manual, ej. precargar estudiantes) |
| `PATCH /users/{id}` | El propio usuario, o admin sobre cualquiera |
| `DELETE /users/{id}` | Solo admin |
| `GET /roles`, `POST /roles`, ... | CRUD de roles |

### ✅ Hábitos y registro diario (RF_06–RF_09)
Catálogo de hábitos (`GET /habits`) sembrado automáticamente al arrancar:
**Sueño** (horas), **Agua** (vasos), **Actividad física** (minutos).

| Endpoint | Descripción |
|---|---|
| `POST /daily-records/me` | Registra/actualiza el día (sueño, agua, actividad, estado de ánimo con los 8 valores del RF_07, comentario ≤500 chars). Un único registro por día — se sobreescribe, nunca duplica. |
| `GET /daily-records/me/today` | Registro de hoy (404 si aún no existe). |
| `GET /daily-records/me?start_date&end_date` | Histórico por rango (consulta semanal/mensual). |
| `GET /daily-records/me/weekly-averages` | Promedios de la semana (lunes-domingo) de sueño/agua/actividad. |

### ✅ Reportes semanales (RF_11)
| Endpoint | Descripción |
|---|---|
| `POST /reports/me/generate-weekly` | Calcula y persiste el reporte de la semana ISO de una fecha (por defecto hoy). Reutiliza la lógica de promedios; no la duplica. |
| `GET /reports/me` | Histórico de reportes, para graficar en el front-end. |

### ✅ Recordatorios (RF_12)
CRUD completo bajo `/reminders/me`, con verificación de dueño (editar/borrar
un recordatorio ajeno da 404, no 403, para no filtrar información).

### ✅ Recursos de apoyo (RF_16)
| Endpoint | Acceso |
|---|---|
| `GET /resources`, `GET /resources/{id}` | Cualquier autenticado |
| `POST /resources`, `PATCH /resources/{id}`, `DELETE /resources/{id}` | Solo admin |

### ✅ Retroalimentación (RF_18)
| Endpoint | Descripción |
|---|---|
| `POST /feedback/me` | Categoría (Sugerencia / Reporte de error / Otro) + mensaje ≤1000 chars. **409** si ya se envió una hoy (máximo una por día). |
| `GET /feedback/me` | Las propias. |
| `GET /feedback` | Todas — solo admin. |

### ⏳ Pendiente (Could have / no funcionales de front-end)
- **RF_13**: exportar reportes en PDF.
- **RNF_10**: pruebas unitarias/integración/sistema/usabilidad (pytest).
- **RNF_07, RNF_08, RNF_09**: son de front-end (ya se están cubriendo ahí).

## Configuración

Variables de entorno (`.env`, ver `.env` de ejemplo en el repo):

```env
DB_USER=admin
DB_PASSWORD=admin123
DB_HOST=localhost
DB_PORT=5432
DB_NAME=app_db

GOOGLE_CLIENT_ID=tu_client_id.apps.googleusercontent.com
ALLOWED_EMAIL_DOMAINS=unal.edu.co

JWT_SECRET_KEY=una_clave_larga_y_aleatoria
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440
```

- `GOOGLE_CLIENT_ID` se crea en [Google Cloud Console](https://console.cloud.google.com/apis/credentials) (OAuth Client ID, tipo "Web application"). Debe coincidir con el que use el front-end.
- `JWT_SECRET_KEY` se genera con: `python -c "import secrets; print(secrets.token_hex(32))"`.

## Instalación y arranque

```bash
pip install -r requirements.txt

# Crea la base de datos y corre Database.sql para armar el esquema `bienestar`

uvicorn app.main:app --reload
```

Documentación interactiva: `http://127.0.0.1:8000/docs`

## Probar el login sin front-end

En la raíz del proyecto hay `test_google_login.html`, una página mínima con
el botón de Google que llama directo a `POST /auth/google` y te muestra la
respuesta (incluyendo tu `access_token`, para pegarlo en el botón
**Authorize** de `/docs` y probar el resto de endpoints protegidos).

```bash
python -m http.server 5500
# entra a http://localhost:5500/test_google_login.html
```

Recuerda agregar ese origen (`http://localhost:5500`) en "Authorized
JavaScript origins" de tu OAuth Client ID en Google Cloud Console.

## Bootstrapping del primer admin

No existe auto-promoción a administrador (sería un hueco de seguridad).
Después de tu primer login con Google, promuévete manualmente:

```sql
INSERT INTO bienestar.rol (nombre) VALUES ('Administrador');

UPDATE bienestar.usuario
SET rol_id = (SELECT id FROM bienestar.rol WHERE nombre = 'Administrador')
WHERE correo_institucional = 'tu_correo@unal.edu.co';
```

## Notas de diseño / bugs corregidos sobre el scaffold original

- `comentario` en `registro_diario` estaba en `VARCHAR(255)` pero el RF_07 pide hasta 500 caracteres → ajustado en `Database.sql` y en el modelo.
- Se agregó `categoria` a `retroalimentacion` (requerida por el RF_18, no estaba en el esquema original).
- `CORSMiddleware` no existía → agregado (necesario para que un front-end en otro puerto/origen pueda llamar la API).

## Proyecto relacionado

El front-end vive en una carpeta separada: [`biUNestar-frontend`](../biUNestar-frontend).
# MODS-TLAUNCHER-project-backend
## Ejecución rápida

```bash
chmod +x setup.sh
./setup.sh
