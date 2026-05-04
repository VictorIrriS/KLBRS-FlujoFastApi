# KLBRS - Flujo FastAPI

Proyecto de ejemplo con FastAPI que implementa un flujo completo de:

- Envío de formulario desde frontend
- Generación de token de verificación
- Verificación de dominio (DNS o archivo TXT)
- Activación de siguiente paso (ej. pago simulado)
- Envío de emails vía SMTP

---



# Instalación del entorno

## 1. Clonar el repositorio

```bash
git clone https://github.com/VictorIrriS/KLBRS-FlujoFastApi.git
cd KLBRS-FlujoFastApi
```

## 2. Crear entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Instalar dependencias

```bash
pip install -r requirements.txt
```
---
#Ejecutar el proyecto
```bash
uvicorn main:app --reload
```
Abrir en el navegador
http://127.0.0.1:8000

#Variables de entorno

crear .env con
```
SMTP_HOST=smtp.tudominio.com
SMTP_PORT=465
SMTP_USER=tu_email
SMTP_PASS=tu_password
EMAIL_TO=destino@dominio.com
```
