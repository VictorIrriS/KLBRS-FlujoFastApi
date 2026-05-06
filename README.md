# KLBRS - Flujo FastAPI

Proyecto de ejemplo con FastAPI que implementa un flujo completo de:

- Envío de formulario desde frontend
- Generación de token de verificación
- Verificación de dominio (DNS o archivo TXT)
- Activación de siguiente paso (ej. pago simulado)
- Envío de emails vía SMTP

---



# Instalación del entorno

## Clonar el repositorio

```bash
git clone https://github.com/VictorIrriS/KLBRS-FlujoFastApi.git
cd KLBRS-FlujoFastApi
```

## Crear entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

## Instalar dependencias

```bash
pip install -r requirements.txt
```
## Activar nginx

```bash
sudo systemctl start nginx
```

---
## Ejecutar main.py
```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```
Abrir en el navegador
http://127.0.0.1:8000

# Variables de entorno

crear .env con
```
SMTP_HOST=smtp.tudominio.com
SMTP_PORT=465
SMTP_USER=tu_email
SMTP_PASS=tu_password
EMAIL_TO=destino@dominio.com
```

---

# Pipeline Propuesto

## Git (GitHub/GitLab)

- main: prod
- dev: integración
- feature/*: desarrollo
 
## CI 

- Test (pytest)
- Linting (isort, black, flake8)
- SAST (Bandit)
- DAST (ZAP)
   
## Artifact (Docker image)

- Python runtime
- App
- requirements.txt
- configuracion runtime
   
## Registry (GHCR / Harbor / GitLab Registry)

- Versionado de imágenes
- Rollbacks
   
## CD (deploy)

- Bajar la imagen del Registry
- actualizar contenedores
- reiniciar servicios
   
## Server (Docker Compose / Kubernetes)

- Docker Compose: "simple y rapido"
- Kubernetes: "auto escalado y secrets management"

## Nginx reverse proxy

- Https
- Rate limiting
- Routing





